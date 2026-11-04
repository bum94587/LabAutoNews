"""Where the console keeps its runtime state. All of it is under ``runtime/`` (git-ignored)."""

from __future__ import annotations

from pathlib import Path

SILA2_DIR = Path(__file__).resolve().parent.parent
RUNTIME = SILA2_DIR / "runtime"
SERVERS_DIR = RUNTIME / "servers"  # <name>.json: pid, port, uuid, options, viewer url
LOGS_DIR = RUNTIME / "logs"  # <name>.log: server stdout/stderr
TRAFFIC_DIR = RUNTIME / "traffic"  # sila_<name>.jsonl (gRPC calls), firmware_lh.jsonl (STAR commands)
RUNS_DIR = RUNTIME / "runs"  # <run id>/: status.json, live.log and the report files
METHODS_DIR = SILA2_DIR / "methods"  # extra workflow files; scheduler/workflow.yaml is the default method


def ensure_dirs() -> None:
    for d in (SERVERS_DIR, LOGS_DIR, TRAFFIC_DIR, RUNS_DIR):
        d.mkdir(parents=True, exist_ok=True)


def sila_traffic_file(name: str) -> Path:
    return TRAFFIC_DIR / f"sila_{name}.jsonl"


def firmware_traffic_file() -> Path:
    return TRAFFIC_DIR / "firmware_lh.jsonl"
