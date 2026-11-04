# Feature: PyLabRobot from the inside: how open-source, hardware-agnostic lab automation works, and where AI agents plug in, 2 Nov 2026

Verifier (independent agent, 3 Nov): 8 key claims verified, 3 partly verified, none contradicted; corrections applied, including two fixes to the code sketch. Badges: ✅ verified · 🟡 partly verified · 🔬 sound · ⚠️ questionable.

Scope: a guided read of the PyLabRobot source code at commit [`7779f50`](https://github.com/PyLabRobot/pylabrobot/commit/7779f506d12755f5f274b4c5cab4d095f4fccb62) (3 Nov 2026) and its git history, plus public work on AI agents and closed-loop labs, with a DMPK worked example. Code links are primary sources; analysis and opinion are labelled.

## TL;DR

- **PyLabRobot (PLR) is a pure-Python, MIT-style open-source library that talks to lab robots at the firmware level**, from Hamilton STARs and Opentrons to plate readers, sealers and arms: 84 devices in its registry, 50 of them on the new "v1" API [1][2][3]. ✅
- **It is in the middle of a big rewrite.** The famous "one protocol, any robot" front end now lives under `pylabrobot.legacy`; new drivers are one plain Python class per device that exposes the machine's real parameters (the v1 STAR `aspirate` takes 33 arguments) [4][5][6]. ✅🔬
- **Development is fast and AI-assisted**: 790 commits from 53 people in the last 12 months, and 54% of them credit an AI coding assistant as co-author, rising to 80% since October [7]. 🟡🔬
- **At run time there is no built-in "AI agent" in PLR.** Third-party MCP servers and demos drive it, but only in simulation, behind human confirmation gates; no public example drives a real liquid handler through PyLabRobot [8][44][45][46]. ✅🔬
- **For a DMPK lab, PLR can already run the liquid handling, 37 °C shaking, plate moves, sealing and centrifugation of a microsomal stability assay**, but not the LC-MS/MS readout or a Caco-2 TEER check; that is where the loop still has to be closed by other software [3][11]. 🟡

## Why a DMPK scientist should care

Most ADME screening runs on liquid handlers whose method editors (Hamilton VENUS, Tecan EVOware/FluentControl, Beckman Biomek) are Windows programs with their own scripting languages. That is fine until you want the robot to do something its editor did not anticipate: change a timepoint because the compound is clearly unstable, re-run an outlier, or let a model choose the next experiment. PyLabRobot's pitch is that every step becomes an ordinary Python call you can put inside an `if` statement or a loop. Its README calls this "Turing-complete protocols that include feedback loops" [1]. The project began in August 2022 (first commit by Rick Wierenga) and was described in a 2023 paper in Cell Press's *Device* [1][12].

## Two architectures living side by side

**The classic design (now "legacy").** For its first four years PLR used a front end/back end split. You wrote your protocol against one universal `LiquidHandler` class, and a back end translated each call into a particular robot's firmware commands. The README still shows the idea: the same `pick_up_tips` / `aspirate` / `dispense` lines run on a Hamilton STAR, an Opentrons OT-2 or a Tecan EVO; only the back-end line changes [1]:

```python
lh = LiquidHandler(backend=STARBackend(), deck=deck)
await lh.pick_up_tips(lh.deck.get_resource("tip_rack")["A1"])
await lh.aspirate(lh.deck.get_resource("plate")["A1"], vols=100)
await lh.dispense(lh.deck.get_resource("plate")["A2"], vols=100)
# ...or: LiquidHandler(backend=OpentronsOT2Backend(host="x.x.x.x"), deck=deck)
# ...or: LiquidHandler(backend=EVOBackend(), deck=deck)
```

Every back end implements the same abstract interface, `LiquidHandlerBackend`, whose required methods are `pick_up_tips`, `drop_tips`, `aspirate`, `dispense`, their 96-head versions, and `pick_up_resource` / `move_picked_up_resource` / `drop_resource` for the gripper [13]. Each single-channel aspiration is passed down as a small frozen record (`SingleChannelAspiration`: container, offset, tip, volume, flow rate, liquid height, blow-out air volume, mix) [14].

**The rewrite ("v1").** On 1 August 2026 a 759-file change (PR #1000, "v1b1 changes") moved that whole stack to `pylabrobot.legacy` and started a new layout, one package per vendor and device: `pylabrobot/hamilton/star`, `pylabrobot/bmg_labtech/vantastar`, `pylabrobot/brooks/precise_flex` [4][15]. Importing from the old path now raises a deprecation warning [16]. The contributor guide is blunt: "The old Driver/Backend split and capability machinery are deprecated — don't use them. Instead write a single plain class whose public methods are the device's operations" [5].

The STAR's own design note explains the new shape in 21 numbered rules [6]. A few worth knowing:

- **One driver, features hang off it** (P1): `pipettes`, `head96`, `head384`, `iswap`, `autoload`, `x_arm`, `cover` are plain classes on one `STARDriver` [6].
- **Nothing exists until the device says it is fitted** (P2): features are built from what the instrument reports at setup, so a STAR without an iSWAP simply has `iswap = None` [6].
- **The wire counts in increments; the driver speaks mm, degrees, µL and seconds** (P4) [6].
- **The device is the authority on where it is** (P8): after every move the driver reads the drive back, so the model matches where the arm actually stopped, even after an error [6].
- **Tests assert the wire** (P15): a test compares the exact firmware string a method would send [6].

*Analysis:* the trade-off is deliberate. The legacy layer hid each robot behind a lowest common denominator. In v1, the STAR's `pipettes.aspirate` exposes the knobs a Hamilton method developer actually tunes: liquid-level detection mode, immersion depth, surface following, clot detection height, settling time, transport air, liquid class and more, 33 arguments in all [17]. Universality is no longer promised by one class; the hardware registry still lists the STAR's production entry as v0 ("full") while the v1 driver matures [3].

## The resource model: the deck as a tree

Everything physical in PLR (deck, carrier, plate, well, tip rack, tip spot, trough, even the reader's plate holder) is a `Resource`: a named box with `size_x/size_y/size_z`, a location relative to its parent, and a list of children [18]. Absolute positions are computed by walking up the tree and adding each child's offset, with rotations applied; `get_absolute_location(x="c", y="c", z="t")` gives, for example, the centre of a well's top [19].

Labware comes as factory functions named after the catalogue item, such as `cor_96_wellplate_2mL_Vb` (a Corning 2 mL V-bottom deep-well plate) or `hamilton_96_tiprack_300uL_filter` [20][21]. Hamilton carriers (`PLT_CAR_L5AC_A00`, `TIP_CAR_480_A00`) and decks (`STARDeck`) are modelled the same way [22][23][24]. Volume and tip tracking can be switched on globally (`set_volume_tracking`, `set_tip_tracking`), so the software knows what should be in each well and which tips are used [25][26].

*Why it matters:* because the deck is data, a program (or an agent) can inspect it, check whether a move makes sense, and draw it before any hardware moves.

## Plate readers: VANTAstar and CLARIOstar

Readers show the v1 style clearly. BMG's VANTAstar driver arrived on 2 November 2026 (PR #1574, by Niklas Hölter, co-authored with Camillo Moschner and an AI assistant) and talks to the reader over native USB, with no vendor DLL [27][28]. The device is a `Resource` whose plate holder refuses a plate unless the drawer was last sensed open [29]:

```python
def _require_drawer_open(self, action: str) -> None:
    if self._drawer.drawer_open is None:
      raise RuntimeError(f"cannot {action}: the drawer has not been sensed; open it first")
```

Its `absorbance.measure(wavelengths, plate=..., wells=...)` reads 1 to 8 wavelengths (220–1000 nm) and documents that optical density is computed as BMG's own Voyager software computes it, not pathlength-corrected [30]. The changelog records what was tested: one reader, firmware 1.12, with luminescence untested [2]. Getting there needed a transport fix: `pylabrobot.io.USB` gained a `zero_length_packets` option because the VANTAstar does not accept the zero-length USB packet most devices expect [2][31].

The CLARIOstar driver was rebuilt in v1 over the second half of October: fluorescence through several channels and as spectra, luminescence, filter detection, z-profiles, refusing to read with the drawer out, and saving reads to disk as they are measured "as one table any program can follow" [32].

## Arms: PreciseFlex, vision and "Z-touch"

The Brooks PreciseFlex PF400 is a collaborative SCARA arm common in workcells. Between 29 October and 2 November 2026 its driver gained a device model with a simulated arm (PR #1550), a refusal of any move that would bring the gripper within reach of its own column or base plate (#1551), force-limited gripper closes (#1552), the IntelliGuide camera as a "vision" feature (#1564), force-sensed Z probing (#1577) and a safer setup that releases the arm if setup fails (#1586) [33].

The Z-touch method is a good example of what "drive the primitives from Python" means. `probe_z_using_ztouch` lowers the arm until the gripper presses with a set force (15 N by default) and returns the height, or `None` if nothing was met [34]:

```python
async def probe_z_using_ztouch(self, *, search_start_position=None, search_end_position=None,
    approach_speed_percent=None, search_speed_percent=None, detection_force: float = 15.0, ...)
    -> Optional[float]:
  """Lower the arm until the gripper presses on something, and read the height."""
```

The vision feature is built only when the controller reports a vision server, and its docstring notes that "Nothing here moves the arm"; `capture_image` retrieves frames from the camera [35]. *Analysis:* a camera you can call from Python, on an arm you can call from Python, is exactly the kind of sensor an AI agent would use to check a plate's position before a pick.

## Simulators and visualizers

The old stand-alone simulator was retired in favour of a browser-based Visualizer [36]. In v1, simulation moved into each driver: the STAR's simulator "overrides only what would reach the wire", one subclass per feature, so discovery, initialisation and locking run exactly as they would against hardware (P14) [6]. `STAR(simulation=True)` builds a simulated STAR from a recorded configuration of a real instrument [37]. A new 3D viewer (`visualizer3D`, September 2026) renders a whole facility, not just one liquid handler [38]. Legacy "chatterbox" back ends simply print every operation, useful for dry runs [39].

## How a new device driver gets written

The device-driver guide reads like a checklist, and it says it was written "for humans and agents" [5]:

- **Extract, don't guess**: work from firmware docs, logs or captures, byte-exact [5].
- **One plain class**, talking through a `pylabrobot.io` transport (USB, serial, FTDI, HID, socket), never a vendor DLL, so it runs on Windows, macOS and Linux [5].
- **Keep the logic client-side**: prefer the device's primitives over opaque on-device macros, so sequencing and decisions live in readable Python [5].
- **Idempotent public API**: no blind toggles; expose "move to state" methods instead [5].
- **Say loudly if untested**: `setup()` should log a warning until someone verifies it on hardware [5].
- Ship a **hello-world notebook** and a **registry entry** in `docs/_static/devices.json` [5][3].

The repository's `AGENTS.md`, aimed at AI coding agents, adds one rule above all: "Never drive real hardware without explicit, per-run approval" [8].

## Who is building it, and how fast

Counting from `git log` at commit 7779f50 [7]:

| Period | Commits | With an AI co-author credit |
|---|---:|---:|
| Nov–Dec 2025 | 141 | 9% |
| Jan–Mar 2026 | 178 | 56% |
| Apr–Jun 2026 | 90 | 69% |
| Jul–Sep 2026 | 276 | 62% |
| Oct–3 Nov 2026 | 105 | 80% |

- **790 commits, 53 distinct authors, ~533,000 lines added** over the 12 months; September 2026 alone had 205 commits as the v1 drivers landed [7].
- **Two people do most of the work:** Camillo Moschner (389 commits) and project founder Rick Wierenga (266) [7].
- **Since May 2026 the busiest areas** are `hamilton` (STAR and Prep drivers), `legacy`, `resources`, `bmg_labtech` and `brooks` [7].
- **AI co-authors are mostly Claude models** (444 trailers) with some GitHub Copilot (60) [7]. Trailers are added voluntarily, so this is a floor, not a full count.

*Analysis:* this is one of the clearest public examples of a lab-automation codebase being written largely with AI coding assistants. The trailers show disclosed AI help, not how much of the code an AI wrote. The style rules (P1–P21, byte-exact protocols, "tests assert the wire") look designed to keep that kind of fast, AI-assisted output checkable.

## Where AI agents plug in

**First, what PLR itself ships: nothing agent-specific at run time.** A search of the repository finds no LLM, agent or MCP (Model Context Protocol, the open standard for exposing tools to AI assistants) code; the only "MCP" strings are Brooks error messages about the arm's Manual Control Pendant [11]. What PLR offers is the set of doors an agent needs: a typed async Python API, simulators that answer like the hardware, an event bus that is "an observation mechanism, not a control mechanism" [9], and optional gRPC device services whose listener "does not authenticate callers" and is meant to sit behind SSH [10].

**Other people are building the agent layer on top, all of it in simulation so far.**

- **plr-mcp** wraps a PyLabRobot liquid handler, plate reader, thermocycler and heater-shaker as MCP tools. It runs on PLR's chatterbox back end by default, tags motion tools as destructive so the AI client must ask first, and requires `confirm=true` before its one real-STAR protocol runs [44]:

```python
@mcp.tool(name="plr_drop_tips",
          annotations=ToolAnnotations(title="Drop tips", readOnlyHint=False, destructiveHint=True, ...))
```

- **OpenLabAI** puts an AI agent in front of OT-2, Hamilton, Biomek and Cellario servers; its Hamilton server writes PyLabRobot protocols and dry-runs them, and states plainly that it "does not execute protocols on a physical Hamilton" [45].
- **labloop**, a public demo from October 2026, joins Bayesian optimisation, a scheduler and an LLM to PLR: every plate is pipetted on a simulated STARlet through `STARChatterboxBackend` [46].
- **Labwire** exposes a PLR liquid handler through an "agent-to-instrument" protocol; per its forum post it uses hardware-free back ends only [47]. An agent "skill" for writing PLR protocols carries a "non-negotiable hardware boundary": never command physical equipment automatically [48].

We found no public example of an AI agent driving a physical liquid handler through PyLabRobot (outside PLR, Coscientist and CRESt did drive real Opentrons robots [50][51]). ✅🔬 *Analysis:* the pattern these projects converge on (simulate by default, label destructive tools, require an explicit human "go", tag every result as simulated or real) is the same rule PLR's `AGENTS.md` sets for coding agents [8].

**The most mature commercial path is Opentrons'.** The OpentronsAI protocol-writing assistant was launched in February 2024 and is open source in the Opentrons monorepo; its server now defaults to an Anthropic Claude model, with an older OpenAI path still present, and gives the model exactly two tools, `simulate_protocol` and `get_relevant_api_docs` [49]. The landmark academic system, Coscientist (*Nature*, December 2023), had GPT-4 plan and run palladium-catalysed couplings on an Opentrons robot; its public repository holds supporting data but no robot code [50].

**How an optimiser hands the next experiment to a robot.** Every closed-loop framework we read uses the same "ask/tell" loop, and none ships a robot driver; the robot side is your own glue code, which is where PLR fits [52][53][54][55]:

| Framework | Ask | Tell |
|---|---|---|
| BayBE (Merck KGaA) | `campaign.recommend(batch_size=...)` returns a table of conditions | `campaign.add_measurements(df)` |
| Ax (Meta) | `client.get_next_trials(...)` | `client.complete_trial(...)` |
| Atlas (Aspuru-Guzik group) | `planner.recommend(observations)` | `campaign.add_observation(...)` |
| MADSci (Argonne) | logic in an `ExperimentScript` | `workcell_client.start_workflow(...)`, results read back as datapoints |

CRESt (MIT) shows the glue in practice: Ax proposes the next batch, a GPT front end insists on three human confirmations (`recipe_confirm`, `ot2_deck_check`, `start`), then posts the recipes to a small web service on the OT-2's computer [51]. On the standards side, a SiLA 2 "feature" is an XML definition of typed commands and properties from which a server and client are generated [56], a self-describing format close to what an AI tool schema needs; PLR can discover SiLA 1 and 2 devices on the network [57].

**What the evidence says about letting models write protocols.** In a 5 February 2026 company preprint, OpenAI and Ginkgo report GPT-5 designing about 36,000 cell-free protein-synthesis reactions run on Ginkgo's automation, cutting cost per gram by 40%, with every design checked against a strict schema before execution and humans doing the reagent prep [58]. ✅ Benchmarks are sobering: in LabSafety Bench (*Nature Machine Intelligence*, January 2026) no model scored above 70% on hazard identification [59] 🟡, and early GPT-4 work on OT-2 scripts found simulators catch syntax and API errors but not experiments that are scientifically wrong [60]. *Analysis:* simulation checks that a protocol *runs*; it does not check that it measures CLint correctly.

**DMPK specifically.** We found no public, AI-driven closed-loop microsomal stability or permeability workflow. The closest are commercial "lab-in-the-loop" ADMET offers, such as ADME-One from Ginkgo Datapoints, Inductive Bio and Tangible Scientific (launched 26 May 2026), where models pick compounds, an automated lab runs a Tier-1 ADME panel and the results retrain the models [61], and Novartis' MicroCycle miniaturised design-make-test platform (*J. Med. Chem.* 2024) [62]. Our [2 Nov deep dive on closed-loop DMTA](2026-11-02_deepdive-closed-loop-dmta.md) covers the pharma deployments.


## Worked example: a microsomal stability assay on PyLabRobot

**The assay.** Human liver microsomes (HLM) plus NADPH metabolise the test compound at 37 °C; samples taken at several timepoints are quenched with cold acetonitrile containing an internal standard, spun down, and the supernatant is analysed by LC-MS/MS. The slope of ln(% remaining) against time gives the half-life and intrinsic clearance (CLint). Automated versions of exactly this, on Hamilton STAR-family robots, are well documented: AstraZeneca runs metabolic stability in HLM and rat hepatocytes, lipophilicity, solubility and plasma protein binding on three Hamilton Microlab STARplus systems with identical decks, for every new compound, weekly [40]; a harmonised microsomal format measures mouse, rat and human CLint together [41].

**A deck for one 8-compound run (illustrative).**

| Position | Item | PLR resource |
|---|---|---|
| Tip carrier | 300 µL filter tips | `TIP_CAR_480_A00` + `hamilton_96_tiprack_300uL_filter` [23][21] |
| Plate carrier, site 0 | Compound plate (10 µM in buffer) | `PLT_CAR_L5AC_A00` + `cor_96_wellplate_2mL_Vb` [22][20] |
| Plate carrier, site 1 | NADPH (start) plate | same |
| Plate carrier, site 2 | Quench plate: cold ACN + internal standard | same |
| Heater-shaker at 37 °C | Reaction plate: HLM in phosphate buffer (300 µL per well) | QInstruments `BioShakeQ1` (v1) [42][3] |

**The steps.** Pre-warm the reaction plate; add compound; start every row with NADPH and note the exact time; at each timepoint move one aliquot per compound into the quench plate; seal, centrifuge, and send to LC-MS/MS.

**An untested sketch** using real names from the repository (legacy universal API for the liquid handler, v1 class for the shaker). It has not been run on hardware or in a simulator; treat it as a reading aid, not a method.

```python
# UNTESTED SKETCH: illustrates the API shape only. Names checked against PLR @ 7779f50.
import asyncio, time
from pylabrobot.legacy.liquid_handling import LiquidHandler
from pylabrobot.legacy.liquid_handling.backends import STARBackend
from pylabrobot.resources import (Coordinate, STARDeck, TIP_CAR_480_A00, PLT_CAR_L5AC_A00,
    hamilton_96_tiprack_300uL_filter, cor_96_wellplate_2mL_Vb, set_volume_tracking)
from pylabrobot.qinstruments import BioShakeQ1

TIMEPOINTS_MIN = [0, 5, 15, 30, 45]          # one quench column per timepoint
ALIQUOT_UL, QUENCH_COLS = 50, range(len(TIMEPOINTS_MIN))

async def run():
    set_volume_tracking(True)                                # PLR keeps a running tally per well
    deck = STARDeck()
    tips = TIP_CAR_480_A00("tip_car");  tips[0] = hamilton_96_tiprack_300uL_filter("tips")
    plates = PLT_CAR_L5AC_A00("plate_car")      # PLT_CAR_L5AC (no suffix) raises at 7779f50
    plates[0] = compounds = cor_96_wellplate_2mL_Vb("compounds")
    plates[1] = nadph = cor_96_wellplate_2mL_Vb("nadph")
    plates[2] = quench = cor_96_wellplate_2mL_Vb("quench")
    deck.assign_child_resource(tips, track=1)               # `track=` replaced `rails=` in 2026
    deck.assign_child_resource(plates, track=7)
    shaker = BioShakeQ1("bioshake", port="/dev/ttyUSB0")   # BioShake3000T is not implemented
    deck.assign_child_resource(shaker, location=Coordinate(500, 100, 100))  # placement illustrative
    shaker.assign_child_resource(reaction := cor_96_wellplate_2mL_Vb("reaction"))
    # volume tracking needs starting volumes, or the first aspirate raises TooLittleLiquidError
    for plate, ul in [(compounds, 200), (nadph, 200), (reaction, 300), (quench, 150)]:
        for well in plate.children: well.tracker.set_volume(ul)   # 300 + 50 + 50 = 400 uL >= 5 x 50 uL samples

    lh = LiquidHandler(backend=STARBackend(), deck=deck)
    await lh.setup(); await shaker.setup()
    await shaker.set_temperature(37.0)

    tip_rack = deck.get_resource("tips")
    await lh.pick_up_tips(tip_rack["A1:H1"])                 # 8 channels = 8 compounds (column 1)
    await lh.aspirate(compounds["A1:H1"], vols=[50] * 8)
    await lh.dispense(reaction["A1:H1"], vols=[50] * 8)
    await lh.discard_tips()

    await lh.pick_up_tips(tip_rack["A2:H2"])                 # start the reaction
    await lh.aspirate(nadph["A1:H1"], vols=[50] * 8)
    await lh.dispense(reaction["A1:H1"], vols=[50] * 8)
    t0 = time.monotonic(); await lh.discard_tips()
    await shaker.start_shaking(speed=600)

    sampled_at = {}
    for i, t_min in enumerate(TIMEPOINTS_MIN):
        await asyncio.sleep(max(0, t0 + 60 * t_min - time.monotonic()))
        await shaker.stop_shaking()
        await lh.pick_up_tips(tip_rack[f"A{3 + i}:H{3 + i}"])
        await lh.aspirate(reaction["A1:H1"], vols=[ALIQUOT_UL] * 8)
        await lh.dispense(quench[f"A{1 + i}:H{1 + i}"], vols=[ALIQUOT_UL] * 8)
        sampled_at[t_min] = time.monotonic() - t0             # actual time, for the kinetic fit
        await lh.discard_tips(); await shaker.start_shaking(speed=600)
    return sampled_at   # quench plate -> seal, spin, LC-MS/MS (outside PLR)
```

The calls (`pick_up_tips`, `aspirate`, `dispense`, `discard_tips`, `start_shaking`, `set_temperature`) and resource names are taken from the repository, and the independent verifier checked each against the code at 7779f50 🟡 [43][42][20][21][22][23][24][25]; deck positions, volumes and the shaker placement are illustrative and would need checking on a real deck (and the 0-minute aliquot would normally be taken from a separate pre-quenched control well).

**What PLR does not cover yet (at 7779f50).**

- **No LC-MS/MS or acoustic-ejection-MS driver**: the readout, peak integration and CLint fit live outside PLR. See our [3 Nov deep dive on AEMS bioanalysis](2026-11-03_deepdive-bioanalysis-automation.md) for how that end is changing [11].
- **No Transwell/insert labware and no TEER meter**, so a Caco-2 permeability run would need custom resources and manual barrier checks [11].
- **Hamilton liquid classes for organic solvents** such as acetonitrile need care; v1's `aspirate` takes explicit `hamilton_liquid_classes`, but validating them for ACN quench is on you [17].
- **No GLP/21 CFR Part 11 features** (audit trail, e-signatures) are claimed anywhere in the repository; regulated work would need them added around PLR (*analysis*).

**Where an agent could close the loop (analysis, speculative).** Because every step above is a Python call and every time is recorded, a controller could: add extra early timepoints when the first two points show fast loss; re-run a compound whose 0-min response is out of range; or pick the next batch of compounds from a model's uncertainty. The simulator lets such a controller rehearse a plan before the real run, and AGENTS.md-style rules (per-run approval to move hardware) are a sensible pattern to keep a human in charge.

## What to watch

- **v1 coverage of liquid handling**: when the STAR's registry entry moves from v0 to v1, and whether a machine-agnostic layer returns on top of the v1 drivers [3][6].
- **Readers and arms as sensors**: VANTAstar/CLARIOstar reads saved as tables, PF400 vision and force probing are the raw material for closed-loop work [27][32][35].
- **Agent tooling around PLR**: whether MCP servers or similar wrappers become part of the project, and how they handle hardware approval [8].

## References

Code links point to commit 7779f50 (3 Nov 2026). "code" = repository file or commit, read directly from a git clone.

1. PyLabRobot README: [https://github.com/PyLabRobot/pylabrobot/blob/7779f506d12755f5f274b4c5cab4d095f4fccb62/README.md](https://github.com/PyLabRobot/pylabrobot/blob/7779f506d12755f5f274b4c5cab4d095f4fccb62/README.md#L13-L60) (code)
2. CHANGELOG, "Unreleased" section: [https://github.com/PyLabRobot/pylabrobot/blob/7779f506d12755f5f274b4c5cab4d095f4fccb62/CHANGELOG.md](https://github.com/PyLabRobot/pylabrobot/blob/7779f506d12755f5f274b4c5cab4d095f4fccb62/CHANGELOG.md) (code)
3. Device registry and support levels: [https://github.com/PyLabRobot/pylabrobot/blob/7779f506d12755f5f274b4c5cab4d095f4fccb62/docs/_static/devices.json](https://github.com/PyLabRobot/pylabrobot/blob/7779f506d12755f5f274b4c5cab4d095f4fccb62/docs/_static/devices.json), [https://github.com/PyLabRobot/pylabrobot/blob/7779f506d12755f5f274b4c5cab4d095f4fccb62/docs/user_guide/machines.md](https://github.com/PyLabRobot/pylabrobot/blob/7779f506d12755f5f274b4c5cab4d095f4fccb62/docs/user_guide/machines.md) (code)
4. PR #1000 "v1b1 changes", 1 Aug 2026, 759 files: [https://github.com/PyLabRobot/pylabrobot/commit/14a776625](https://github.com/PyLabRobot/pylabrobot/commit/14a776625) (code)
5. Device-driver guide: [https://github.com/PyLabRobot/pylabrobot/blob/7779f506d12755f5f274b4c5cab4d095f4fccb62/docs/contributor_guide/device-driver-guide.md](https://github.com/PyLabRobot/pylabrobot/blob/7779f506d12755f5f274b4c5cab4d095f4fccb62/docs/contributor_guide/device-driver-guide.md) (code)
6. STAR design note, patterns P1–P20: [https://github.com/PyLabRobot/pylabrobot/blob/7779f506d12755f5f274b4c5cab4d095f4fccb62/pylabrobot/hamilton/star/design.md](https://github.com/PyLabRobot/pylabrobot/blob/7779f506d12755f5f274b4c5cab4d095f4fccb62/pylabrobot/hamilton/star/design.md) (code)
7. Git history at 7779f50: `git log --since=2025-11-01`, authors and `Co-authored-by` trailers counted by LabAutoNews on 3 Nov 2026: [https://github.com/PyLabRobot/pylabrobot/commits/main](https://github.com/PyLabRobot/pylabrobot/commits/main) (code)
8. AGENTS.md: [https://github.com/PyLabRobot/pylabrobot/blob/7779f506d12755f5f274b4c5cab4d095f4fccb62/AGENTS.md](https://github.com/PyLabRobot/pylabrobot/blob/7779f506d12755f5f274b4c5cab4d095f4fccb62/AGENTS.md) (code)
9. EventBus contributor guide: [https://github.com/PyLabRobot/pylabrobot/blob/7779f506d12755f5f274b4c5cab4d095f4fccb62/docs/contributor_guide/event-bus.md](https://github.com/PyLabRobot/pylabrobot/blob/7779f506d12755f5f274b4c5cab4d095f4fccb62/docs/contributor_guide/event-bus.md) (code)
10. RPC (gRPC device services) README: [https://github.com/PyLabRobot/pylabrobot/blob/7779f506d12755f5f274b4c5cab4d095f4fccb62/pylabrobot/rpc/README.md](https://github.com/PyLabRobot/pylabrobot/blob/7779f506d12755f5f274b4c5cab4d095f4fccb62/pylabrobot/rpc/README.md) (code)
11. Repository tree at 7779f50 (no LC-MS, TEER or Transwell modules or resources found by search of `pylabrobot/`): [https://github.com/PyLabRobot/pylabrobot/tree/7779f506d12755f5f274b4c5cab4d095f4fccb62/pylabrobot](https://github.com/PyLabRobot/pylabrobot/tree/7779f506d12755f5f274b4c5cab4d095f4fccb62/pylabrobot) (code)
12. Wierenga R. et al., "PyLabRobot: An open-source, hardware-agnostic interface for liquid-handling robots and accessories", *Device* (2023): [https://www.cell.com/device/fulltext/S2666-9986(23)00170-9](https://www.cell.com/device/fulltext/S2666-9986(23)00170-9) (paper)
13. `LiquidHandlerBackend` abstract interface: [https://github.com/PyLabRobot/pylabrobot/blob/7779f506d12755f5f274b4c5cab4d095f4fccb62/pylabrobot/legacy/liquid_handling/backends/backend.py#L29-L136](https://github.com/PyLabRobot/pylabrobot/blob/7779f506d12755f5f274b4c5cab4d095f4fccb62/pylabrobot/legacy/liquid_handling/backends/backend.py#L29-L136) (code)
14. `SingleChannelAspiration`: [https://github.com/PyLabRobot/pylabrobot/blob/7779f506d12755f5f274b4c5cab4d095f4fccb62/pylabrobot/legacy/liquid_handling/standard.py#L53-L61](https://github.com/PyLabRobot/pylabrobot/blob/7779f506d12755f5f274b4c5cab4d095f4fccb62/pylabrobot/legacy/liquid_handling/standard.py#L53-L61) (code)
15. Vendor/device package layout: [https://github.com/PyLabRobot/pylabrobot/tree/7779f506d12755f5f274b4c5cab4d095f4fccb62/pylabrobot](https://github.com/PyLabRobot/pylabrobot/tree/7779f506d12755f5f274b4c5cab4d095f4fccb62/pylabrobot) (code)
16. Deprecation shim for `pylabrobot.liquid_handling`: [https://github.com/PyLabRobot/pylabrobot/blob/7779f506d12755f5f274b4c5cab4d095f4fccb62/pylabrobot/liquid_handling/__init__.py](https://github.com/PyLabRobot/pylabrobot/blob/7779f506d12755f5f274b4c5cab4d095f4fccb62/pylabrobot/liquid_handling/__init__.py) (code)
17. v1 STAR `Pipettes.aspirate`: [https://github.com/PyLabRobot/pylabrobot/blob/7779f506d12755f5f274b4c5cab4d095f4fccb62/pylabrobot/hamilton/star/driver/features/pipettes.py#L6101-L6140](https://github.com/PyLabRobot/pylabrobot/blob/7779f506d12755f5f274b4c5cab4d095f4fccb62/pylabrobot/hamilton/star/driver/features/pipettes.py#L6101-L6140) (code)
18. `Resource` base class: [https://github.com/PyLabRobot/pylabrobot/blob/7779f506d12755f5f274b4c5cab4d095f4fccb62/pylabrobot/resources/resource.py#L135-L200](https://github.com/PyLabRobot/pylabrobot/blob/7779f506d12755f5f274b4c5cab4d095f4fccb62/pylabrobot/resources/resource.py#L135-L200) (code)
19. `Resource.get_absolute_location`: [https://github.com/PyLabRobot/pylabrobot/blob/7779f506d12755f5f274b4c5cab4d095f4fccb62/pylabrobot/resources/resource.py#L347-L380](https://github.com/PyLabRobot/pylabrobot/blob/7779f506d12755f5f274b4c5cab4d095f4fccb62/pylabrobot/resources/resource.py#L347-L380) (code)
20. `cor_96_wellplate_2mL_Vb`: [https://github.com/PyLabRobot/pylabrobot/blob/7779f506d12755f5f274b4c5cab4d095f4fccb62/pylabrobot/resources/corning/plates.py#L101](https://github.com/PyLabRobot/pylabrobot/blob/7779f506d12755f5f274b4c5cab4d095f4fccb62/pylabrobot/resources/corning/plates.py#L101) (code)
21. `hamilton_96_tiprack_300uL_filter`: [https://github.com/PyLabRobot/pylabrobot/blob/7779f506d12755f5f274b4c5cab4d095f4fccb62/pylabrobot/resources/hamilton/tip_racks.py#L214](https://github.com/PyLabRobot/pylabrobot/blob/7779f506d12755f5f274b4c5cab4d095f4fccb62/pylabrobot/resources/hamilton/tip_racks.py#L214) (code)
22. `PLT_CAR_L5AC_A00`: [https://github.com/PyLabRobot/pylabrobot/blob/7779f506d12755f5f274b4c5cab4d095f4fccb62/pylabrobot/resources/hamilton/plate_carriers.py#L752](https://github.com/PyLabRobot/pylabrobot/blob/7779f506d12755f5f274b4c5cab4d095f4fccb62/pylabrobot/resources/hamilton/plate_carriers.py#L752) (code)
23. `TIP_CAR_480_A00`: [https://github.com/PyLabRobot/pylabrobot/blob/7779f506d12755f5f274b4c5cab4d095f4fccb62/pylabrobot/resources/hamilton/tip_carriers.py#L374](https://github.com/PyLabRobot/pylabrobot/blob/7779f506d12755f5f274b4c5cab4d095f4fccb62/pylabrobot/resources/hamilton/tip_carriers.py#L374) (code)
24. `STARDeck`: [https://github.com/PyLabRobot/pylabrobot/blob/7779f506d12755f5f274b4c5cab4d095f4fccb62/pylabrobot/resources/hamilton/star_decks.py#L237-L262](https://github.com/PyLabRobot/pylabrobot/blob/7779f506d12755f5f274b4c5cab4d095f4fccb62/pylabrobot/resources/hamilton/star_decks.py#L237-L262) (code)
25. `set_volume_tracking`: [https://github.com/PyLabRobot/pylabrobot/blob/7779f506d12755f5f274b4c5cab4d095f4fccb62/pylabrobot/resources/volume_tracker.py#L17](https://github.com/PyLabRobot/pylabrobot/blob/7779f506d12755f5f274b4c5cab4d095f4fccb62/pylabrobot/resources/volume_tracker.py#L17) (code)
26. `set_tip_tracking`: [https://github.com/PyLabRobot/pylabrobot/blob/7779f506d12755f5f274b4c5cab4d095f4fccb62/pylabrobot/resources/tip_tracking.py#L8](https://github.com/PyLabRobot/pylabrobot/blob/7779f506d12755f5f274b4c5cab4d095f4fccb62/pylabrobot/resources/tip_tracking.py#L8) (code)
27. PR #1574, VANTAstar over native USB (2 Nov 2026): [https://github.com/PyLabRobot/pylabrobot/pull/1574](https://github.com/PyLabRobot/pylabrobot/pull/1574), commit [https://github.com/PyLabRobot/pylabrobot/commit/87e7102b1](https://github.com/PyLabRobot/pylabrobot/commit/87e7102b1) (code)
28. VANTAstar package: [https://github.com/PyLabRobot/pylabrobot/tree/7779f506d12755f5f274b4c5cab4d095f4fccb62/pylabrobot/bmg_labtech/vantastar](https://github.com/PyLabRobot/pylabrobot/tree/7779f506d12755f5f274b4c5cab4d095f4fccb62/pylabrobot/bmg_labtech/vantastar) (code)
29. VANTAstar plate holder drawer check: [https://github.com/PyLabRobot/pylabrobot/blob/7779f506d12755f5f274b4c5cab4d095f4fccb62/pylabrobot/bmg_labtech/vantastar/device.py#L21-L70](https://github.com/PyLabRobot/pylabrobot/blob/7779f506d12755f5f274b4c5cab4d095f4fccb62/pylabrobot/bmg_labtech/vantastar/device.py#L21-L70) (code)
30. VANTAstar `Absorbance.measure`: [https://github.com/PyLabRobot/pylabrobot/blob/7779f506d12755f5f274b4c5cab4d095f4fccb62/pylabrobot/bmg_labtech/vantastar/driver/features/absorbance.py#L79-L128](https://github.com/PyLabRobot/pylabrobot/blob/7779f506d12755f5f274b4c5cab4d095f4fccb62/pylabrobot/bmg_labtech/vantastar/driver/features/absorbance.py#L79-L128) (code)
31. `USB(zero_length_packets=...)`: [https://github.com/PyLabRobot/pylabrobot/blob/7779f506d12755f5f274b4c5cab4d095f4fccb62/pylabrobot/io/usb.py#L62-L85](https://github.com/PyLabRobot/pylabrobot/blob/7779f506d12755f5f274b4c5cab4d095f4fccb62/pylabrobot/io/usb.py#L62-L85) (code)
32. CLARIOstar v1 PRs, Oct 2026, e.g. [https://github.com/PyLabRobot/pylabrobot/pull/1526](https://github.com/PyLabRobot/pylabrobot/pull/1526), [https://github.com/PyLabRobot/pylabrobot/pull/1536](https://github.com/PyLabRobot/pylabrobot/pull/1536), [https://github.com/PyLabRobot/pylabrobot/pull/1540](https://github.com/PyLabRobot/pylabrobot/pull/1540) (code)
33. PreciseFlex PRs: [https://github.com/PyLabRobot/pylabrobot/pull/1550](https://github.com/PyLabRobot/pylabrobot/pull/1550), [https://github.com/PyLabRobot/pylabrobot/pull/1551](https://github.com/PyLabRobot/pylabrobot/pull/1551), [https://github.com/PyLabRobot/pylabrobot/pull/1552](https://github.com/PyLabRobot/pylabrobot/pull/1552), [https://github.com/PyLabRobot/pylabrobot/pull/1564](https://github.com/PyLabRobot/pylabrobot/pull/1564), [https://github.com/PyLabRobot/pylabrobot/pull/1577](https://github.com/PyLabRobot/pylabrobot/pull/1577), [https://github.com/PyLabRobot/pylabrobot/pull/1586](https://github.com/PyLabRobot/pylabrobot/pull/1586) (code)
34. `PreciseFlexArm.probe_z_using_ztouch`: [https://github.com/PyLabRobot/pylabrobot/blob/7779f506d12755f5f274b4c5cab4d095f4fccb62/pylabrobot/brooks/precise_flex/driver/features/arm.py#L2422-L2470](https://github.com/PyLabRobot/pylabrobot/blob/7779f506d12755f5f274b4c5cab4d095f4fccb62/pylabrobot/brooks/precise_flex/driver/features/arm.py#L2422-L2470) (code)
35. `PreciseFlexVision`: [https://github.com/PyLabRobot/pylabrobot/blob/7779f506d12755f5f274b4c5cab4d095f4fccb62/pylabrobot/brooks/precise_flex/driver/features/vision.py#L1-L12](https://github.com/PyLabRobot/pylabrobot/blob/7779f506d12755f5f274b4c5cab4d095f4fccb62/pylabrobot/brooks/precise_flex/driver/features/vision.py#L1-L12), `capture_image` [https://github.com/PyLabRobot/pylabrobot/blob/7779f506d12755f5f274b4c5cab4d095f4fccb62/pylabrobot/brooks/precise_flex/driver/features/vision.py#L637](https://github.com/PyLabRobot/pylabrobot/blob/7779f506d12755f5f274b4c5cab4d095f4fccb62/pylabrobot/brooks/precise_flex/driver/features/vision.py#L637) (code)
36. "The simulator was removed in favor of the Visualizer": [https://github.com/PyLabRobot/pylabrobot/blob/7779f506d12755f5f274b4c5cab4d095f4fccb62/docs/user_guide/machine-agnostic-features/using-the-simulator.rst](https://github.com/PyLabRobot/pylabrobot/blob/7779f506d12755f5f274b4c5cab4d095f4fccb62/docs/user_guide/machine-agnostic-features/using-the-simulator.rst) (code)
37. `STAR(simulation=True)` factory: [https://github.com/PyLabRobot/pylabrobot/blob/7779f506d12755f5f274b4c5cab4d095f4fccb62/pylabrobot/hamilton/star/device.py#L382-L421](https://github.com/PyLabRobot/pylabrobot/blob/7779f506d12755f5f274b4c5cab4d095f4fccb62/pylabrobot/hamilton/star/device.py#L382-L421) (code)
38. visualizer3D README (PR #1378, 27 Sep 2026): [https://github.com/PyLabRobot/pylabrobot/blob/7779f506d12755f5f274b4c5cab4d095f4fccb62/pylabrobot/visualizer3D/README.md](https://github.com/PyLabRobot/pylabrobot/blob/7779f506d12755f5f274b4c5cab4d095f4fccb62/pylabrobot/visualizer3D/README.md) (code)
39. `LiquidHandlerChatterboxBackend`: [https://github.com/PyLabRobot/pylabrobot/blob/7779f506d12755f5f274b4c5cab4d095f4fccb62/pylabrobot/legacy/liquid_handling/backends/chatterbox.py#L24](https://github.com/PyLabRobot/pylabrobot/blob/7779f506d12755f5f274b4c5cab4d095f4fccb62/pylabrobot/legacy/liquid_handling/backends/chatterbox.py#L24) (code)
40. "A Fully Integrated Assay Panel for Early Drug Metabolism and Pharmacokinetics Profiling" (AstraZeneca): [https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7567642/](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7567642/) (paper)
41. "Harmonised high throughput microsomal stability assay": [https://pubmed.ncbi.nlm.nih.gov/27773845/](https://pubmed.ncbi.nlm.nih.gov/27773845/) (paper)
42. QInstruments `BioShake` (v1): [https://github.com/PyLabRobot/pylabrobot/blob/7779f506d12755f5f274b4c5cab4d095f4fccb62/pylabrobot/qinstruments/bioshake.py#L20-L280](https://github.com/PyLabRobot/pylabrobot/blob/7779f506d12755f5f274b4c5cab4d095f4fccb62/pylabrobot/qinstruments/bioshake.py#L20-L280) (code)
43. Legacy `LiquidHandler` methods `pick_up_tips`, `discard_tips`, `aspirate`, `dispense`: [https://github.com/PyLabRobot/pylabrobot/blob/7779f506d12755f5f274b4c5cab4d095f4fccb62/pylabrobot/legacy/liquid_handling/liquid_handler.py#L660](https://github.com/PyLabRobot/pylabrobot/blob/7779f506d12755f5f274b4c5cab4d095f4fccb62/pylabrobot/legacy/liquid_handling/liquid_handler.py#L660), [#L1028](https://github.com/PyLabRobot/pylabrobot/blob/7779f506d12755f5f274b4c5cab4d095f4fccb62/pylabrobot/legacy/liquid_handling/liquid_handler.py#L1028), [#L1124](https://github.com/PyLabRobot/pylabrobot/blob/7779f506d12755f5f274b4c5cab4d095f4fccb62/pylabrobot/legacy/liquid_handling/liquid_handler.py#L1124), [#L1316](https://github.com/PyLabRobot/pylabrobot/blob/7779f506d12755f5f274b4c5cab4d095f4fccb62/pylabrobot/legacy/liquid_handling/liquid_handler.py#L1316) (code)
44. di-omics/plr-mcp, `plr_drop_tips` tool and README: [https://github.com/di-omics/plr-mcp/blob/db90c579439bdea0930be5f7dc0ac5fddb93b3b3/plr_mcp/server.py#L199-L206](https://github.com/di-omics/plr-mcp/blob/db90c579439bdea0930be5f7dc0ac5fddb93b3b3/plr_mcp/server.py#L199-L206), [README](https://github.com/di-omics/plr-mcp/blob/db90c579439bdea0930be5f7dc0ac5fddb93b3b3/README.md) (code)
45. nygmeta/OpenLabAI, Hamilton MCP server: [https://github.com/nygmeta/OpenLabAI/blob/daade8e9f92e573362b20f9c46738b60db55cb6d/mcp_servers/hamilton_server.py](https://github.com/nygmeta/OpenLabAI/blob/daade8e9f92e573362b20f9c46738b60db55cb6d/mcp_servers/hamilton_server.py) (code)
46. sl148/closed-loop-lab-demo ("labloop"), PLR bridge: [https://github.com/sl148/closed-loop-lab-demo/blob/86b27d6c66d54e57abd22e93fefa084d2dc20f15/src/labloop/execution/plr_bridge.py#L21-L65](https://github.com/sl148/closed-loop-lab-demo/blob/86b27d6c66d54e57abd22e93fefa084d2dc20f15/src/labloop/execution/plr_bridge.py#L21-L65) (code)
47. PyLabRobot forum, "Bridged PyLabRobot into an agent-facing protocol" (Labwire): [https://discuss.pylabrobot.org/t/bridged-pylabrobot-into-an-agent-facing-protocol/552](https://discuss.pylabrobot.org/t/bridged-pylabrobot-into-an-agent-facing-protocol/552) (secondary)
48. K-Dense-AI/claude-scientific-skills, `skills/pylabrobot/SKILL.md`: [https://github.com/K-Dense-AI/claude-scientific-skills/blob/a25cf9ec00e2745d03f8704acf6f6919694ccd9a/skills/pylabrobot/SKILL.md](https://github.com/K-Dense-AI/claude-scientific-skills/blob/a25cf9ec00e2745d03f8704acf6f6919694ccd9a/skills/pylabrobot/SKILL.md) (code)
49. Opentrons, OpentronsAI server settings and tools: [https://github.com/Opentrons/opentrons/blob/631207155300fe9e96e08e4cfca48d11837fbd0c/opentrons-ai-server/api/settings.py#L32-L34](https://github.com/Opentrons/opentrons/blob/631207155300fe9e96e08e4cfca48d11837fbd0c/opentrons-ai-server/api/settings.py#L32-L34), [anthropic_predict.py#L145-L160](https://github.com/Opentrons/opentrons/blob/631207155300fe9e96e08e4cfca48d11837fbd0c/opentrons-ai-server/api/domain/anthropic_predict.py#L145-L160) (code); launch release, 1 Feb 2024: [https://www.businesswire.com/news/home/20240201923858/en/](https://www.businesswire.com/news/home/20240201923858/en/) (primary)
50. Boiko D.A. et al., "Autonomous chemical research with large language models", *Nature* 624, 570–578 (2023): [https://www.nature.com/articles/s41586-023-06792-0](https://www.nature.com/articles/s41586-023-06792-0) (paper); repo [https://github.com/gomesgroup/coscientist/tree/417e82b85743f88719ba7cf8838220fcb872e2ae](https://github.com/gomesgroup/coscientist/tree/417e82b85743f88719ba7cf8838220fcb872e2ae) (code)
51. CRESt, human-confirmation flags: [https://github.com/zhang21mit/CRESt/blob/8bcb140d285b58508c9b34d53bf2dc39360b2b64/Auto_SEM/main_workflow/main_workflow_func_list.py#L193-L210](https://github.com/zhang21mit/CRESt/blob/8bcb140d285b58508c9b34d53bf2dc39360b2b64/Auto_SEM/main_workflow/main_workflow_func_list.py#L193-L210) (code)
52. BayBE `Campaign.recommend` / `add_measurements`: [https://github.com/emdgroup/baybe/blob/ed54e0092acd0dc07b2a920ef4b58198f608bfa1/baybe/campaign.py#L495](https://github.com/emdgroup/baybe/blob/ed54e0092acd0dc07b2a920ef4b58198f608bfa1/baybe/campaign.py#L495), [#L324](https://github.com/emdgroup/baybe/blob/ed54e0092acd0dc07b2a920ef4b58198f608bfa1/baybe/campaign.py#L324) (code)
53. Ax README (`Client.get_next_trials` / `complete_trial`): [https://github.com/facebook/Ax/blob/5a7b3367f2d372e1653fd6c6ff1eaf8069ecc850/README.md](https://github.com/facebook/Ax/blob/5a7b3367f2d372e1653fd6c6ff1eaf8069ecc850/README.md) (code)
54. MADSci example experiment: [https://github.com/AD-SDL/MADSci/blob/bbfcba5efcaeacb750252a921256de5d61d51bb2/examples/example_experiment.py#L105](https://github.com/AD-SDL/MADSci/blob/bbfcba5efcaeacb750252a921256de5d61d51bb2/examples/example_experiment.py#L105) (code)
55. Atlas README (ask/tell): [https://github.com/aspuru-guzik-group/atlas/blob/ebb1f4f728107f759c48289c2faecfa3af19254f/README.md](https://github.com/aspuru-guzik-group/atlas/blob/ebb1f4f728107f759c48289c2faecfa3af19254f/README.md) (code)
56. SiLA 2 Python reference implementation, GreetingProvider feature: [https://gitlab.com/SiLA2/sila_python/-/tree/e6df5262ae6098cc7a04cd6c02a77a1621172cf6/example_server](https://gitlab.com/SiLA2/sila_python/-/tree/e6df5262ae6098cc7a04cd6c02a77a1621172cf6/example_server) (code)
57. PLR SiLA discovery guide: [https://github.com/PyLabRobot/pylabrobot/blob/7779f506d12755f5f274b4c5cab4d095f4fccb62/docs/user_guide/machine-agnostic-features/sila-discovery.ipynb](https://github.com/PyLabRobot/pylabrobot/blob/7779f506d12755f5f274b4c5cab4d095f4fccb62/docs/user_guide/machine-agnostic-features/sila-discovery.ipynb) (code)
58. OpenAI, "GPT-5 lowers the cost of cell-free protein synthesis" (Feb 2026): [https://openai.com/index/gpt-5-lowers-protein-synthesis-cost/](https://openai.com/index/gpt-5-lowers-protein-synthesis-cost/) (primary)
59. Zhou et al., LabSafety Bench, *Nature Machine Intelligence*: [https://www.nature.com/articles/s42256-025-01152-1](https://www.nature.com/articles/s42256-025-01152-1); preprint [https://arxiv.org/abs/2410.14182](https://arxiv.org/abs/2410.14182) (paper)
60. Inagaki T. et al., "LLMs can generate robotic scripts from goal-oriented instructions in biological laboratory automation", arXiv 2304.10267 (2023): [https://arxiv.org/abs/2304.10267](https://arxiv.org/abs/2304.10267) (paper)
61. Inductive Bio, "Ginkgo Datapoints, Tangible Scientific and Inductive Bio launch ADME-One" (26 May 2026): [https://www.inductive.bio/news/ginkgo-datapoints-tangible-scientific-and-inductive-bio-launch-adme-one](https://www.inductive.bio/news/ginkgo-datapoints-tangible-scientific-and-inductive-bio-launch-adme-one) (primary)
62. Brocklehurst C.E. et al. (Novartis), "MicroCycle", *J. Med. Chem.* (2024): [https://doi.org/10.1021/acs.jmedchem.3c02029](https://doi.org/10.1021/acs.jmedchem.3c02029) (paper)

> **Rate:** _/5 · **Tags:** _ · `LAN-F20261102`
