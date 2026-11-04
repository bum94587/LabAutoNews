"""Tiny two-lane workflow scheduler for the SiLA 2 digital-twin POC.

- `scheduler.workflow`  loads and checks `workflow.yaml` (steps, dependencies, timing).
- `scheduler.scheduler` runs it against SiLA 2 features, one worker thread per device.
- `scheduler.report`    turns the recorded timeline into SVG plots and a Markdown summary.
"""
