"""Control the SiLA 2 twin servers from the command line. Every command prints ONE JSON object.

Run from the SiLA2 folder::

    uv run python -m console.ctl status
    uv run python -m console.ctl start all --viewer --motion-scale 0.5 --initialize
    uv run python -m console.ctl features lh
    uv run python -m console.ctl call lh LiquidHandlerService Initialize
    uv run python -m console.ctl call lh LiquidHandlerService Transfer \\
        --params '{"SourcePlate": "compounds", "SourceColumn": 1, "TargetPlate": "reaction", "TargetColumn": 1, "VolumeUl": 50}'
    uv run python -m console.ctl call hhs HeaterShakerService CurrentTemperature
    uv run python -m console.ctl methods
    uv run python -m console.ctl run workflow --time-scale 4
    uv run python -m console.ctl runs
    uv run python -m console.ctl stop all

Servers started here run in the background (their own session, so they outlive the caller) and
are found again through ``runtime/servers/<name>.json``. Unlike ``run_demo.py``, which starts and
stops its own servers for one run, these stay up until ``stop``, so methods, manual calls and the
3D viewer all talk to the same twin. Each server records its SiLA traffic to
``runtime/traffic/sila_<name>.jsonl`` and the STAR twin its firmware commands to
``runtime/traffic/firmware_lh.jsonl`` (see ``console/traffic.py``).
"""

from __future__ import annotations

import argparse
import json
import os
import re
import signal
import socket
import subprocess
import sys
import threading
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from console import paths

SERVERS: dict[str, dict[str, Any]] = {
    "lh": {
        "module": "lh_twin",
        "port": 50052,
        "feature": "LiquidHandlerService",
        "title": "Hamilton STAR twin",
        "what": "PyLabRobot v1 STAR on its firmware-level simulator",
    },
    "hhs": {
        "module": "hhs_twin",
        "port": 50053,
        "feature": "HeaterShakerService",
        "title": "Heater-shaker twin",
        "what": "first-order thermal model, accelerated time",
    },
}
HOST = "127.0.0.1"
DEFAULT_METHOD = paths.SILA2_DIR / "scheduler" / "workflow.yaml"


# ------------------------------------------------------------------------------------------------
# small helpers
# ------------------------------------------------------------------------------------------------


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def out(payload: dict[str, Any]) -> None:
    print(json.dumps(payload, default=str))


def fail(message: str, **extra: Any) -> dict[str, Any]:
    return {"ok": False, "error": message, **extra}


def names_from(arg: str) -> list[str]:
    if arg == "all":
        return list(SERVERS)
    if arg not in SERVERS:
        raise SystemExit(f"unknown server '{arg}' (use {', '.join(SERVERS)} or all)")
    return [arg]


def port_open(port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(0.3)
        return sock.connect_ex((HOST, port)) == 0


def pid_alive(pid: int | None, module: str) -> bool:
    """True if `pid` runs and is our server (its command line names the module)."""
    if not pid:
        return False
    try:
        cmdline = Path(f"/proc/{pid}/cmdline").read_bytes().replace(b"\0", b" ").decode()
    except OSError:
        return False
    return f"-m {module}" in cmdline


def state_file(name: str) -> Path:
    return paths.SERVERS_DIR / f"{name}.json"


def viewer_file() -> Path:
    return paths.SERVERS_DIR / "lh_viewer.json"


def read_json(path: Path) -> dict[str, Any] | None:
    try:
        return json.loads(path.read_text())
    except (OSError, ValueError):
        return None


def tail(path: Path, lines: int = 40) -> list[str]:
    try:
        return path.read_text(errors="replace").splitlines()[-lines:]
    except OSError:
        return []


# ------------------------------------------------------------------------------------------------
# server status / start / stop
# ------------------------------------------------------------------------------------------------


def server_status(name: str) -> dict[str, Any]:
    spec = SERVERS[name]
    state = read_json(state_file(name)) or {}
    running = pid_alive(state.get("pid"), spec["module"])
    port = state.get("port", spec["port"])
    info: dict[str, Any] = {
        "name": name,
        "title": spec["title"],
        "what": spec["what"],
        "feature": spec["feature"],
        "port": port,
        "running": running,
        "pid": state.get("pid") if running else None,
        "started": state.get("started") if running else None,
        "uuid": state.get("uuid") if running else None,
        "options": state.get("options", {}),
        "stale_state": bool(state) and not running,
        "port_busy_elsewhere": (not running) and port_open(port),
        "log": str(paths.LOGS_DIR / f"{spec['module']}.log"),
        "traffic": str(paths.sila_traffic_file(name)),
    }
    if name == "lh":
        info["firmware_log"] = str(paths.firmware_traffic_file())
        viewer = read_json(viewer_file()) if running else None
        info["viewer"] = viewer
    return info


def wait_until_ready(name: str, server_uuid: str, pid: int, timeout_s: float = 90.0) -> None:
    from sila2.client import SilaClient  # noqa: PLC0415

    spec = SERVERS[name]
    deadline = time.monotonic() + timeout_s
    last = "no attempt"
    while time.monotonic() < deadline:
        if not pid_alive(pid, spec["module"]):
            log = "\n".join(tail(paths.LOGS_DIR / f"{spec['module']}.log", 15))
            raise RuntimeError(f"{spec['module']} exited during start-up:\n{log}")
        try:
            client = SilaClient(HOST, spec["port"], insecure=True)
        except Exception as ex:  # noqa: BLE001 - not up yet
            last = f"{type(ex).__name__}: {ex}"
            time.sleep(0.4)
            continue
        try:
            answered = str(client.SiLAService.ServerUUID.get())
            if answered != server_uuid:
                raise RuntimeError(f"port {spec['port']} is answered by another SiLA server ({answered})")
            if hasattr(client, spec["feature"]):
                return
        finally:
            client.close()
        time.sleep(0.4)
    raise TimeoutError(f"{spec['module']} not ready after {timeout_s:g} s ({last})")


def start_one(name: str, viewer: bool, motion_scale: float | None) -> dict[str, Any]:
    spec = SERVERS[name]
    status = server_status(name)
    if status["running"]:
        return {**status, "note": "already running"}
    if status["port_busy_elsewhere"]:
        raise RuntimeError(f"port {spec['port']} is in use by another process; stop it first")

    paths.ensure_dirs()
    server_uuid = str(uuid.uuid4())
    env = dict(os.environ)
    env["PYTHONPATH"] = os.pathsep.join(filter(None, [str(paths.SILA2_DIR), env.get("PYTHONPATH")]))
    env["SILA_TRAFFIC_LOG"] = str(paths.sila_traffic_file(name))
    options: dict[str, Any] = {}
    if name == "lh":
        scale = 0.1 if motion_scale is None else motion_scale
        env["LH_TWIN_MOTION_SCALE"] = str(scale)
        env["LH_TWIN_FIRMWARE_LOG"] = str(paths.firmware_traffic_file())
        options["motion_scale"] = scale
        options["viewer"] = viewer
        viewer_file().unlink(missing_ok=True)
        if viewer:
            env["LH_TWIN_VIEWER"] = "1"
            env["LH_TWIN_VIEWER_FILE"] = str(viewer_file())
    log_path = paths.LOGS_DIR / f"{spec['module']}.log"
    with log_path.open("w") as log:
        proc = subprocess.Popen(
            [sys.executable, "-m", spec["module"], "--ip-address", HOST, "--port", str(spec["port"]),
             "--server-uuid", server_uuid, "--insecure", "--disable-discovery"],
            stdout=log, stderr=subprocess.STDOUT, stdin=subprocess.DEVNULL,
            cwd=paths.SILA2_DIR, env=env, start_new_session=True,
        )
    state = {"pid": proc.pid, "port": spec["port"], "uuid": server_uuid, "started": now_iso(), "options": options}
    state_file(name).write_text(json.dumps(state, indent=2))
    wait_until_ready(name, server_uuid, proc.pid)
    return server_status(name)


def stop_one(name: str) -> dict[str, Any]:
    spec = SERVERS[name]
    state = read_json(state_file(name)) or {}
    pid = state.get("pid")
    stopped = False
    if pid_alive(pid, spec["module"]):
        os.kill(pid, signal.SIGTERM)
        for _ in range(100):
            if not pid_alive(pid, spec["module"]):
                break
            time.sleep(0.1)
        else:
            os.kill(pid, signal.SIGKILL)
        stopped = True
    state_file(name).unlink(missing_ok=True)
    if name == "lh":
        viewer_file().unlink(missing_ok=True)
    return {"name": name, "stopped": stopped}


# ------------------------------------------------------------------------------------------------
# introspection and calls
# ------------------------------------------------------------------------------------------------


def client_for(name: str):
    from sila2.client import SilaClient  # noqa: PLC0415

    status = server_status(name)
    if not status["running"]:
        raise RuntimeError(f"the {SERVERS[name]['title']} server is not running (start it first)")
    return SilaClient(HOST, status["port"], insecure=True)


def type_info(data_type: Any) -> dict[str, Any]:
    """A SiLA data type as {type, base, constraints} (Constrained types name their base type)."""
    kind = type(data_type).__name__
    info: dict[str, Any] = {"type": kind}
    if kind == "Constrained":
        base = type_info(data_type.base_type)
        info.update(type=base["type"], constrained=True, constraints=[constraint_text(c) for c in data_type.constraints])
    elif kind == "List":
        info["element"] = type_info(getattr(data_type, "element_type", None))
    return info


def constraint_text(constraint: Any) -> str:
    name = type(constraint).__name__
    value = getattr(constraint, "value", None)
    if value is None:
        values = getattr(constraint, "values", None)
        return f"{name} {values}" if values is not None else name
    return f"{name} {value}"


def field_info(field: Any) -> dict[str, Any]:
    return {
        "identifier": field._identifier,
        "display_name": field._display_name,
        "description": " ".join(str(field._description).split()),
        **type_info(field.data_type),
    }


def error_names(errors: Any) -> list[str]:
    """Defined execution error identifiers, from either a dict (feature) or a list of nodes (command)."""
    if not errors:
        return []
    items = errors.values() if isinstance(errors, dict) else errors
    return sorted({str(getattr(e, "_identifier", getattr(e, "identifier", e))) for e in items})


def describe_feature(feature: Any) -> dict[str, Any]:
    commands = []
    for observable, table in ((False, feature._unobservable_commands), (True, feature._observable_commands)):
        for ident, cmd in table.items():
            commands.append({
                "identifier": ident,
                "display_name": cmd._display_name,
                "description": " ".join(str(cmd._description).split()),
                "observable": observable,
                "parameters": [field_info(f) for f in cmd.parameters.fields],
                "responses": [field_info(f) for f in cmd.responses.fields],
                "intermediate": [field_info(f) for f in getattr(cmd, "intermediate_responses", None).fields]
                if observable and getattr(cmd, "intermediate_responses", None) is not None else [],
                "errors": error_names(getattr(cmd, "defined_execution_errors", None)),
            })
    properties = []
    for observable, table in ((False, feature._unobservable_properties), (True, feature._observable_properties)):
        for ident, prop in table.items():
            properties.append({
                "identifier": ident,
                "display_name": prop._display_name,
                "description": " ".join(str(prop._description).split()),
                "observable": observable,
                **type_info(prop.data_type),
            })
    return {
        "identifier": feature._identifier,
        "display_name": feature._display_name,
        "description": " ".join(str(feature._description).split()),
        "fully_qualified_identifier": str(feature.fully_qualified_identifier),
        "commands": commands,
        "properties": properties,
        "errors": error_names(getattr(feature, "defined_execution_errors", None)),
    }


def cmd_features(name: str) -> dict[str, Any]:
    from sila2.framework import Feature  # noqa: PLC0415

    client = client_for(name)
    try:
        features = []
        for fqi in client.SiLAService.ImplementedFeatures.get():
            xml = client.SiLAService.GetFeatureDefinition(FeatureIdentifier=fqi).FeatureDefinition
            features.append(describe_feature(Feature(xml)))
        return {"ok": True, "server": name, "uuid": str(client.SiLAService.ServerUUID.get()),
                "server_name": client.SiLAService.ServerName.get(), "features": features}
    finally:
        client.close()


def plain(value: Any) -> Any:
    if hasattr(value, "_asdict"):
        return {k: plain(v) for k, v in value._asdict().items()}
    if isinstance(value, dict):
        return {k: plain(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [plain(v) for v in value]
    if isinstance(value, (str, int, float, bool)) or value is None:
        return value
    return str(value)


def error_info(ex: BaseException) -> dict[str, Any]:
    from sila2.framework import (  # noqa: PLC0415
        DefinedExecutionError,
        UndefinedExecutionError,
        ValidationError,
    )

    if isinstance(ex, DefinedExecutionError):
        return {"kind": "DefinedExecutionError", "identifier": ex.identifier, "message": ex.message}
    if isinstance(ex, UndefinedExecutionError):
        return {"kind": "UndefinedExecutionError", "message": ex.message}
    if isinstance(ex, ValidationError):
        return {"kind": "ValidationError", "parameter": str(getattr(ex, "parameter_fully_qualified_identifier", "")),
                "message": getattr(ex, "message", str(ex))}
    return {"kind": type(ex).__name__, "message": str(ex)}


def cmd_call(name: str, feature: str, element: str, params: dict[str, Any], timeout_s: float) -> dict[str, Any]:
    from sila2.framework import CommandExecutionNotFinished  # noqa: PLC0415

    client = client_for(name)
    start = time.perf_counter()
    try:
        target = getattr(getattr(client, feature), element)
        kind = type(target).__name__
        intermediates: list[Any] = []
        if kind == "ClientUnobservableCommand":
            result = target(**params)
        elif kind == "ClientObservableCommand":
            instance = target(**params)
            if hasattr(instance, "subscribe_to_intermediate_responses"):
                subscription = instance.subscribe_to_intermediate_responses()

                def collect() -> None:
                    try:
                        for item in subscription:
                            intermediates.append({"t_ms": round((time.perf_counter() - start) * 1000), **plain(item)})
                    except Exception:  # noqa: BLE001 - the stream ends when the command does
                        pass

                reader = threading.Thread(target=collect, daemon=True)
                reader.start()
            deadline = time.monotonic() + timeout_s
            while True:
                try:
                    result = instance.get_responses()
                    break
                except CommandExecutionNotFinished:
                    if time.monotonic() > deadline:
                        raise TimeoutError(f"no result within {timeout_s:g} s") from None
                    time.sleep(0.05)
            if hasattr(instance, "subscribe_to_intermediate_responses"):
                reader.join(timeout=2)
                subscription.cancel()
            if hasattr(instance, "cancel_execution_info_subscription"):
                instance.cancel_execution_info_subscription()
        elif kind in ("ClientUnobservableProperty", "ClientObservableProperty"):
            result = target.get()
        else:
            return fail(f"{feature}.{element} is a {kind}, which this console cannot call")
        return {"ok": True, "server": name, "feature": feature, "element": element, "kind": kind,
                "params": params, "result": plain(result), "intermediates": intermediates,
                "ms": round((time.perf_counter() - start) * 1000, 1)}
    except AttributeError as ex:
        return fail(f"no {feature}.{element} on the {name} server ({ex})")
    except Exception as ex:  # noqa: BLE001 - reported to the caller, by SiLA error type
        return {"ok": False, "server": name, "feature": feature, "element": element, "params": params,
                "error": error_info(ex), "ms": round((time.perf_counter() - start) * 1000, 1)}
    finally:
        client.close()


def cmd_snapshot() -> dict[str, Any]:
    """Everything the live panel shows, in one go: STAR status and plates, heater-shaker state."""
    snap: dict[str, Any] = {"ok": True, "time": now_iso()}
    plates = ("compounds", "nadph", "reaction", "quench")
    if server_status("lh")["running"]:
        lh: dict[str, Any] = {}
        client = client_for("lh")
        try:
            feature = client.LiquidHandlerService
            lh["status"] = feature.Status.get()
            volumes, problems = {}, []
            for plate in plates:
                try:
                    volumes[plate] = json.loads(feature.GetWellVolumes(Plate=plate).VolumesJson)
                except Exception as ex:  # noqa: BLE001 - e.g. NotInitialized
                    problems.append(error_info(ex).get("message", str(ex)))
            lh["volumes"] = volumes
            if problems:
                lh["volumes_error"] = problems[0]
            try:
                layout = json.loads(feature.GetDeckLayout().DeckLayoutJson)
                lh["tip_columns_used"] = layout.get("poc_layout", {}).get("tip_columns_used", [])
            except Exception:  # noqa: BLE001
                lh["tip_columns_used"] = None
        finally:
            client.close()
        snap["lh"] = lh
    if server_status("hhs")["running"]:
        client = client_for("hhs")
        try:
            feature = client.HeaterShakerService
            snap["hhs"] = {"temperature": feature.CurrentTemperature.get(), "speed": feature.ShakingSpeed.get()}
        finally:
            client.close()
    return snap


# ------------------------------------------------------------------------------------------------
# methods (workflow files) and runs
# ------------------------------------------------------------------------------------------------


def method_files() -> list[Path]:
    extra = sorted(paths.METHODS_DIR.glob("*.yaml")) if paths.METHODS_DIR.is_dir() else []
    return [DEFAULT_METHOD, *extra]


def method_id(path: Path) -> str:
    return "workflow" if path == DEFAULT_METHOD else path.stem


def method_path(ident: str) -> Path:
    for path in method_files():
        if method_id(path) == ident or str(path) == ident:
            return path
    candidate = Path(ident)
    if candidate.is_file():
        return candidate
    raise SystemExit(f"unknown method '{ident}' (see: methods)")


def header_comment(path: Path) -> str:
    """The comment block at the top of a method file: its description."""
    lines = []
    for line in path.read_text().splitlines():
        if not line.startswith("#"):
            break
        lines.append(line[1:].strip())
    return "\n".join(lines).strip()


def cmd_methods() -> dict[str, Any]:
    from scheduler.workflow import load_workflow  # noqa: PLC0415

    methods = []
    for path in method_files():
        entry: dict[str, Any] = {"id": method_id(path), "path": str(path),
                                 "file": str(path.relative_to(paths.SILA2_DIR)), "description": header_comment(path)}
        try:
            wf = load_workflow(path)
            entry.update(
                name=wf.name,
                time_scale=wf.real_seconds_per_workflow_minute,
                devices={k: {"port": d.port, "feature": d.feature, "description": d.description}
                         for k, d in wf.devices.items()},
                steps=[{"id": s.id, "device": s.device, "command": s.command, "params": s.params,
                        "depends_on": list(s.depends_on), "start_after_t0_s": s.start_after_t0_s,
                        "marks_t0": s.marks_t0} for s in wf.steps],
            )
        except Exception as ex:  # noqa: BLE001 - show a broken method rather than hide it
            entry["error"] = f"{type(ex).__name__}: {ex}"
        methods.append(entry)
    return {"ok": True, "methods": methods}


def run_dir(run_id: str) -> Path:
    if not re.fullmatch(r"[A-Za-z0-9_.-]+", run_id):
        raise SystemExit("bad run id")
    return paths.RUNS_DIR / run_id


def write_status(folder: Path, **values: Any) -> None:
    status = read_json(folder / "status.json") or {}
    status.update(values)
    (folder / "status.json").write_text(json.dumps(status, indent=2, default=str))


def cmd_run(method: str, time_scale: float | None) -> dict[str, Any]:
    path = method_path(method)
    down = [n for n in SERVERS if not server_status(n)["running"]]
    if down:
        return fail(f"start the servers first (not running: {', '.join(down)})")
    active = [r for r in list_runs(5) if r.get("state") in ("starting", "running") and pid_alive(r.get("pid"), "console.ctl")]
    if active:
        return fail(f"run {active[0]['run_id']} is still going")
    paths.ensure_dirs()
    run_id = datetime.now().strftime("%Y%m%d-%H%M%S") + "_" + method_id(path)
    folder = run_dir(run_id)
    folder.mkdir(parents=True)
    write_status(folder, run_id=run_id, method=method_id(path), method_file=str(path), state="starting",
                 created=now_iso(), time_scale=time_scale)
    args = [sys.executable, "-m", "console.ctl", "_worker", run_id, str(path)]
    if time_scale:
        args += ["--time-scale", str(time_scale)]
    env = dict(os.environ)
    env["PYTHONPATH"] = os.pathsep.join(filter(None, [str(paths.SILA2_DIR), env.get("PYTHONPATH")]))
    with (folder / "live.log").open("w") as log:
        proc = subprocess.Popen(args, stdout=log, stderr=subprocess.STDOUT, stdin=subprocess.DEVNULL,
                                cwd=paths.SILA2_DIR, env=env, start_new_session=True)
    write_status(folder, pid=proc.pid)
    return {"ok": True, "run_id": run_id, "folder": str(folder)}


def worker(run_id: str, method_file: str, time_scale: float | None) -> int:
    """The background half of `run`: drive the method against the running servers."""
    import dataclasses  # noqa: PLC0415

    from sila2.client import SilaClient  # noqa: PLC0415

    import run_demo  # noqa: PLC0415 - reuse its result collection and report writing
    from scheduler.scheduler import Scheduler  # noqa: PLC0415
    from scheduler.workflow import Workflow, load_workflow  # noqa: PLC0415

    folder = run_dir(run_id)
    clients = []
    try:
        wf = load_workflow(method_file)
        devices = {}
        for name, dev in wf.devices.items():
            port = server_status(name)["port"] if name in SERVERS else dev.port
            devices[name] = dataclasses.replace(dev, host=HOST, port=port)
        wf = Workflow(wf.name, time_scale or wf.real_seconds_per_workflow_minute, devices, wf.steps)
        features = {}
        for name, dev in wf.devices.items():
            client = SilaClient(dev.host, dev.port, insecure=True)
            clients.append(client)
            features[name] = getattr(client, dev.feature)
        trace_start = 0
        if "lh" in features:
            try:
                trace_start = len(json.loads(features["lh"].GetFirmwareTrace(SinceIndex=0).TraceJson))
            except Exception:  # noqa: BLE001 - before Initialize there is no trace yet
                trace_start = 0
        write_status(folder, state="running", started=now_iso(), name=wf.name,
                     time_scale=wf.real_seconds_per_workflow_minute, steps_total=len(wf.steps))
        print(f"method {wf.name} ({len(wf.steps)} steps, 1 workflow minute = "
              f"{wf.real_seconds_per_workflow_minute:g} s)", flush=True)
        scheduler = Scheduler(wf, features, log=lambda line: print(line, flush=True))
        timeline = scheduler.run()
        trace, volumes, info = [], {}, ""
        if "lh" in features:
            trace, volumes, info = run_demo.collect_lh_state(features["lh"])
            trace = [t for t in trace if t.get("index", 0) >= trace_start]
        run_demo.write_results(folder, timeline, trace, volumes, info, scheduler.log_lines)
        steps = timeline["steps"]
        ok = sum(s["status"] == "succeeded" for s in steps)
        write_status(folder, state="finished", finished=now_iso(), run_status=timeline["run_status"],
                     steps_ok=ok, steps_total=len(steps), duration_s=timeline.get("duration_s"),
                     firmware_commands=len(trace))
        print(f"run {timeline['run_status']}: {ok}/{len(steps)} steps, {len(trace)} firmware commands", flush=True)
        return 0 if timeline["run_status"] == "succeeded" else 1
    except Exception as ex:  # noqa: BLE001 - recorded for the console
        write_status(folder, state="error", finished=now_iso(), error=f"{type(ex).__name__}: {ex}")
        print(f"ERROR: {type(ex).__name__}: {ex}", flush=True)
        return 2
    finally:
        for client in clients:
            client.close()


def list_runs(limit: int = 20) -> list[dict[str, Any]]:
    if not paths.RUNS_DIR.is_dir():
        return []
    runs = []
    for folder in sorted(paths.RUNS_DIR.iterdir(), reverse=True)[:limit]:
        status = read_json(folder / "status.json")
        if status:
            if status.get("state") in ("starting", "running") and not pid_alive(status.get("pid"), "console.ctl"):
                status["state"] = "died"
            runs.append({**status, "folder": str(folder)})
    return runs


# ------------------------------------------------------------------------------------------------
# entry point
# ------------------------------------------------------------------------------------------------


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="python -m console.ctl", description=__doc__.splitlines()[0])
    sub = p.add_subparsers(dest="command", required=True)
    sub.add_parser("status", help="both servers, the 3D viewer and where the runtime files are")
    s = sub.add_parser("start", help="start server(s) in the background")
    s.add_argument("which", choices=[*SERVERS, "all"])
    s.add_argument("--viewer", action="store_true", help="STAR twin: serve PyLabRobot's 3D viewer")
    s.add_argument("--motion-scale", type=float, default=None,
                   help="STAR twin: 1 = real STAR speed, 0.1 = 10x faster (default), 0 = instant")
    s.add_argument("--initialize", action="store_true", help="STAR twin: call Initialize once it is up")
    s = sub.add_parser("stop", help="stop server(s)")
    s.add_argument("which", choices=[*SERVERS, "all"])
    s = sub.add_parser("features", help="the features, commands and properties a server offers")
    s.add_argument("which", choices=list(SERVERS))
    s = sub.add_parser("call", help="call one command or read one property")
    s.add_argument("which", choices=list(SERVERS))
    s.add_argument("feature")
    s.add_argument("element")
    s.add_argument("--params", default="{}", help="JSON object of parameters")
    s.add_argument("--timeout", type=float, default=180.0, help="seconds to wait for an observable command")
    sub.add_parser("snapshot", help="STAR status and plate volumes, heater-shaker temperature and speed")
    sub.add_parser("methods", help="the method files and their steps")
    s = sub.add_parser("run", help="run a method in the background against the running servers")
    s.add_argument("method", help="method id (see: methods) or a YAML path")
    s.add_argument("--time-scale", type=float, default=None, help="real seconds per workflow minute")
    s = sub.add_parser("runs", help="recent runs, newest first")
    s.add_argument("--limit", type=int, default=20)
    sub.add_parser("clear-traffic", help="empty the traffic files")
    s = sub.add_parser("_worker")  # internal: the background half of `run`
    s.add_argument("run_id")
    s.add_argument("method_file")
    s.add_argument("--time-scale", type=float, default=None)
    a = p.parse_args(argv)

    if a.command == "_worker":
        return worker(a.run_id, a.method_file, a.time_scale)
    try:
        if a.command == "status":
            result = {"ok": True, "servers": {n: server_status(n) for n in SERVERS},
                      "sila2_dir": str(paths.SILA2_DIR), "runtime": str(paths.RUNTIME)}
        elif a.command == "start":
            started = {}
            for name in names_from(a.which):
                started[name] = start_one(name, viewer=a.viewer, motion_scale=a.motion_scale)
            result = {"ok": True, "servers": started}
            if a.initialize and "lh" in started:
                result["initialize"] = cmd_call("lh", "LiquidHandlerService", "Initialize", {}, 120)
                result["servers"]["lh"] = server_status("lh")
        elif a.command == "stop":
            result = {"ok": True, "stopped": [stop_one(n) for n in names_from(a.which)]}
        elif a.command == "features":
            result = cmd_features(a.which)
        elif a.command == "call":
            params = json.loads(a.params or "{}")
            if not isinstance(params, dict):
                raise ValueError("--params must be a JSON object")
            result = cmd_call(a.which, a.feature, a.element, params, a.timeout)
        elif a.command == "snapshot":
            result = cmd_snapshot()
        elif a.command == "methods":
            result = cmd_methods()
        elif a.command == "run":
            result = cmd_run(a.method, a.time_scale)
        elif a.command == "runs":
            result = {"ok": True, "runs": list_runs(a.limit)}
        elif a.command == "clear-traffic":
            paths.ensure_dirs()
            cleared = []
            for f in paths.TRAFFIC_DIR.glob("*.jsonl"):
                f.write_text("")
                cleared.append(f.name)
            result = {"ok": True, "cleared": cleared}
        else:  # pragma: no cover - argparse guards this
            result = fail(f"unknown command {a.command}")
    except SystemExit as ex:
        result = fail(str(ex))
    except Exception as ex:  # noqa: BLE001 - JSON out, always
        result = fail(f"{type(ex).__name__}: {ex}")
    out(result)
    return 0 if result.get("ok") else 1


if __name__ == "__main__":
    sys.exit(main())
