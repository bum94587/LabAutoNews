"""Record the SiLA 2 traffic a twin server handles: every gRPC call, as one JSON line each.

SiLA 2 runs on gRPC, so "SiLA traffic" is gRPC calls with protobuf messages. A server-side gRPC
interceptor sees each call before the feature implementation does; this one wraps the handler,
times it, and writes what came in and went out to ``runtime/traffic/sila_<server>.jsonl``.

What a SiLA call looks like on the wire (RPC names come from the feature definition):

* unobservable command ``Initialize``: one unary call, ``.../LiquidHandlerService/Initialize``
* unobservable property ``InstrumentInfo``: unary ``Get_InstrumentInfo``
* observable property ``Status``: server stream ``Subscribe_Status`` (one item per change)
* observable command ``Transfer``: unary ``Transfer`` (returns a command execution UUID), then
  server streams ``Transfer_Info`` (status, progress) and ``Transfer_Intermediate`` (``Step``
  strings), then unary ``Transfer_Result``
* SiLA errors travel as an ABORTED gRPC status whose details are a base64 ``SiLAError`` message;
  they are decoded here, so a defined execution error shows up by name.

Line format: ``{"ts", "time", "server", "service", "feature", "rpc", "kind", ...}`` where kind is
``unary`` (with ``request``, ``response`` or ``error``, ``ms``), or ``stream_open`` /
``stream_item`` / ``stream_end`` for server streams. Long strings are cut to ``MAX_TEXT``.

Installed by the server classes when ``SILA_TRAFFIC_LOG`` names a file (the console does that);
otherwise nothing is recorded and the servers behave exactly as before.
"""

from __future__ import annotations

import base64
import json
import os
import threading
import time
from contextlib import contextmanager
from datetime import datetime, timezone
from typing import Any, Iterator, Optional
from unittest import mock

import grpc
from google.protobuf.json_format import MessageToDict

MAX_TEXT = 1500  # characters kept per string field (a firmware trace JSON can be 100 kB)
ENV_VAR = "SILA_TRAFFIC_LOG"


class TrafficLog:
    """Append-only JSON-lines file, safe to write from gRPC's worker threads."""

    def __init__(self, path: str, server: str) -> None:
        self.path = path
        self.server = server
        self._lock = threading.Lock()
        os.makedirs(os.path.dirname(path) or ".", exist_ok=True)

    def write(self, entry: dict[str, Any]) -> None:
        now = time.time()
        line = {
            "ts": round(now, 4),
            "time": datetime.fromtimestamp(now, timezone.utc).isoformat(timespec="milliseconds"),
            "server": self.server,
            **entry,
        }
        text = json.dumps(line, default=str)
        with self._lock, open(self.path, "a", encoding="utf-8") as f:
            f.write(text + "\n")


def _cut(value: Any) -> Any:
    if isinstance(value, str):
        return value if len(value) <= MAX_TEXT else value[:MAX_TEXT] + f"... ({len(value)} chars)"
    if isinstance(value, dict):
        return {k: _cut(v) for k, v in value.items()}
    if isinstance(value, list):
        return [_cut(v) for v in value[:50]] + ([f"... ({len(value)} items)"] if len(value) > 50 else [])
    return value


def message_dict(message: Any) -> Any:
    """A protobuf message as a plain dict (SiLA wraps every value: ``{"VolumeUl": {"value": 50}}``)."""
    try:
        return _cut(MessageToDict(message, preserving_proto_field_name=True))
    except Exception:  # noqa: BLE001 - never let logging break a call
        return _cut(repr(message))


def decode_sila_error(details: Optional[str]) -> Any:
    """Turn the base64 ``SiLAError`` in an ABORTED status back into a dict, if it is one."""
    if not details:
        return None
    try:
        from sila2.framework.pb2 import SiLAFramework_pb2  # noqa: PLC0415

        error = SiLAFramework_pb2.SiLAError.FromString(base64.standard_b64decode(details))
        return _cut(MessageToDict(error, preserving_proto_field_name=True))
    except Exception:  # noqa: BLE001 - plain gRPC error text
        return _cut(details)


def split_method(method: str) -> tuple[str, str, str]:
    """``/sila2.org.x.liquidhandlerservice.v1.LiquidHandlerService/Transfer`` -> (service, feature, rpc)."""
    service, _, rpc = method.lstrip("/").rpartition("/")
    feature = service.rsplit(".", 1)[-1] if service else ""
    return service, feature, rpc


class _RecordingContext:
    """Forwards everything to the real context, but remembers what ``abort`` was called with."""

    def __init__(self, context: grpc.ServicerContext) -> None:
        self._context = context
        self.aborted: Optional[tuple[str, Optional[str]]] = None

    def abort(self, code: grpc.StatusCode, details: str = "") -> None:
        self.aborted = (code.name, details)
        self._context.abort(code, details)

    def __getattr__(self, name: str) -> Any:
        return getattr(self._context, name)


class TrafficInterceptor(grpc.ServerInterceptor):
    """Wraps unary-unary and unary-stream handlers (all SiLA uses, apart from binary upload)."""

    def __init__(self, log: TrafficLog) -> None:
        self.log = log

    def intercept_service(self, continuation, handler_call_details):  # noqa: ANN001 - grpc API
        handler = continuation(handler_call_details)
        if handler is None:
            return None
        service, feature, rpc = split_method(handler_call_details.method)
        base = {"service": service, "feature": feature, "rpc": rpc}

        if handler.unary_unary is not None:
            return grpc.unary_unary_rpc_method_handler(
                self._unary(handler.unary_unary, base),
                request_deserializer=handler.request_deserializer,
                response_serializer=handler.response_serializer,
            )
        if handler.unary_stream is not None:
            return grpc.unary_stream_rpc_method_handler(
                self._stream(handler.unary_stream, base),
                request_deserializer=handler.request_deserializer,
                response_serializer=handler.response_serializer,
            )
        self.log.write({**base, "kind": "other", "note": "client-streaming call, not recorded in detail"})
        return handler

    def _unary(self, behaviour, base: dict[str, Any]):
        def wrapped(request, context):
            recording = _RecordingContext(context)
            start = time.perf_counter()
            entry: dict[str, Any] = {**base, "kind": "unary", "request": message_dict(request)}
            try:
                response = behaviour(request, recording)
            except Exception as error:
                entry.update(self._failure(recording, error, start))
                self.log.write(entry)
                raise
            entry.update(ms=round((time.perf_counter() - start) * 1000, 2), status="OK",
                         response=message_dict(response))
            self.log.write(entry)
            return response

        return wrapped

    def _stream(self, behaviour, base: dict[str, Any]):
        def wrapped(request, context) -> Iterator[Any]:
            recording = _RecordingContext(context)
            start = time.perf_counter()
            stream_id = f"{base['rpc']}-{int(start * 1e6) % 10**9}"
            self.log.write({**base, "kind": "stream_open", "stream": stream_id, "request": message_dict(request)})
            count = 0
            try:
                for item in behaviour(request, recording):
                    count += 1
                    self.log.write({**base, "kind": "stream_item", "stream": stream_id, "n": count,
                                    "response": message_dict(item)})
                    yield item
            except Exception as error:
                self.log.write({**base, "kind": "stream_end", "stream": stream_id, "items": count,
                                **self._failure(recording, error, start)})
                raise
            self.log.write({**base, "kind": "stream_end", "stream": stream_id, "items": count, "status": "OK",
                            "ms": round((time.perf_counter() - start) * 1000, 2)})

        return wrapped

    @staticmethod
    def _failure(recording: _RecordingContext, error: BaseException, start: float) -> dict[str, Any]:
        out: dict[str, Any] = {"ms": round((time.perf_counter() - start) * 1000, 2)}
        if recording.aborted is not None:
            code, details = recording.aborted
            out.update(status=code, error=decode_sila_error(details))
        else:
            out.update(status="EXCEPTION", error=f"{type(error).__name__}: {error}")
        return out


@contextmanager
def recording_grpc_servers(server_name: str) -> Iterator[None]:
    """While active, ``grpc.server(...)`` gets a traffic interceptor (if ``SILA_TRAFFIC_LOG`` is set).

    ``SilaServer.__init__`` builds its gRPC server itself and has no interceptor parameter, so the
    server classes construct themselves inside this context instead. Nothing else is patched.
    """
    path = os.environ.get(ENV_VAR)
    if not path:
        yield
        return
    log = TrafficLog(path, server_name)
    original = grpc.server

    def server_with_traffic(*args: Any, **kwargs: Any):
        kwargs["interceptors"] = [*kwargs.get("interceptors", ()), TrafficInterceptor(log)]
        return original(*args, **kwargs)

    with mock.patch.object(grpc, "server", server_with_traffic):
        yield
