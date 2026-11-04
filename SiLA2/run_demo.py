"""End-to-end demo: start both SiLA 2 twin servers, run the workflow, write results/.

    uv run python run_demo.py                     # default workflow, ports 50052/50053
    uv run python run_demo.py --time-scale 1.0    # 1 workflow-minute = 1 s (faster)

Steps:
  1. check the ports are free, then start servers/lh_twin and servers/hhs_twin as subprocesses
     (insecure, no discovery, localhost only, each with a fresh server UUID); their output goes
     to results/logs/lh_twin.log and results/logs/hhs_twin.log
  2. wait until each one answers a SiLA connection with *its* UUID and lists its feature
  3. run scheduler/workflow.yaml with the scheduler (live log on the console)
  4. read back the firmware trace and well volumes, write timeline/trace/volumes JSON,
     gantt.svg, plate_volumes.svg and run_summary.md
  5. always stop the servers; exit code 1 if any step failed
"""

from __future__ import annotations

import argparse
import dataclasses
import json
import socket
import subprocess
import sys
import time
import uuid
from pathlib import Path
from typing import IO, Any

from sila2.client import SilaClient

from scheduler import report
from scheduler.scheduler import Scheduler, describe_error
from scheduler.workflow import DEFAULT_WORKFLOW, Workflow, load_workflow

HERE = Path(__file__).resolve().parent
SERVER_MODULES = {"lh": "lh_twin", "hhs": "hhs_twin"}  # workflow device -> server package


@dataclasses.dataclass
class ServerProcess:
    """A twin server subprocess and what we need to talk to it and clean it up."""

    module: str
    port: int
    server_uuid: str
    log_path: Path
    log_file: IO[str]
    proc: subprocess.Popen


def ensure_port_free(port: int, host: str = "127.0.0.1") -> None:
    """Fail loudly if something already listens on the port.

    gRPC servers bind with SO_REUSEPORT, so a second twin on the same port would start
    without complaint and the kernel would spread our connections across both. A plain
    bind (SO_REUSEADDR only, no SO_REUSEPORT) fails if the port is taken.
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            sock.bind((host, port))
        except OSError as ex:
            raise RuntimeError(
                f"port {port} is already in use ({ex.strerror}); is an old twin server still running? "
                f"Stop it, or pick other ports with --lh-port/--hhs-port."
            ) from None


def start_server(module: str, port: int, log_path: Path) -> ServerProcess:
    """Launch `python -m <module>` as a SiLA 2 server on localhost:<port> with a fresh UUID."""
    ensure_port_free(port)
    server_uuid = str(uuid.uuid4())
    log_file = log_path.open("w")
    cmd = [sys.executable, "-m", module, "--ip-address", "127.0.0.1", "--port", str(port),
           "--server-uuid", server_uuid, "--insecure", "--disable-discovery"]
    proc = subprocess.Popen(cmd, stdout=log_file, stderr=subprocess.STDOUT, cwd=HERE)
    return ServerProcess(module, port, server_uuid, log_path, log_file, proc)


def wait_for_server(server: ServerProcess, host: str, feature: str, timeout_s: float = 90.0) -> SilaClient:
    """Retry SilaClient until *our* server (matching UUID) lists `feature`; fail early if it died."""
    deadline = time.monotonic() + timeout_s
    last_error = "no attempt"
    while time.monotonic() < deadline:
        if server.proc.poll() is not None:
            server.log_file.flush()
            tail = "\n".join(server.log_path.read_text().splitlines()[-15:])
            raise RuntimeError(f"{server.module} on port {server.port} exited with code "
                               f"{server.proc.returncode}:\n{tail}")
        try:
            client = SilaClient(host, server.port, insecure=True)
        except Exception as ex:  # noqa: BLE001 - not up yet
            last_error = describe_error(ex)
            time.sleep(0.5)
            continue
        answered_uuid = str(client.SiLAService.ServerUUID.get())
        if answered_uuid != server.server_uuid:
            client.close()
            raise RuntimeError(f"port {server.port} is answered by another SiLA server (UUID {answered_uuid}, "
                               f"expected {server.server_uuid}); stop the other server first")
        if hasattr(client, feature):
            return client
        client.close()
        last_error = f"feature {feature} not offered"
        time.sleep(0.5)
    raise TimeoutError(f"{server.module} on port {server.port} not ready after {timeout_s:g} s ({last_error})")


def stop_server(server: ServerProcess) -> None:
    """SIGTERM (the server stops its gRPC server on it), kill if needed, close the log file."""
    proc = server.proc
    if proc.poll() is None:
        proc.terminate()
        try:
            proc.wait(timeout=10)
        except subprocess.TimeoutExpired:
            proc.kill()
            proc.wait()
    server.log_file.close()


def collect_lh_state(lh: Any) -> tuple[list[dict[str, Any]], dict[str, dict[str, Any]], str]:
    """Firmware trace, well volumes of every plate and InstrumentInfo, as far as available."""
    trace, volumes, info = [], {}, ""
    try:
        trace = json.loads(lh.GetFirmwareTrace(SinceIndex=0).TraceJson)
    except Exception as ex:  # noqa: BLE001 - partial results are still useful
        print(f"  could not read firmware trace: {describe_error(ex)}")
    for plate in report.PLATES:
        try:
            volumes[plate] = json.loads(lh.GetWellVolumes(Plate=plate).VolumesJson)
        except Exception as ex:  # noqa: BLE001
            print(f"  could not read volumes of {plate}: {describe_error(ex)}")
    try:
        info = lh.InstrumentInfo.get()
    except Exception as ex:  # noqa: BLE001
        print(f"  could not read InstrumentInfo: {describe_error(ex)}")
    return trace, volumes, info


def write_results(out: Path, timeline: dict, trace: list, volumes: dict, info: str, log_lines: list[str]) -> str:
    """Write every results/ file and return the summary text."""
    (out / "timeline.json").write_text(json.dumps(timeline, indent=2))
    (out / "firmware_trace.json").write_text(json.dumps(trace, indent=2))
    (out / "well_volumes.json").write_text(json.dumps(volumes, indent=2))
    (out / "run_log.txt").write_text("\n".join(log_lines) + "\n")
    report.write_gantt(timeline, out / "gantt.svg")
    report.write_plate_volumes(volumes, out / "plate_volumes.svg")
    return report.write_summary(timeline, volumes, trace, info, out / "run_summary.md")


def override_workflow(wf: Workflow, args: argparse.Namespace) -> Workflow:
    """Apply command-line overrides (ports, time scale) to the loaded workflow."""
    ports = {"lh": args.lh_port, "hhs": args.hhs_port}
    devices = {name: dataclasses.replace(d, host="127.0.0.1", port=ports.get(name) or d.port)
               for name, d in wf.devices.items()}
    scale = args.time_scale or wf.real_seconds_per_workflow_minute
    return Workflow(wf.name, scale, devices, wf.steps)


def run(args: argparse.Namespace) -> int:
    """The whole demo; returns the process exit code."""
    wf = override_workflow(load_workflow(args.workflow), args)
    out = Path(args.out)
    logs = out / "logs"
    logs.mkdir(parents=True, exist_ok=True)
    servers: list[ServerProcess] = []
    clients: list[SilaClient] = []
    try:
        features = {}
        for dev in wf.devices.values():  # check every port before starting anything
            ensure_port_free(dev.port)
        for name, dev in wf.devices.items():
            log_path = logs / f"{SERVER_MODULES[name]}.log"
            print(f"starting {SERVER_MODULES[name]} on {dev.host}:{dev.port} (log: {log_path})")
            servers.append(start_server(SERVER_MODULES[name], dev.port, log_path))
        for server, (name, dev) in zip(servers, wf.devices.items()):
            client = wait_for_server(server, dev.host, dev.feature)
            clients.append(client)
            features[name] = getattr(client, dev.feature)
            print(f"connected to {dev.feature} on port {dev.port}")

        scheduler = Scheduler(wf, features)
        timeline = scheduler.run()

        print("collecting results from the LH twin ...")
        trace, volumes, info = collect_lh_state(features["lh"])
        summary = write_results(out, timeline, trace, volumes, info, scheduler.log_lines)
        print_key_numbers(timeline, trace, volumes, out)
        if args.print_summary:
            print(summary)
        return 0 if timeline["run_status"] == "succeeded" else 1
    finally:
        for client in clients:
            client.close()
        for server in servers:
            stop_server(server)
        print("servers stopped")


def print_key_numbers(timeline: dict, trace: list, volumes: dict, out: Path) -> None:
    """A few headline numbers on the console; the full story is in run_summary.md."""
    steps = timeline["steps"]
    ok = sum(s["status"] == "succeeded" for s in steps)
    print(f"\nrun {timeline['run_status'].upper()}: {ok}/{len(steps)} steps succeeded "
          f"in {timeline['duration_s']:.1f} s")
    print(f"firmware commands sent to the STAR simulator: {len(trace)}")
    reaction = report.column_mean(volumes.get("reaction", {}), 1)
    quench = [report.column_mean(volumes.get("quench", {}), c) for c in range(1, 6)]
    print(f"reaction col 1: {reaction} uL; quench cols 1-5: {quench} uL")
    for s in steps:
        if s["command"] == "SetTemperature":
            print(f"{s['id']}: reached {report._fmt(s['responses'].get('ReachedTemperature'))} C ({s['status']})")
    failed = [s for s in steps if s["status"] == "failed"]
    for s in failed:
        print(f"FAILED step {s['id']}: {s['error']}")
    print(f"results written to {out}/")


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--workflow", default=str(DEFAULT_WORKFLOW), help="workflow YAML")
    p.add_argument("--out", default=str(HERE / "results"), help="results directory")
    p.add_argument("--time-scale", type=float, default=None,
                   help="real seconds per workflow minute (default: from the YAML)")
    p.add_argument("--lh-port", type=int, default=None, help="override the LH server port")
    p.add_argument("--hhs-port", type=int, default=None, help="override the HHS server port")
    p.add_argument("--print-summary", action="store_true", help="also print run_summary.md")
    return p.parse_args(argv)


if __name__ == "__main__":
    try:
        sys.exit(run(parse_args()))
    except (RuntimeError, TimeoutError) as err:  # setup problems (busy port, server did not start)
        print(f"ERROR: {err}", file=sys.stderr)
        sys.exit(2)
