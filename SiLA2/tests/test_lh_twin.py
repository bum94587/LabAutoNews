"""
Integration test for the Hamilton STAR twin SiLA 2 server (servers/lh_twin).

Starts ``python -m lh_twin`` as a subprocess on a free port (as run_demo.py would), talks to it
with the *dynamic* sila2 client (the API the scheduler uses), then stops it with SIGTERM.

Run from SiLA2/:
    uv run python tests/test_lh_twin.py
(also collectable by pytest: one ``test_lh_twin`` function runs the checks in order).

Covers:
- InstrumentInfo and the observable Status property (idle / busy: ... / error: ...).
- NotInitialized before Initialize; Initialize; GetDeckLayout (contract resource names).
- Transfer as an observable command: 4 intermediate Step responses, final Message,
  automatic tip-column tracking (column 1, then 2, ...).
- GetWellVolumes reflects the transfer; GetFirmwareTrace(SinceIndex) returns firmware strings.
- Clean shutdown: SIGTERM must end the server with exit code 0 (no kill needed).
- LiquidHandlingError: aspirate without tips, too little liquid, unknown plate, failing Transfer
  (tips are put back), out of tips after 12 columns.
"""

from __future__ import annotations

import json
import signal
import socket
import subprocess
import sys
import tempfile
import threading
import time
from pathlib import Path

from sila2.client import SilaClient
from sila2.framework import DefinedExecutionError

HOST = "127.0.0.1"


# --- server process handling --------------------------------------------------------------


def free_port() -> int:
    """Ask the OS for an unused TCP port."""
    with socket.socket() as s:
        s.bind((HOST, 0))
        return s.getsockname()[1]


class ServerProcess:
    """Runs ``python -m lh_twin`` in a subprocess, with its log captured to a temp file."""

    def __init__(self) -> None:
        self.port = free_port()
        self.log_file = Path(tempfile.mkstemp(prefix="lh_twin_", suffix=".log")[1])
        self._log_fp = self.log_file.open("w")
        self.proc = subprocess.Popen(
            [sys.executable, "-m", "lh_twin", "--port", str(self.port), "--insecure", "--disable-discovery"],
            stdout=self._log_fp,
            stderr=subprocess.STDOUT,
        )

    def connect(self, timeout_s: float = 30.0) -> SilaClient:
        """Retry until the server answers a SiLA call."""
        deadline = time.monotonic() + timeout_s
        while True:
            if self.proc.poll() is not None:
                raise RuntimeError(f"server exited early:\n{self.log()}")
            try:
                client = SilaClient(HOST, self.port, insecure=True)
                client.SiLAService.ServerName.get()
                return client
            except Exception:  # noqa: BLE001 - not up yet
                if time.monotonic() > deadline:
                    raise
                time.sleep(0.3)

    def stop(self) -> int:
        """SIGTERM, then wait; returns the exit code."""
        if self.proc.poll() is None:
            self.proc.send_signal(signal.SIGTERM)
            try:
                self.proc.wait(timeout=10)
            except subprocess.TimeoutExpired:
                self.proc.kill()
                self.proc.wait()
        self._log_fp.close()
        return self.proc.returncode

    def log(self) -> str:
        self._log_fp.flush()
        return self.log_file.read_text()


# --- helpers ------------------------------------------------------------------------------


def expect_error(identifier: str, func, *args, **kwargs) -> str:
    """Call ``func`` and assert it raises the named SiLA defined execution error."""
    try:
        func(*args, **kwargs)
    except DefinedExecutionError as error:
        assert error.identifier == identifier, f"expected {identifier}, got {error.identifier}: {error.message}"
        print(f"  [ok] {identifier}: {error.message}")
        return error.message
    raise AssertionError(f"expected {identifier}, but the call succeeded")


def run_transfer(lh, **params) -> tuple[list[str], str]:
    """Start an observable Transfer, stream its Step intermediate responses, return (steps, message)."""
    instance = lh.Transfer(**params)  # returns at once with a command execution UUID
    steps: list[str] = []
    subscription = instance.subscribe_to_intermediate_responses()
    for item in subscription:  # ends when the command finishes
        steps.append(item.Step)
        print(f"    step: {item.Step}")
    while not instance.done:  # execution info arrives on its own subscription thread
        time.sleep(0.05)
    return steps, instance.get_responses().Message


def collect_status(lh, sink: list[str]):
    """Subscribe to the observable Status property and append every value to ``sink``."""
    subscription = lh.Status.subscribe()
    subscription.add_callback(sink.append)
    return subscription


# --- the test -----------------------------------------------------------------------------


def check_all(lh) -> None:
    print("InstrumentInfo:", lh.InstrumentInfo.get().splitlines()[0][:160], "...")
    assert lh.Status.get() == "idle"

    print("Before Initialize:")
    expect_error("NotInitialized", lh.GetDeckLayout)
    expect_error("NotInitialized", lh.Aspirate, Plate="compounds", Column=1, VolumeUl=10.0)
    assert json.loads(lh.GetFirmwareTrace(SinceIndex=0).TraceJson) == []

    statuses: list[str] = []
    status_sub = collect_status(lh, statuses)

    print("Initialize:")
    summary = lh.Initialize().Summary
    print("  " + summary.splitlines()[0])
    setup_trace = json.loads(lh.GetFirmwareTrace(SinceIndex=0).TraceJson)
    assert len(setup_trace) > 50, "setup should exchange many firmware commands"

    print("GetDeckLayout:")
    layout = json.loads(lh.GetDeckLayout().DeckLayoutJson)
    names = set()

    def walk(node):
        names.add(node["name"])
        for child in node.get("children", []):
            walk(child)

    walk(layout["tree"])
    for name in ("tip_car", "tips", "plate_car", "compounds", "nadph", "reaction", "quench"):
        assert name in names, f"{name} missing from deck layout"
    print(f"  {len(names)} resources, POC layout: {layout['poc_layout']['plate_car']}")

    print("Transfer compounds col 1 -> reaction col 1, 50 uL (observable):")
    steps, message = run_transfer(
        lh, SourcePlate="compounds", SourceColumn=1, TargetPlate="reaction", TargetColumn=1, VolumeUl=50.0
    )
    print("  final:", message)
    assert len(steps) == 4 and steps[0].startswith("1/4 pick up tips: tips column 1"), steps

    vols = json.loads(lh.GetWellVolumes(Plate="compounds").VolumesJson)
    rvols = json.loads(lh.GetWellVolumes(Plate="reaction").VolumesJson)
    print(f"  compounds A1={vols['A1']} H1={vols['H1']} A2={vols['A2']}; reaction A1={rvols['A1']}")
    assert len(vols) == 96 and vols["A1"] == vols["H1"] == 150.0 and vols["A2"] == 200.0
    assert rvols["A1"] == 350.0

    print("Second Transfer uses the next tip column:")
    steps, _ = run_transfer(lh, SourcePlate="nadph", SourceColumn=1, TargetPlate="reaction", TargetColumn=1, VolumeUl=50.0)
    assert "tips column 2" in steps[0], steps

    print("GetFirmwareTrace:")
    trace = json.loads(lh.GetFirmwareTrace(SinceIndex=0).TraceJson)
    commands = [entry["command"][:4] for entry in trace]
    for code, meaning in (("C0TP", "tip pick-up"), ("C0AS", "aspirate"), ("C0DS", "dispense"), ("C0TR", "tip drop")):
        assert code in commands, f"{code} ({meaning}) not in trace"
    assert [e["index"] for e in trace] == list(range(len(trace)))
    tail = json.loads(lh.GetFirmwareTrace(SinceIndex=len(setup_trace)).TraceJson)
    assert tail[0]["index"] == len(setup_trace)
    aspirate = next(e for e in trace if e["command"].startswith("C0AS"))
    print(f"  {len(trace)} entries ({len(setup_trace)} from setup); e.g. #{aspirate['index']} during "
          f"'{aspirate['operation']}': {aspirate['command'][:90]}...")

    print("Errors:")
    expect_error("LiquidHandlingError", lh.Aspirate, Plate="compounds", Column=1, VolumeUl=10.0)  # no tips
    lh.PickUpTips(TipRack="tips", Column=3)
    expect_error("LiquidHandlingError", lh.Aspirate, Plate="compounds", Column=1, VolumeUl=180.0)  # 150 left
    assert lh.Status.get().startswith("error:")
    print("  DropTips:", lh.DropTips().Message)
    assert lh.Status.get() == "idle"
    expect_error("LiquidHandlingError", lh.GetWellVolumes, Plate="no_such_plate")
    expect_error("LiquidHandlingError", run_transfer, lh, SourcePlate="nope", SourceColumn=1,
                 TargetPlate="quench", TargetColumn=1, VolumeUl=10.0)
    # Fails at the aspirate step, after tips were picked up: the twin must put them back.
    expect_error("LiquidHandlingError", run_transfer, lh, SourcePlate="compounds", SourceColumn=1,
                 TargetPlate="quench", TargetColumn=1, VolumeUl=500.0)
    lh.PickUpTips(TipRack="tips", Column=12)  # would fail if the failed Transfer had left tips on
    lh.DropTips()

    print("Run the rack empty:")
    used = 0
    while True:
        try:
            run_transfer(lh, SourcePlate="nadph", SourceColumn=2, TargetPlate="quench", TargetColumn=2, VolumeUl=1.0)
            used += 1
        except DefinedExecutionError as error:
            assert error.identifier == "LiquidHandlingError" and "out of tips" in error.message, error.message
            print(f"  [ok] after {used} more transfers: {error.message}")
            break
        assert used < 12, "tip tracking never ran out"
    print("  quench B2 volume:", json.loads(lh.GetWellVolumes(Plate="quench").VolumesJson)["B2"])

    time.sleep(0.3)
    status_sub.cancel()
    busy = [s for s in statuses if s.startswith("busy:")]
    print(f"Status subscription saw {len(statuses)} updates, e.g. {busy[:2]}")
    assert busy and any(s.startswith("error:") for s in statuses) and "idle" in statuses


def test_lh_twin() -> None:
    server = ServerProcess()
    try:
        client = server.connect()
        print(f"Connected to '{client.SiLAService.ServerName.get()}' on port {server.port}")
        check_all(client.LiquidHandlerService)
    except BaseException:
        print("---- server log ----\n" + server.log()[-4000:])
        raise
    finally:
        code = server.stop()
        print(f"Server stopped (exit code {code})")
    assert code == 0, f"server did not exit cleanly on SIGTERM (exit code {code})"


if __name__ == "__main__":
    test_lh_twin()
    print("ALL LH TWIN CHECKS PASSED")
