"""Smoke tests for the scheduler and the end-to-end demo.

    uv run python tests/test_smoke.py          # plain runner, no pytest needed
    uv run --with pytest pytest -q tests       # or with pytest

1-3 use in-process fakes that mimic the sila2 dynamic client (unobservable commands return a
NamedTuple; observable commands return an instance with subscribe_to_intermediate_responses()
and get_responses()), so they test the scheduling logic without servers. 4 runs run_demo.py
for real (both twin servers as subprocesses) on spare ports.
"""

from __future__ import annotations

import json
import socket
import subprocess
import sys
import tempfile
import threading
import time
from pathlib import Path
from typing import NamedTuple

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from scheduler import report  # noqa: E402
from scheduler.scheduler import Scheduler  # noqa: E402
from scheduler.workflow import Step, Workflow, load_workflow, validate  # noqa: E402

FAST_SCALE = 0.2  # real seconds per workflow minute in the fake runs (5 min -> 1 s)


# ------------------------------------------------------------------ fakes


class Message(NamedTuple):
    Message: str


class Reached(NamedTuple):
    ReachedTemperature: float


class Volumes(NamedTuple):
    VolumesJson: str


class Trace(NamedTuple):
    TraceJson: str


class StepUpdate(NamedTuple):
    Step: str


class TemperatureUpdate(NamedTuple):
    CurrentTemperature: float


class FakeSubscription:
    """Mimics sila2's Subscription: an iterator over intermediate responses with cancel()."""

    def __init__(self, items, delay_s):
        self._items, self._delay = iter(items), delay_s

    def __iter__(self):
        return self

    def __next__(self):
        item = next(self._items)
        time.sleep(self._delay)
        return item

    def cancel(self):
        self._items = iter(())


class FakeInstance:
    """Mimics ClientObservableCommandInstanceWithIntermediateResponses."""

    def __init__(self, intermediates, final, delay_s=0.02, error=None):
        self._intermediates, self._final, self._delay, self._error = intermediates, final, delay_s, error

    def subscribe_to_intermediate_responses(self):
        return FakeSubscription(self._intermediates, self._delay)

    def get_responses(self):
        if self._error:
            raise self._error
        return self._final


class FakeLH:
    """Liquid handler fake: tracks column volumes and busy-ness (to catch lane overlaps)."""

    def __init__(self, fail_on_quench_column=None):
        self.vol = {(p, c): v for p, v in report.NOMINAL_START_UL.items() for c in range(1, 13)}
        self.fail_on = fail_on_quench_column
        self.busy = threading.Lock()
        self.overlaps = 0

    def _enter(self):
        if not self.busy.acquire(blocking=False):
            self.overlaps += 1
            self.busy.acquire()
        time.sleep(0.02)
        self.busy.release()

    def Initialize(self):
        self._enter()
        return Message("fake STAR ready")

    def Transfer(self, SourcePlate, SourceColumn, TargetPlate, TargetColumn, VolumeUl):
        self._enter()
        if TargetPlate == "quench" and TargetColumn == self.fail_on:
            return FakeInstance([], None, error=RuntimeError("simulated LiquidHandlingError"))
        self.vol[(SourcePlate, SourceColumn)] -= VolumeUl
        self.vol[(TargetPlate, TargetColumn)] += VolumeUl
        steps = [StepUpdate(s) for s in ("pick up tips", "aspirate", "dispense", "drop tips")]
        return FakeInstance(steps, Message("ok"))

    def GetWellVolumes(self, Plate):
        wells = {f"{r}{c}": self.vol[(Plate, c)] for r in report.ROWS for c in range(1, 13)}
        return Volumes(json.dumps(wells))

    def GetFirmwareTrace(self, SinceIndex):
        return Trace(json.dumps([{"index": 0, "time": 0.0, "command": "C0ASid0001", "reply": "C0ASid0001er00/00"}]))


class FakeHHS:
    def __init__(self):
        self.temp = 22.0

    def SetTemperature(self, TargetTemperature):
        ramp = [TemperatureUpdate(self.temp + (TargetTemperature - self.temp) * k / 5) for k in range(1, 6)]
        self.temp = TargetTemperature
        return FakeInstance(ramp, Reached(TargetTemperature), delay_s=0.05)

    def StartShaking(self, Speed):
        return Message(f"shaking at {Speed}")

    def StopShaking(self):
        return Message("stopped")


def fast_workflow() -> Workflow:
    wf = load_workflow()
    wf.real_seconds_per_workflow_minute = FAST_SCALE
    return wf


# ------------------------------------------------------------------ tests


def test_fake_run_respects_dependencies_and_timing():
    wf = fast_workflow()
    lh, hhs = FakeLH(), FakeHHS()
    timeline = Scheduler(wf, {"lh": lh, "hhs": hhs}, log=lambda line: None).run()
    steps = {s["id"]: s for s in timeline["steps"]}

    assert timeline["run_status"] == "succeeded", [s["error"] for s in steps.values() if s["error"]]
    assert lh.overlaps == 0, "the LH lane ran two steps at once"
    for s in steps.values():  # every step starts after all of its dependencies ended
        for dep in s["depends_on"]:
            assert s["start_s"] >= steps[dep]["end_s"], (s["id"], dep)
        if s["start_after_t0_s"] is not None:  # and timed steps not before they are due
            due = timeline["t0_s"] + s["start_after_t0_s"] / 60 * FAST_SCALE
            assert s["start_s"] >= due - 1e-3, s["id"]
    assert timeline["t0_s"] == steps["add_nadph"]["end_s"]
    assert steps["heat_to_37"]["intermediate_count"] == 5
    assert steps["add_compound"]["intermediate_count"] == 4
    assert lh.vol[("reaction", 1)] == 300 + 50 + 50 - 5 * 50
    assert all(lh.vol[("quench", c)] == 200 for c in range(1, 6))

    with tempfile.TemporaryDirectory() as tmp:  # the report code works on a fake timeline
        volumes = {p: json.loads(lh.GetWellVolumes(p).VolumesJson) for p in report.PLATES}
        trace = json.loads(lh.GetFirmwareTrace(0).TraceJson)
        report.write_gantt(timeline, Path(tmp) / "gantt.svg")
        report.write_plate_volumes(volumes, Path(tmp) / "plate_volumes.svg")
        text = report.write_summary(timeline, volumes, trace, "fake", Path(tmp) / "run_summary.md")
        assert "| reaction | 1 | 150.0 | 150.0 |" in text
        assert (Path(tmp) / "gantt.svg").stat().st_size > 1000


def test_fake_failure_stops_the_run():
    wf = fast_workflow()
    timeline = Scheduler(wf, {"lh": FakeLH(fail_on_quench_column=2), "hhs": FakeHHS()}, log=lambda _: None).run()
    status = {s["id"]: s["status"] for s in timeline["steps"]}
    assert timeline["run_status"] == "failed"
    assert status["sample_t1"] == "failed"
    assert status["sample_t0"] == "succeeded"
    for later in ("shake_t1", "stop_t2", "sample_t5", "cool_to_22", "firmware_trace"):
        assert status[later] == "skipped", later
    assert "simulated LiquidHandlingError" in next(s["error"] for s in timeline["steps"] if s["id"] == "sample_t1")


def test_step_watchdog_fails_a_hanging_call():
    class SlowLH(FakeLH):
        def Initialize(self):
            time.sleep(2.0)  # longer than the watchdog below
            return Message("too late")

    wf = fast_workflow()
    timeline = Scheduler(wf, {"lh": SlowLH(), "hhs": FakeHHS()}, log=lambda _: None, step_timeout_s=0.5).run()
    init = next(s for s in timeline["steps"] if s["id"] == "lh_init")
    assert timeline["run_status"] == "failed"
    assert init["status"] == "failed" and "watchdog" in init["error"], init
    assert init["duration_s"] < 1.5


def test_validation_rejects_cycles_and_untimed_t0():
    wf = fast_workflow()
    cyclic = Workflow("x", 1.0, wf.devices, [Step("a", "lh", "Initialize", depends_on=("b",)),
                                             Step("b", "lh", "Initialize", depends_on=("a",))])
    no_t0 = Workflow("y", 1.0, wf.devices, [Step("a", "lh", "Initialize", start_after_t0_s=60)])
    for bad in (cyclic, no_t0):
        try:
            validate(bad)
        except ValueError:
            continue
        raise AssertionError(f"workflow {bad.name} should be rejected")


def servers_implemented() -> bool:
    impls = [ROOT / "servers/lh_twin/lh_twin/feature_implementations/liquidhandlerservice_impl.py",
             ROOT / "servers/hhs_twin/hhs_twin/feature_implementations/heatershakerservice_impl.py"]
    return all("raise NotImplementedError" not in p.read_text() for p in impls)


def free_ports(n: int) -> list[int]:
    """n distinct ports nobody listens on right now (the OS picks them; sockets held together)."""
    socks = [socket.socket() for _ in range(n)]
    try:
        for sock in socks:
            sock.bind(("127.0.0.1", 0))
        return [sock.getsockname()[1] for sock in socks]
    finally:
        for sock in socks:
            sock.close()


def test_port_in_use_is_detected():
    """A listener with SO_REUSEPORT (as gRPC uses) must still make run_demo refuse the port."""
    import run_demo

    with socket.socket() as listener:
        listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        listener.bind(("127.0.0.1", 0))
        listener.listen()
        try:
            run_demo.ensure_port_free(listener.getsockname()[1])
        except RuntimeError as ex:
            assert "already in use" in str(ex)
        else:
            raise AssertionError("busy port not detected")
    run_demo.ensure_port_free(free_ports(1)[0])  # and a free one passes


def test_end_to_end_demo():
    if not servers_implemented():
        print("  SKIP end-to-end: server implementations are still stubs")
        return
    with tempfile.TemporaryDirectory() as tmp:
        lh_port, hhs_port = free_ports(2)
        proc = subprocess.run(
            [sys.executable, str(ROOT / "run_demo.py"), "--out", tmp, "--time-scale", "1.0",
             "--lh-port", str(lh_port), "--hhs-port", str(hhs_port)],
            cwd=ROOT, capture_output=True, text=True, timeout=300,
        )
        assert proc.returncode == 0, proc.stdout[-3000:] + proc.stderr[-3000:]
        for name in ("timeline.json", "firmware_trace.json", "well_volumes.json", "gantt.svg",
                     "plate_volumes.svg", "run_summary.md"):
            assert (Path(tmp) / name).stat().st_size > 0, name
        volumes = json.loads((Path(tmp) / "well_volumes.json").read_text())
        col = report.column_mean
        # relative checks, robust to the twin scaling its starting volumes
        assert abs(col(volumes["reaction"], 1) - (col(volumes["reaction"], 2) - 150)) < 0.5
        for c in range(1, 6):
            assert abs(col(volumes["quench"], c) - (col(volumes["quench"], 6) + 50)) < 0.5, c
        assert len(json.loads((Path(tmp) / "firmware_trace.json").read_text())) > 10


if __name__ == "__main__":
    failures = 0
    for name, fn in [(n, f) for n, f in globals().items() if n.startswith("test_")]:
        t = time.monotonic()
        try:
            fn()
            print(f"PASS {name} ({time.monotonic() - t:.1f} s)")
        except Exception as ex:  # noqa: BLE001
            failures += 1
            print(f"FAIL {name}: {type(ex).__name__}: {ex}")
    sys.exit(1 if failures else 0)
