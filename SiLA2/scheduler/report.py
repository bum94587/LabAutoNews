"""Turn a run's timeline, well volumes and firmware trace into plots and a Markdown summary.

- `write_gantt`          one row per device, steps as bars, t0 and the planned time points,
                         plus the heater-shaker temperature streamed by SetTemperature.
- `write_plate_volumes`  four 8x12 heat maps (the twin's tracked volume per well).
- `write_summary`        run_summary.md: steps, timings, time points, temperatures, firmware
                         command counts and final volumes.

Inputs are the plain dicts/JSON that run_demo.py collects, so this module has no SiLA code.
"""

from __future__ import annotations

import re
from collections import Counter
from pathlib import Path
from typing import Any

import matplotlib

matplotlib.use("Agg")  # headless: render straight to files
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import Patch  # noqa: E402

ROWS = "ABCDEFGH"
PLATES = ["compounds", "nadph", "reaction", "quench"]
# Nominal starting volumes from PLAN.md (uL/well); the twin may scale them, see InstrumentInfo.
NOMINAL_START_UL = {"compounds": 200.0, "nadph": 200.0, "reaction": 300.0, "quench": 150.0}

# Categorical colours (validated default palette of the dataviz guidance), by command family.
COLORS = {
    "transfer": "#2a78d6",  # blue: liquid transfers
    "temperature": "#eb6834",  # orange: SetTemperature
    "shaking": "#1baf7a",  # aqua: Start/StopShaking
    "other": "#6250d6",  # violet: Initialize, read-outs
}
INK, MUTED, GRID = "#0b0b0b", "#52514e", "#d9d8d4"
FAILED = "#e34948"

# Hamilton STAR firmware commands are <module><command>, e.g. "C0TP" = master module, tip pick-up.
FIRMWARE_CODES = {
    "C0TP": "pick up tips",
    "C0TR": "drop / return tips",
    "C0AS": "aspirate",
    "C0DS": "dispense",
    "C0DI": "initialise pipetting channels",
}


def family(command: str) -> str:
    if command in ("Transfer", "Aspirate", "Dispense", "PickUpTips", "DropTips"):
        return "transfer"
    if command == "SetTemperature":
        return "temperature"
    if command in ("StartShaking", "StopShaking"):
        return "shaking"
    return "other"


# ------------------------------------------------------------------ parsing


def well_grid(volumes: dict[str, Any]) -> list[list[float | None]]:
    """Map {well: volume} onto an 8x12 grid. Accepts "A1", "A01" or names ending in them."""
    grid: list[list[float | None]] = [[None] * 12 for _ in ROWS]
    for name, vol in volumes.items():
        m = re.search(r"([A-H])0?(\d{1,2})$", str(name))
        if m and 1 <= int(m.group(2)) <= 12 and isinstance(vol, (int, float)):
            grid[ROWS.index(m.group(1))][int(m.group(2)) - 1] = float(vol)
    return grid


def column_mean(volumes: dict[str, Any], column: int) -> float | None:
    """Mean volume of one plate column (8 wells), or None if unknown."""
    vals = [row[column - 1] for row in well_grid(volumes) if row[column - 1] is not None]
    return sum(vals) / len(vals) if vals else None


def firmware_stats(trace: list[dict[str, Any]]) -> Counter:
    """Count firmware commands by <module><command> code; the 8 channel modules P1..P8 count as "Px"."""
    return Counter(re.sub(r"^P[1-8]", "Px", str(entry.get("command", ""))[:4]) for entry in trace)


def expected_column_volumes(timeline: dict[str, Any]) -> dict[tuple[str, int], float]:
    """Final volume per (plate, column) implied by the successful Transfers + PLAN start volumes."""
    expected: dict[tuple[str, int], float] = {}
    for step in timeline["steps"]:
        if step["command"] != "Transfer" or step["status"] != "succeeded":
            continue
        p = step["params"]
        src, dst, vol = (p["SourcePlate"], p["SourceColumn"]), (p["TargetPlate"], p["TargetColumn"]), p["VolumeUl"]
        for key, delta in ((src, -vol), (dst, +vol)):
            expected[key] = expected.get(key, NOMINAL_START_UL.get(key[0], 0.0)) + delta
    return expected


# -------------------------------------------------------------------- plots


def _style(ax) -> None:
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    for side in ("left", "bottom"):
        ax.spines[side].set_color(MUTED)
    ax.tick_params(colors=MUTED, labelsize=8)
    ax.grid(axis="x", color=GRID, linewidth=0.6)
    ax.set_axisbelow(True)


def write_gantt(timeline: dict[str, Any], path: Path) -> None:
    """Gantt chart of the run (one row per device) with a temperature panel underneath."""
    steps = [s for s in timeline["steps"] if s["start_s"] is not None]
    devices = list(timeline["devices"])  # file order: lh, hhs
    temps = [
        (pt["t_s"], pt["CurrentTemperature"])
        for s in steps
        if s["command"] == "SetTemperature"
        for pt in s["intermediates"]
        if "CurrentTemperature" in pt
    ]
    fig, axes = plt.subplots(
        2 if temps else 1, 1, figsize=(11, 5.2 if temps else 3.4), sharex=True,
        gridspec_kw={"height_ratios": [2.2, 1.3]} if temps else None, squeeze=False,
    )
    ax = axes[0][0]
    _style(ax)
    ypos = {d: len(devices) - 1 - i for i, d in enumerate(devices)}
    end = max([s["end_s"] or s["start_s"] for s in steps] + [timeline["duration_s"]])
    min_width = end * 0.004  # instant commands (StopShaking) still get a visible sliver

    _draw_shaking_bands(ax, steps, ypos)
    for s in steps:
        width = max((s["end_s"] or end) - s["start_s"], min_width)
        failed = s["status"] == "failed"
        ax.barh(ypos[s["device"]], width, left=s["start_s"], height=0.5,
                color=COLORS[family(s["command"])], edgecolor=FAILED if failed else "white",
                linewidth=2 if failed else 0.8, hatch="//" if failed else None)
        if s["command"] == "Transfer":  # label above the bar: "compound", "nadph", "t0", "t1", ...
            ax.text(s["start_s"] + width / 2, ypos[s["device"]] + 0.3, s["id"].split("_")[-1],
                    ha="center", va="bottom", fontsize=7, color=MUTED)

    t0 = timeline.get("t0_s")
    if t0 is not None:
        for a in [row[0] for row in axes]:
            a.axvline(t0, color=INK, linestyle="--", linewidth=1)
        for s in steps:
            if s["planned_start_s"] is not None and s["start_after_t0_s"]:
                for a in [row[0] for row in axes]:
                    a.axvline(s["planned_start_s"], color=MUTED, linestyle=":", linewidth=0.9)
        scale = timeline["real_seconds_per_workflow_minute"]
        top = ax.secondary_xaxis("top", functions=(lambda x: (x - t0) / scale, lambda m: m * scale + t0))
        top.set_xlabel("workflow minutes since t0 (NADPH added); dotted = planned time points",
                       fontsize=8, color=MUTED)
        top.tick_params(colors=MUTED, labelsize=8)

    labels = {d: f"{d.upper()}\n{timeline['devices'][d]['feature']}" for d in devices}
    ax.set_yticks([ypos[d] for d in devices], [labels[d] for d in devices], fontsize=8, color=INK)
    ax.set_ylim(-0.7, len(devices) - 0.3)
    handles = [Patch(color=c, label=n) for n, c in
               [("Transfer", COLORS["transfer"]), ("SetTemperature", COLORS["temperature"]),
                ("Start/StopShaking (band = shaking)", COLORS["shaking"]),
                ("Initialize / read-outs", COLORS["other"])]]
    ax.legend(handles=handles, fontsize=7, loc="upper center", bbox_to_anchor=(0.5, -0.12 if not temps else -0.04),
              ncol=4, frameon=False)
    status = timeline["run_status"]
    ax.set_title(f"{timeline['workflow']}: run {status}, {timeline['duration_s']:.1f} s real time",
                 fontsize=10, color=INK, loc="left", pad=28)

    if temps:
        tax = axes[1][0]
        _style(tax)
        tax.plot([t for t, _ in temps], [v for _, v in temps], color=COLORS["temperature"], linewidth=2)
        tax.set_ylabel("HHS block (C)", fontsize=8, color=MUTED)
        tax.grid(axis="y", color=GRID, linewidth=0.6)
    axes[-1][0].set_xlabel("seconds since run start (real time)", fontsize=8, color=MUTED)
    fig.tight_layout()
    fig.savefig(path)  # format from the suffix (.svg)
    plt.close(fig)


def _draw_shaking_bands(ax, steps: list[dict[str, Any]], ypos: dict[str, int]) -> None:
    """Thin band under the HHS lane from each StartShaking to the next StopShaking."""
    start = None
    for s in sorted(steps, key=lambda s: s["start_s"]):
        if s["command"] == "StartShaking" and s["status"] == "succeeded":
            start = s["end_s"]
        elif s["command"] == "StopShaking" and start is not None:
            ax.barh(ypos[s["device"]] - 0.36, s["start_s"] - start, left=start, height=0.1,
                    color=COLORS["shaking"], alpha=0.5, linewidth=0)
            start = None


def write_plate_volumes(volumes: dict[str, dict[str, Any]], path: Path) -> None:
    """2x2 heat maps of the four plates on one shared volume scale, wells annotated in uL."""
    grids = {p: well_grid(volumes.get(p, {})) for p in PLATES}
    vmax = max([v for g in grids.values() for row in g for v in row if v is not None] + [1.0])
    fig, axes = plt.subplots(2, 2, figsize=(12, 7))
    image = None
    for ax, plate in zip(axes.flat, PLATES):
        grid = grids[plate]
        data = [[float("nan") if v is None else v for v in row] for row in grid]
        image = ax.imshow(data, cmap="Blues", vmin=0, vmax=vmax, aspect="equal")
        for r, row in enumerate(grid):
            for c, v in enumerate(row):
                if v is not None:
                    ax.text(c, r, f"{v:.0f}", ha="center", va="center", fontsize=6.5,
                            color="white" if v > 0.6 * vmax else INK)
        ax.set_xticks(range(12), [str(i) for i in range(1, 13)], fontsize=7, color=MUTED)
        ax.set_yticks(range(8), list(ROWS), fontsize=7, color=MUTED)
        ax.tick_params(length=0)
        for spine in ax.spines.values():
            spine.set_visible(False)
        ax.set_title(f"{plate} (start {NOMINAL_START_UL[plate]:.0f} uL/well nominal)",
                     fontsize=9, color=INK, loc="left")
    cbar = fig.colorbar(image, ax=axes, shrink=0.8, label="tracked volume (uL)")
    cbar.ax.tick_params(labelsize=8)
    fig.suptitle("Final well volumes in the STAR twin (PyLabRobot volume tracking)", fontsize=11, color=INK,
                 x=0.06, ha="left")
    fig.savefig(path)  # format from the suffix (.svg)
    plt.close(fig)


# ------------------------------------------------------------------ summary


def _fmt(v: Any, digits: int = 2) -> str:
    if v is None:
        return "-"
    return f"{v:.{digits}f}" if isinstance(v, float) else str(v)


def write_summary(timeline: dict[str, Any], volumes: dict[str, dict[str, Any]], trace: list[dict[str, Any]],
                  instrument_info: str, path: Path) -> str:
    """Write run_summary.md and return its text."""
    steps = timeline["steps"]
    t0 = timeline.get("t0_s")
    scale = timeline["real_seconds_per_workflow_minute"]
    by_status = Counter(s["status"] for s in steps)
    lines = [
        "# Run summary: SiLA 2 digital-twin POC",
        "",
        f"- Workflow: **{timeline['workflow']}**",
        f"- Result: **{timeline['run_status'].upper()}**: "
        + ", ".join(f"{n} {k}" for k, n in sorted(by_status.items())),
        f"- Started {timeline['run_started_wall']} (UTC), real duration {timeline['duration_s']:.2f} s",
        f"- Time scale: 1 workflow minute = {scale:g} s real; t0 (NADPH added) at "
        f"{_fmt(t0)} s after run start",
        "",
        "## Liquid handler twin (InstrumentInfo)",
        "",
        "```",
        instrument_info.strip() or "n/a",
        "```",
        "",
        "## Steps",
        "",
        "| step | device | command | start (s) | duration (s) | late (s) | status | intermediates | result |",
        "|---|---|---|---:|---:|---:|---|---:|---|",
    ]
    for s in steps:
        result = s["error"] or "; ".join(f"{k}={_fmt(v)}" for k, v in s["responses"].items())
        result = result.replace("|", "/").replace("\n", " ")
        if len(result) > 80:
            result = result[:77] + "..."
        lines.append(f"| {s['id']} | {s['device']} | {s['command']} | {_fmt(s['start_s'])} | "
                     f"{_fmt(s['duration_s'])} | {_fmt(s['late_s'])} | {s['status']} | "
                     f"{s['intermediate_count']} | {result} |")

    lines += _timepoint_section(steps, t0, scale)
    lines += _temperature_section(steps)
    lines += _firmware_section(trace)
    lines += _volume_section(timeline, volumes)
    lines += [
        "",
        "## Files",
        "",
        "- `timeline.json`: every step with start/end, status, responses and intermediate responses",
        "- `firmware_trace.json`: Hamilton firmware command strings sent to the simulated STAR, with replies",
        "- `well_volumes.json`: tracked volume of every well of the four plates",
        "- `gantt.svg`, `plate_volumes.svg`: plots of the above",
        "- `run_log.txt`: scheduler live log; `logs/lh_twin.log`, `logs/hhs_twin.log`: server output",
        "",
    ]
    text = "\n".join(lines)
    path.write_text(text)
    return text


def _timepoint_section(steps: list[dict[str, Any]], t0: float | None, scale: float) -> list[str]:
    """Nominal vs effective sampling times: the quench happens at the end of each sample Transfer."""
    out = ["", "## Time points", ""]
    timed = {s["id"]: s for s in steps if s["start_after_t0_s"] is not None}
    samples = [s for s in steps if s["command"] == "Transfer" and s["params"].get("TargetPlate") == "quench"]
    if t0 is None or not samples:
        return out + ["No time points ran."]
    out += ["| sample | nominal (min) | due (s) | stop-shake late (s) | quenched at (min after t0) | status |",
            "|---|---:|---:|---:|---:|---|"]
    for s in samples:
        trigger = next((timed[d] for d in s["depends_on"] if d in timed), None)
        nominal = trigger["start_after_t0_s"] / 60 if trigger else None
        quenched = (s["end_s"] - t0) / scale if s["end_s"] is not None else None
        out.append(f"| {s['id']} -> quench col {s['params']['TargetColumn']} | {_fmt(nominal, 1)} | "
                   f"{_fmt(trigger['planned_start_s'] if trigger else None)} | "
                   f"{_fmt(trigger['late_s'] if trigger else None)} | {_fmt(quenched)} | {s['status']} |")
    out += ["", "Effective time = end of the sampling Transfer (aliquot dispensed into acetonitrile). "
            "The gap to nominal is the Transfer's own duration in workflow minutes; a real method "
            "would start each sampling step early by that amount."]
    return out


def _temperature_section(steps: list[dict[str, Any]]) -> list[str]:
    out = ["", "## Temperatures (heater-shaker twin)", ""]
    for s in steps:
        if s["command"] != "SetTemperature":
            continue
        temps = [p["CurrentTemperature"] for p in s["intermediates"] if "CurrentTemperature" in p]
        start = f"from {temps[0]:.1f} C " if temps else ""
        out.append(f"- `{s['id']}`: target {s['params'].get('TargetTemperature')} C, {start}reached "
                   f"{_fmt(s['responses'].get('ReachedTemperature'))} C in {_fmt(s['duration_s'])} s real "
                   f"({s['intermediate_count']} CurrentTemperature updates); status {s['status']}")
    return out


def _firmware_section(trace: list[dict[str, Any]]) -> list[str]:
    out = ["", "## Firmware trace (simulated Hamilton STAR)", ""]
    if not trace:
        return out + ["No firmware trace available."]
    counts = firmware_stats(trace)
    no_reply = sum(1 for e in trace if e.get("reply") in (None, ""))
    out += [f"{len(trace)} firmware commands were sent to the STAR simulator "
            f"({no_reply} action commands without a reply: the simulator only answers read commands).", ""]
    if any("operation" in e for e in trace):
        per_op = Counter(e.get("operation", "?") for e in trace)
        out += ["Per twin operation (in order of first use):", "", "| operation | commands |", "|---|---:|"]
        out += [f"| {op} | {n} |" for op, n in per_op.items()]
        out.append("")
    out += ["Liquid-handling actions (`TP`/`TR`/`AS`/`DS`: one each per Transfer):", "", "| code | count | meaning |", "|---|---:|---|"]
    out += [f"| `{code}` | {counts.get(code, 0)} | {meaning} |" for code, meaning in FIRMWARE_CODES.items()]
    out += ["", "Most frequent codes overall (`Px` = any of the 8 pipetting channels; a command starting "
            "with `R` is a request/read, e.g. `RZ` Z position, `RD` dispensing-drive position, "
            "`RY` Y position):", "", "| code | count |", "|---|---:|"]
    out += [f"| `{code}` | {n} |" for code, n in counts.most_common(10)]
    example = next((e for e in trace if str(e.get("command", "")).startswith("C0AS")), trace[0])
    command = str(example.get("command"))
    if len(command) > 160:
        command = command[:160] + f"... ({len(command)} chars)"
    out += ["", "Example (first aspirate, cut):", "", "```", f"> {command}", f"< {example.get('reply')}", "```"]
    return out


def _volume_section(timeline: dict[str, Any], volumes: dict[str, dict[str, Any]]) -> list[str]:
    out = ["", "## Final volumes (column means, uL)", ""]
    if not volumes:
        return out + ["No well volumes available."]
    expected = expected_column_volumes(timeline)
    out += ["| plate | column | twin | expected from workflow + PLAN start volumes |", "|---|---:|---:|---:|"]
    for (plate, col), exp in sorted(expected.items(), key=lambda kv: (PLATES.index(kv[0][0])
                                                                    if kv[0][0] in PLATES else 9, kv[0][1])):
        out.append(f"| {plate} | {col} | {_fmt(column_mean(volumes.get(plate, {}), col), 1)} | {exp:.1f} |")
    out += ["", "Columns not listed were not touched by the workflow."]
    return out
