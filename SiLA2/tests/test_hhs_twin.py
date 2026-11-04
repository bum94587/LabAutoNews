"""
Integration test for the heater-shaker twin SiLA 2 server (servers/hhs_twin).

Starts the server as a subprocess on a free port (exactly as run_demo.py would), talks to it with
the *dynamic* sila2 client (the same API the scheduler uses), then stops it with SIGTERM.

Run from SiLA2/:
    uv run python tests/test_hhs_twin.py
(also collectable by pytest: every check is a ``test_*`` function sharing one server).

Covers:
- SetTemperature(37) as an observable command: intermediate responses stream the ramp,
  final response ReachedTemperature is within 0.5 C, real duration matches tau=30 s at 10x.
- Subscription to the observable property CurrentTemperature follows the ramp.
- StartShaking / StopShaking and the ShakingSpeed property.
- Defined execution errors SpeedOutOfRange and TemperatureOutOfRange (dynamic and generated client).
- Clean shutdown on SIGTERM.
"""

from __future__ import annotations

import atexit
import math
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
EXPECTED_RAMP_S = 30.0 * math.log(15.0 / 0.5) / 10.0  # 22 -> 37 C within 0.5 C: ~10.2 s real


# --- server process handling --------------------------------------------------------------


def free_port() -> int:
    """Ask the OS for an unused TCP port."""
    with socket.socket() as s:
        s.bind((HOST, 0))
        return s.getsockname()[1]


class ServerProcess:
    """Runs ``python -m hhs_twin`` in a subprocess, with its log captured to a temp file."""

    def __init__(self) -> None:
        self.port = free_port()
        self.log_file = Path(tempfile.mkstemp(prefix="hhs_twin_", suffix=".log")[1])
        self._log_fp = self.log_file.open("w")
        self.proc = subprocess.Popen(
            [sys.executable, "-m", "hhs_twin", "--port", str(self.port), "--insecure", "--disable-discovery"],
            stdout=self._log_fp,
            stderr=subprocess.STDOUT,
        )

    def connect(self, timeout_s: float = 20.0) -> SilaClient:
        """Retry until the server answers a SiLA call."""
        deadline = time.monotonic() + timeout_s
        while True:
            if self.proc.poll() is not None:
                raise RuntimeError(f"server exited early:\n{self.log()}")
            try:
                client = SilaClient(HOST, self.port, insecure=True)
                client.SiLAService.ServerName.get()
                return client
            except Exception:
                if time.monotonic() > deadline:
                    raise
                time.sleep(0.3)

    def stop(self, timeout_s: float = 15.0) -> int:
        """SIGTERM, wait; kill as a last resort. Returns the exit code."""
        if self.proc.poll() is None:
            self.proc.send_signal(signal.SIGTERM)
            try:
                self.proc.wait(timeout_s)
            except subprocess.TimeoutExpired:
                self.proc.kill()
                self.proc.wait()
                self._log_fp.close()
                raise AssertionError(f"server did not stop on SIGTERM within {timeout_s} s")
        self._log_fp.close()
        return self.proc.returncode

    def log(self) -> str:
        if not self._log_fp.closed:
            self._log_fp.flush()
        return self.log_file.read_text()


# One server for the whole module (module-level so pytest and the __main__ runner share it).
_server: ServerProcess | None = None
_client: SilaClient | None = None


def client() -> SilaClient:
    global _server, _client
    if _client is None:
        _server = ServerProcess()
        atexit.register(_kill_server)  # never leave a server behind, even if a test crashes
        _client = _server.connect()
    return _client


def _kill_server() -> None:
    if _server is not None and _server.proc.poll() is None:
        _server.proc.kill()
        _server.proc.wait()


# --- tests ---------------------------------------------------------------------------------


def test_initial_state():
    hhs = client().HeaterShakerService
    assert client().SiLAService.ServerName.get() == "HHS Twin"
    assert abs(hhs.CurrentTemperature.get() - 22.0) < 0.01, "twin should start at 22.0 C"
    assert hhs.ShakingSpeed.get() == 0


def test_set_temperature_37_with_property_subscription():
    hhs = client().HeaterShakerService

    # Observable property: subscribe and collect every pushed value via a callback.
    property_values: list[float] = []
    lock = threading.Lock()

    def on_value(v: float) -> None:
        with lock:
            property_values.append(v)

    prop_sub = hhs.CurrentTemperature.subscribe(callbacks=[on_value])

    # Observable command: the call returns an instance immediately (Command Execution UUID).
    t0 = time.monotonic()
    inst = hhs.SetTemperature(TargetTemperature=37.0)

    # Intermediate responses: the stream ends by itself when the command finishes.
    ramp = [r.CurrentTemperature for r in inst.subscribe_to_intermediate_responses()]
    elapsed = time.monotonic() - t0

    # After the intermediate stream has ended the result is available.
    result = inst.get_responses()
    time.sleep(0.6)  # let the last property updates arrive
    prop_sub.cancel()

    print(f"  SetTemperature(37): {len(ramp)} intermediate responses in {elapsed:.1f} s, "
          f"first {ramp[0]:.2f} C, last {ramp[-1]:.2f} C, ReachedTemperature {result.ReachedTemperature:.2f} C")
    with lock:
        values = list(property_values)
    print(f"  CurrentTemperature subscription: {len(values)} values, {values[0]:.2f} -> {values[-1]:.2f} C")

    assert len(ramp) >= 20, "expected ~4 intermediate responses per real second over ~10 s"
    assert all(b >= a for a, b in zip(ramp, ramp[1:])), "heating ramp must be monotonic"
    assert ramp[0] < 25.0
    assert abs(result.ReachedTemperature - 37.0) <= 0.5
    assert EXPECTED_RAMP_S - 1.5 < elapsed < EXPECTED_RAMP_S + 3.0, f"ramp took {elapsed:.1f} s"

    assert len(values) >= 20, "observable property should update during the ramp"
    assert values[0] < 25.0 and values[-1] > 36.5
    assert all(b >= a for a, b in zip(values, values[1:]))

    # The model keeps evolving after the command finished (background tick): T -> 37.
    time.sleep(1.0)
    assert hhs.CurrentTemperature.get() > result.ReachedTemperature


def test_shaking():
    hhs = client().HeaterShakerService
    msg = hhs.StartShaking(Speed=600).Message
    print(f"  StartShaking(600): {msg!r}")
    assert hhs.ShakingSpeed.get() == 600
    msg = hhs.StopShaking().Message
    print(f"  StopShaking(): {msg!r}")
    assert hhs.ShakingSpeed.get() == 0


def test_speed_out_of_range():
    hhs = client().HeaterShakerService
    for bad in (100, 5000):
        try:
            hhs.StartShaking(Speed=bad)
        except DefinedExecutionError as err:
            # Dynamic client: plain DefinedExecutionError carrying the FDL identifier.
            assert err.identifier == "SpeedOutOfRange", err
            print(f"  StartShaking({bad}) -> {err.identifier}: {err.message}")
        else:
            raise AssertionError(f"StartShaking({bad}) should fail")
    assert hhs.ShakingSpeed.get() == 0


def test_temperature_out_of_range():
    hhs = client().HeaterShakerService
    inst = hhs.SetTemperature(TargetTemperature=100.0)
    # The command fails at once: the intermediate stream is empty and the error comes with the result.
    assert list(inst.subscribe_to_intermediate_responses()) == []
    try:
        inst.get_responses()
    except DefinedExecutionError as err:
        assert err.identifier == "TemperatureOutOfRange", err
        print(f"  SetTemperature(100) -> {err.identifier}: {err.message}")
    else:
        raise AssertionError("SetTemperature(100) should fail")

    # The code-generated client raises the generated error class instead.
    from hhs_twin.generated.client import Client
    from hhs_twin.generated.heatershakerservice import TemperatureOutOfRange

    with Client(HOST, _server.port, insecure=True) as typed:
        inst = typed.HeaterShakerService.SetTemperature(TargetTemperature=1.0)
        list(inst.subscribe_to_intermediate_responses())
        try:
            inst.get_responses()
        except TemperatureOutOfRange as err:
            print(f"  generated Client: SetTemperature(1) -> {type(err).__name__}")
        else:
            raise AssertionError("SetTemperature(1) should fail")


def test_shutdown():
    """Last: SIGTERM must stop the server promptly with exit code 0, and the log has the state changes."""
    global _client
    client().close()
    _client = None
    code = _server.stop()
    log = _server.log()
    assert code == 0, f"exit code {code}\n{log}"
    for needle in ("Setpoint -> 37.00 C", "Setpoint reached", "Shaking: 0 -> 600 rpm", "Shaking stopped"):
        assert needle in log, f"missing log line {needle!r}"
    print(f"  server stopped (exit {code}); log at {_server.log_file}")


TESTS = [
    test_initial_state,
    test_set_temperature_37_with_property_subscription,
    test_shaking,
    test_speed_out_of_range,
    test_temperature_out_of_range,
    test_shutdown,
]


def main() -> int:
    failures = 0
    try:
        for test in TESTS:
            print(f"{test.__name__} ...")
            try:
                test()
                print("  PASS")
            except Exception as exc:  # report and continue
                failures += 1
                print(f"  FAIL: {type(exc).__name__}: {exc}")
    finally:
        _kill_server()
    print(f"\n{len(TESTS) - failures}/{len(TESTS)} passed")
    if failures and _server is not None:
        print("--- server log ---\n" + _server.log())
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
