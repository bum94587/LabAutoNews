# Deep dive: Orchestration and data for ADME labs, 2026-11-04
Scope: the scheduler layer between instruments and data. Builds on the SiLA 2 / LADS items of 2026-11-03. Page fetches were limited here; Orca facts are from its GitHub pages. Search found no new vendor scheduler news in the window.

## TL;DR
- Open-source schedulers are arriving: Orca (Cheshire Labs) reached v2.3.0 with a daemon, REST API and audit log [1][2].
- Licence matters: Orca moved from AGPL-3.0 to SSPL in v2.0.0 [1] (SSPL is not OSI-approved; that is analysis, not in the source).
- Scheduling is the missing middle: PyLabRobot drives devices, SiLA 2 standardises device calls, but neither plans parallel plate flow (see 2026-11-03 items).

## What a scheduler does (learn-a-topic)
An ADME run (microsomal stability, Caco-2, plasma protein binding) is many plates with timed steps: incubate, quench at fixed time points, centrifuge, hand to the LC-MS. A scheduler decides which plate uses which device when, so timed steps are not missed while the arm is busy. Orca expresses this as plain Python workflows with reservation-based device booking [1].

## What Orca 2.x adds
- A persistent local daemon with REST/SSE interface and a CLI [1].
- Simulation can be paced faster than real time, so a protocol can be dry-run before touching hardware [2].
- Audit rows with an optional reason, and unique labware barcodes [2]. These are the traceability basics a GxP-minded lab asks for. (Analysis: whether this meets any regulated-use bar is untested.)
- Caveat (unverified, from a search summary of the README): the daemon is reported to have no authentication, so it should stay on localhost.

## AI agents
Agents can already reach devices through MCP wrappers (SiLA, PyLabRobot, Opentrons), only in simulation so far (see 2026-11-02/03 items). A scheduler with an audit log and simulation mode is the natural gate between an agent's plan and real hardware. This is speculation, not a shipped product.

## What to watch
- Whether Orca or a similar scheduler gets a vendor-backed or LIMS/ELN integration.
- Any SiLA/LADS liquid-handling feature standard.
- Real ADME labs publishing scheduler-driven throughput.

## References
[1] Orca v2.0.0 PR, Cheshire Labs, 2026-09-23 (primary): https://github.com/Cheshire-Labs/orca/pull/14
[2] Orca v2.3.0 release notes, Cheshire Labs, 19 Oct (primary): https://github.com/Cheshire-Labs/orca/releases/tag/v2.3.0

> **Rate:** _/5 · **Tags:** _ · `LAN-D20261104`
