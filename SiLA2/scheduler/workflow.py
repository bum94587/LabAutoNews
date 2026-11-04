"""Load and validate a workflow YAML file (format documented at the top of workflow.yaml).

The result is a plain `Workflow` object: devices (how to reach each SiLA server), the
steps in file order, and the time scale. Validation catches the mistakes that would
otherwise make the scheduler hang: unknown devices, unknown or circular dependencies,
and timed steps that can never become due because no step marks t0 before them.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml

DEFAULT_WORKFLOW = Path(__file__).with_name("workflow.yaml")


@dataclass(frozen=True)
class Device:
    """One SiLA 2 server = one scheduler lane."""

    name: str
    host: str
    port: int
    feature: str  # SiLA feature identifier, e.g. "LiquidHandlerService"
    description: str = ""


@dataclass(frozen=True)
class Step:
    """One SiLA command call in the workflow."""

    id: str
    device: str
    command: str
    params: dict[str, Any] = field(default_factory=dict)
    depends_on: tuple[str, ...] = ()
    start_after_t0_s: float | None = None  # workflow seconds after t0
    marks_t0: bool = False


@dataclass
class Workflow:
    name: str
    real_seconds_per_workflow_minute: float
    devices: dict[str, Device]
    steps: list[Step]

    def real_delay(self, workflow_seconds: float) -> float:
        """Convert a workflow-time offset into real seconds."""
        return workflow_seconds / 60.0 * self.real_seconds_per_workflow_minute

    def step(self, step_id: str) -> Step:
        return next(s for s in self.steps if s.id == step_id)


def load_workflow(path: str | Path = DEFAULT_WORKFLOW) -> Workflow:
    """Read a workflow YAML file, validate it, and return a `Workflow`."""
    raw = yaml.safe_load(Path(path).read_text())
    devices = {
        name: Device(
            name=name,
            host=d.get("host", "127.0.0.1"),
            port=int(d["port"]),
            feature=d["feature"],
            description=d.get("description", ""),
        )
        for name, d in raw["devices"].items()
    }
    steps = [
        Step(
            id=s["id"],
            device=s["device"],
            command=s["command"],
            params=dict(s.get("params") or {}),
            depends_on=tuple(s.get("depends_on") or ()),
            start_after_t0_s=s.get("start_after_t0_s"),
            marks_t0=bool(s.get("marks_t0", False)),
        )
        for s in raw["steps"]
    ]
    scale = float(raw.get("time_scale", {}).get("real_seconds_per_workflow_minute", 2.0))
    wf = Workflow(raw.get("name", Path(path).stem), scale, devices, steps)
    validate(wf)
    return wf


def validate(wf: Workflow) -> None:
    """Raise ValueError if the workflow could not run to completion."""
    ids = [s.id for s in wf.steps]
    dupes = {i for i in ids if ids.count(i) > 1}
    if dupes:
        raise ValueError(f"duplicate step ids: {sorted(dupes)}")
    known = set(ids)
    for s in wf.steps:
        if s.device not in wf.devices:
            raise ValueError(f"step {s.id}: unknown device {s.device!r}")
        missing = set(s.depends_on) - known
        if missing:
            raise ValueError(f"step {s.id}: unknown dependencies {sorted(missing)}")

    t0_steps = [s.id for s in wf.steps if s.marks_t0]
    if len(t0_steps) > 1:
        raise ValueError(f"more than one step marks t0: {t0_steps}")

    # Cycle check (depth-first search) and "t0 is an ancestor of every timed step".
    ancestors: dict[str, set[str]] = {}

    def collect(step_id: str, path: tuple[str, ...]) -> set[str]:
        if step_id in path:
            raise ValueError(f"dependency cycle: {' -> '.join(path + (step_id,))}")
        if step_id not in ancestors:
            result: set[str] = set()
            for dep in wf.step(step_id).depends_on:
                result |= {dep} | collect(dep, path + (step_id,))
            ancestors[step_id] = result
        return ancestors[step_id]

    for s in wf.steps:
        collect(s.id, ())
        if s.start_after_t0_s is not None and not (t0_steps and t0_steps[0] in ancestors[s.id]):
            raise ValueError(f"step {s.id} is timed relative to t0 but does not depend on the marks_t0 step")
