"""End-to-end demo: start both SiLA 2 twin servers, run the workflow, write results/.

    uv run python run_demo.py                     # default workflow, ports 50052/50053
    uv run python run_demo.py --time-scale 1.0    # 1 workflow-minute = 1 s (faster)

Steps:
  1. start servers/lh_twin and servers/hhs_twin as subprocesses (insecure, no discovery,
     localhost only); their output goes to results/logs/lh_twin.log and results/logs/hhs_twin.log
  2. wait until each one answers a SiLA connection (SilaClient lists its features)
  3. run scheduler/workflow.yaml with the scheduler (live log on the console)
  4. read back the firmware trace and well volumes, write timeline/trace/volumes JSON,
     gantt.svg, plate_volumes.svg and run_summary.md
  5. always stop the servers; exit code 1 if any step failed
"""

from __future__ import annotations

import argparse
import dataclasses
import json
import subprocess
import sys
import time
from pathlib import Path
from typing import Any

from sila2.client import SilaClient

from scheduler import report
from scheduler.scheduler import Scheduler, describe_error
from scheduler.workflow import DEFAULT_WORKFLOW, Workflow, load_workflow

HERE = Path(__file__).resolve().parent
SERVER_MODULES = {"lh": "lh_twin", "hhs": "hhs_twin"}  # workflow device -> server package


def start_server(module: str, port: int, log_path: Path) -> subprocess.Popen:
    """Launch `python -m <module>` as a SiLA 2 server on localhost:<port>."""
    log = log_path.open("w")
    cmd = [sys.executable, "-m", module, "--ip-address", "127.0.0.1", "--port", str(port),
           "--insecure", "--disable-discovery"]
    return subprocess.Popen(cmd, stdout=log, stderr=subprocess.STDOUT, cwd=HERE)


def wait_for_server(proc: subprocess.Popen, host: str, port: int, feature: str, log_path: Path,
                    timeout_s: float = 90.0) -> SilaClient:
    """Retry SilaClient until the server lists `feature`; fail early if the process died."""
    deadline = time.monotonic() + timeout_s
    last_error = "no attempt"
    while time.monotonic() < deadline:
        if proc.poll() is not None:
            tail = "\n".join(log_path.read_text().splitlines()[-15:])
            raise RuntimeError(f"server on port {port} exited with code {proc.returncode}:\n{tail}")
        try:
            client = SilaClient(host, port, insecure=True)
            if hasattr(client, feature):
                return client
            client.close()
            last_error = f"feature {feature} not offered"
        except Exception as ex:  # noqa: BLE001 - not up yet
            last_error = describe_error(ex)
        time.sleep(0.5)
    raise TimeoutError(f"server on port {port} not ready after {timeout_s:g} s ({last_error})")


def stop_server(proc: subprocess.Popen) -> None:
    """SIGTERM (the generated server stops its gRPC server on it), then kill if needed."""
    if proc.poll() is None:
        proc.terminate()
        try:
            proc.wait(timeout=10)
        except subprocess.TimeoutExpired:
            proc.kill()
            proc.wait()


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
    procs: list[subprocess.Popen] = []
    clients: list[SilaClient] = []
    try:
        features = {}
        for name, dev in wf.devices.items():
            log_path = logs / f"{SERVER_MODULES[name]}.log"
            print(f"starting {SERVER_MODULES[name]} on {dev.host}:{dev.port} (log: {log_path})")
            procs.append(start_server(SERVER_MODULES[name], dev.port, log_path))
        for proc, (name, dev) in zip(procs, wf.devices.items()):
            client = wait_for_server(proc, dev.host, dev.port, dev.feature, logs / f"{SERVER_MODULES[name]}.log")
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
        for proc in procs:
            stop_server(proc)
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
    sys.exit(run(parse_args()))
