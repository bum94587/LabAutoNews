"""Run a workflow against SiLA 2 servers: one worker thread per device lane.

Scheduling rule (the whole algorithm): a lane's worker repeatedly picks the first step,
in file order, of its own device that is
  1. still pending,
  2. has all `depends_on` steps finished successfully, and
  3. is due: `start_after_t0_s` (workflow seconds, scaled to real seconds) has passed since t0.
It runs that step to completion (a device does one thing at a time), records it, and wakes
the other lanes. t0 is the moment the `marks_t0` step *finishes* (for the NADPH Transfer: after
the tip drop, a few tenths of a second after the dispense). If any step fails, no new step is
started anywhere; steps already running finish, the rest are marked "skipped". Every step has
a watchdog (`timeout_s` in the YAML, else the scheduler default): a call that does not return
in time fails the step and therefore the run.

SiLA 2 in one paragraph (sila2 0.14 dynamic client): `SilaClient(host, port, insecure=True)`
reads the server's feature definitions and exposes each feature as an attribute, e.g.
`client.LiquidHandlerService`. Calling an *unobservable* command returns its responses as a
NamedTuple straight away. Calling an *observable* command returns a command-instance handle
at once; the command keeps running on the server, we subscribe to its intermediate
responses (a stream that ends when the command ends) and then fetch the final responses.
Errors declared in the feature definition arrive as `DefinedExecutionError` (with the
FDL identifier, e.g. "LiquidHandlingError"), anything else as `UndefinedExecutionError`.

Usage (servers must already be running; run_demo.py does all of this for you):

    uv run python -m scheduler.scheduler [scheduler/workflow.yaml]
"""

from __future__ import annotations

import json
import sys
import threading
import time
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable

from sila2.framework import CommandExecutionNotFinished, DefinedExecutionError, UndefinedExecutionError

from scheduler.workflow import DEFAULT_WORKFLOW, Step, Workflow, load_workflow

MAX_TIMELINE_STRING = 600  # long responses (firmware trace, volumes) are cut in timeline.json


@dataclass
class StepRecord:
    """What happened to one step. Times in seconds from run start (monotonic clock)."""

    id: str
    device: str
    command: str
    params: dict[str, Any]
    depends_on: list[str]
    status: str = "pending"  # pending -> running -> succeeded | failed ; or skipped
    planned_start_s: float | None = None  # t0 + offset, for timed steps
    start_s: float | None = None
    end_s: float | None = None
    duration_s: float | None = None
    late_s: float | None = None  # how much later than planned the step really started
    start_wall: str | None = None
    end_wall: str | None = None
    responses: dict[str, Any] = field(default_factory=dict)
    intermediate_count: int = 0
    intermediates: list[dict[str, Any]] = field(default_factory=list)  # [{t_s, <field>: value}]
    error: str | None = None
    marks_t0: bool = False
    start_after_t0_s: float | None = None


def describe_error(ex: BaseException) -> str:
    """One-line description of an exception, naming the SiLA error type where there is one."""
    if isinstance(ex, DefinedExecutionError):
        return f"DefinedExecutionError {ex.identifier}: {ex.message}"
    if isinstance(ex, UndefinedExecutionError):
        return f"UndefinedExecutionError: {ex.message}"
    return f"{type(ex).__name__}: {ex}"


def as_plain_dict(responses: Any) -> dict[str, Any]:
    """SiLA responses come as NamedTuples; turn them into JSON-friendly dicts."""
    if responses is None:
        return {}
    if hasattr(responses, "_asdict"):
        responses = responses._asdict()
    if not isinstance(responses, dict):
        return {"value": _plain(responses)}
    return {k: _plain(v) for k, v in responses.items()}


def _plain(value: Any) -> Any:
    return value if isinstance(value, (str, int, float, bool)) or value is None else str(value)


def _now_wall() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="milliseconds")


class Scheduler:
    """Executes a `Workflow` given one SiLA feature object per device.

    `features` maps device name -> feature object, e.g.
    `{"lh": lh_client.LiquidHandlerService, "hhs": hhs_client.HeaterShakerService}`.
    Anything with the same call shape works, which is how tests/test_smoke.py uses fakes.
    """

    def __init__(
        self,
        workflow: Workflow,
        features: dict[str, Any],
        log: Callable[[str], None] = print,
        step_timeout_s: float = 120.0,
        intermediate_log_interval_s: float = 0.5,
    ):
        self.wf = workflow
        self.features = features
        self._log_sink = log
        self.step_timeout_s = step_timeout_s
        self.intermediate_log_interval_s = intermediate_log_interval_s
        self.records = {
            s.id: StepRecord(
                id=s.id,
                device=s.device,
                command=s.command,
                params=dict(s.params),
                depends_on=list(s.depends_on),
                marks_t0=s.marks_t0,
                start_after_t0_s=s.start_after_t0_s,
            )
            for s in workflow.steps
        }
        self.log_lines: list[str] = []
        self.t0_s: float | None = None
        self.failed = False
        self._cond = threading.Condition()  # guards records/t0/failed; lanes wait on it
        self._log_lock = threading.Lock()
        self._run_start = 0.0

    # ----------------------------------------------------------------- public

    def run(self) -> dict[str, Any]:
        """Run every lane to completion and return the timeline as a dict."""
        missing = {s.device for s in self.wf.steps} - set(self.features)
        if missing:
            raise ValueError(f"no SiLA feature given for devices {sorted(missing)}")
        self._run_start = time.monotonic()
        started_wall = _now_wall()
        self.log(f"run start: {self.wf.name} ({len(self.wf.steps)} steps, "
                 f"1 workflow-min = {self.wf.real_seconds_per_workflow_minute:g} s)")

        lanes = sorted({s.device for s in self.wf.steps})
        threads = [threading.Thread(target=self._lane, args=(d,), name=f"lane-{d}") for d in lanes]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        for rec in self.records.values():
            if rec.status == "pending":
                rec.status = "skipped"
        status = "failed" if self.failed else "succeeded"
        duration = self._now()
        self.log(f"run {status.upper()} after {duration:.2f} s")
        return {
            "workflow": self.wf.name,
            "real_seconds_per_workflow_minute": self.wf.real_seconds_per_workflow_minute,
            "run_status": status,
            "run_started_wall": started_wall,
            "run_ended_wall": _now_wall(),
            "duration_s": round(duration, 3),
            "t0_s": None if self.t0_s is None else round(self.t0_s, 3),
            "devices": {n: asdict(d) for n, d in self.wf.devices.items()},
            "steps": [self._timeline_entry(self.records[s.id]) for s in self.wf.steps],
        }

    def log(self, message: str, device: str = "", step_id: str = "") -> None:
        """Thread-safe live log line, prefixed with seconds since run start."""
        prefix = f"[{self._now():7.2f}s]"
        if device or step_id:
            prefix += f" {device:<3} | {step_id:<17} |"
        line = f"{prefix} {message}"
        with self._log_lock:
            self.log_lines.append(line)
            self._log_sink(line)

    # ------------------------------------------------------------ lane logic

    def _now(self) -> float:
        return time.monotonic() - self._run_start

    def _lane(self, device: str) -> None:
        """Worker loop for one device: wait for a runnable step, run it, repeat."""
        my_steps = [s for s in self.wf.steps if s.device == device]
        while True:
            with self._cond:
                step = self._wait_for_next_step(my_steps)
                if step is None:
                    return
            status, responses, error = self._execute(step)
            end_s, end_wall = round(self._now(), 3), _now_wall()
            # Status, end time and t0 change together under the lock, so another lane never sees
            # the t0 step "succeeded" while t0 is still unset.
            with self._cond:
                rec = self.records[step.id]
                rec.status, rec.responses, rec.error = status, responses, error
                rec.end_s, rec.end_wall = end_s, end_wall
                rec.duration_s = round(end_s - rec.start_s, 3)
                if status == "failed":
                    self.failed = True
                elif step.marks_t0:
                    self.t0_s = end_s
                self._cond.notify_all()
            self._log_outcome(rec)

    def _wait_for_next_step(self, my_steps: list[Step]) -> Step | None:
        """Block (holding the condition) until a step is runnable; None when the lane is done."""
        while True:
            if self.failed:
                return None
            pending = [s for s in my_steps if self.records[s.id].status == "pending"]
            if not pending:
                return None
            step, wait_s = self._pick_ready(pending)
            if step is not None:
                self.records[step.id].status = "running"
                return step
            self._cond.wait(timeout=wait_s)  # woken by another lane, or when a timed step is due

    def _pick_ready(self, pending: list[Step]) -> tuple[Step | None, float | None]:
        """First runnable step in file order, else (None, seconds until a timed step is due)."""
        wait_s: float | None = None
        for step in pending:
            if any(self.records[d].status != "succeeded" for d in step.depends_on):
                continue
            if step.start_after_t0_s is not None:
                if self.t0_s is None:  # cannot happen (t0 step is an ancestor), but never crash
                    continue
                due = self.t0_s + self.wf.real_delay(step.start_after_t0_s)
                self.records[step.id].planned_start_s = round(due, 3)
                remaining = due - self._now()
                if remaining > 0:
                    wait_s = remaining if wait_s is None else min(wait_s, remaining)
                    continue
            return step, None
        return None, wait_s

    # -------------------------------------------------------- SiLA execution

    def _execute(self, step: Step) -> tuple[str, dict[str, Any], str | None]:
        """Call one SiLA command under a watchdog; return (status, responses, error). Never raises.

        Only start time and intermediate responses are written to the record here; the outcome
        is written by the lane under the lock (see `_lane`).
        """
        rec = self.records[step.id]
        rec.start_s = round(self._now(), 3)
        rec.start_wall = _now_wall()
        if rec.planned_start_s is not None:
            rec.late_s = round(rec.start_s - rec.planned_start_s, 3)
        params = ", ".join(f"{k}={v}" for k, v in step.params.items())
        timing = ""
        if step.start_after_t0_s is not None:
            timing = f"  [due t0+{step.start_after_t0_s / 60:g} min, late by {rec.late_s:+.2f} s]"
        self.log(f"START {step.command}({params}){timing}", step.device, step.id)

        def call() -> Any:
            command = getattr(self.features[step.device], step.command)
            result = command(**step.params)
            if hasattr(result, "get_responses"):  # observable command: we got an instance handle
                result = self._follow_observable(rec, result)
            return result

        timeout_s = step.timeout_s or self.step_timeout_s
        try:
            return "succeeded", as_plain_dict(self._with_watchdog(call, timeout_s)), None
        except Exception as ex:  # noqa: BLE001 - any failure fails the step, and the run
            return "failed", {}, describe_error(ex)

    @staticmethod
    def _with_watchdog(func: Callable[[], Any], timeout_s: float) -> Any:
        """Run func in a helper thread; raise TimeoutError if it has not returned in time.

        A timed-out call keeps its (daemon) thread; the run fails and stops scheduling, and
        run_demo.py stops the servers, which ends any call still waiting on them.
        """
        box: dict[str, Any] = {}

        def target() -> None:
            try:
                box["result"] = func()
            except BaseException as ex:  # noqa: BLE001 - handed back to the caller below
                box["error"] = ex

        worker = threading.Thread(target=target, daemon=True, name="sila-call")
        worker.start()
        worker.join(timeout_s)
        if worker.is_alive():
            raise TimeoutError(f"no result within {timeout_s:g} s (step watchdog)")
        if "error" in box:
            raise box["error"]
        return box["result"]

    def _log_outcome(self, rec: StepRecord) -> None:
        if rec.status == "succeeded":
            self.log(f"DONE  in {rec.duration_s:.2f} s -> {self._short(rec.responses)}", rec.device, rec.id)
            if rec.marks_t0:
                self.log("t0 set (reaction started); timed steps now count from here", rec.device, rec.id)
        else:
            self.log(f"FAIL  after {rec.duration_s:.2f} s: {rec.error}", rec.device, rec.id)
            self.log("run marked FAILED: no new steps will be started", rec.device, rec.id)

    def _follow_observable(self, rec: StepRecord, instance: Any) -> Any:
        """Stream intermediate responses into the log, then return the final responses."""
        last_logged = -1e9
        if hasattr(instance, "subscribe_to_intermediate_responses"):
            subscription = instance.subscribe_to_intermediate_responses()
            try:
                for item in subscription:  # ends when the command finishes on the server
                    now = self._now()
                    values = as_plain_dict(item)
                    rec.intermediates.append({"t_s": round(now, 3), **values})
                    rec.intermediate_count += 1
                    # Text steps are always shown; numeric streams (temperatures) are throttled.
                    is_text = any(isinstance(v, str) for v in values.values())
                    if is_text or now - last_logged >= self.intermediate_log_interval_s:
                        self.log(f"  ... {self._short(values)}", rec.device, rec.id)
                        last_logged = now
            finally:
                subscription.cancel()
        try:
            return self._wait_for_responses(instance)
        finally:
            if hasattr(instance, "cancel_execution_info_subscription"):
                instance.cancel_execution_info_subscription()

    @staticmethod
    def _wait_for_responses(instance: Any) -> Any:
        """get_responses() raises CommandExecutionNotFinished until the server is done.

        (The step watchdog bounds this loop.)
        """
        while True:
            try:
                return instance.get_responses()
            except CommandExecutionNotFinished:
                time.sleep(0.05)

    # --------------------------------------------------------------- helpers

    @staticmethod
    def _short(values: dict[str, Any], limit: int = 90) -> str:
        text = ", ".join(f"{k}={v:.2f}" if isinstance(v, float) else f"{k}={v}" for k, v in values.items())
        return text if len(text) <= limit else text[: limit - 3] + "..."

    @staticmethod
    def _timeline_entry(rec: StepRecord) -> dict[str, Any]:
        entry = asdict(rec)
        for key, value in entry["responses"].items():
            if isinstance(value, str) and len(value) > MAX_TIMELINE_STRING:
                entry["responses"][key] = (
                    value[:MAX_TIMELINE_STRING] + f"... [{len(value)} chars; full data in results/*.json]"
                )
        return entry


def connect_features(wf: Workflow) -> tuple[dict[str, Any], list[Any]]:
    """Open a SilaClient per device; return ({device: feature object}, [clients])."""
    from sila2.client import SilaClient  # local import: tests with fakes never need a server

    features, clients = {}, []
    for name, dev in wf.devices.items():
        client = SilaClient(dev.host, dev.port, insecure=True)
        clients.append(client)
        features[name] = getattr(client, dev.feature)
    return features, clients


def main(argv: list[str]) -> int:
    """Run a workflow against already-running servers and write results/timeline.json."""
    wf = load_workflow(argv[0] if argv else DEFAULT_WORKFLOW)
    features, clients = connect_features(wf)
    try:
        timeline = Scheduler(wf, features).run()
    finally:
        for c in clients:
            c.close()
    out = Path(__file__).resolve().parent.parent / "results" / "timeline.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(timeline, indent=2))
    print(f"wrote {out}")
    return 0 if timeline["run_status"] == "succeeded" else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
