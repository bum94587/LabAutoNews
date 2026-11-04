# Lab automation daily, 4 Nov 2026

4 Nov 2026 · 2 stories · 0 papers · 1 filtered out · 🎯 your field (DMPK/ADME) · ✅ verified · 🟡 partly verified · ⚪ unverified · ⏳ not yet checked · ⚠️ technical claim questionable · ⛔ technical claim unsupported

## Stories

### 1. Orca 2.3.0 adds simulation time-scaling and audit reasons for scheduler actions
✅ · community · Cheshire Labs · 19 Oct

Orca 2.3.0 lets simulated runs be paced faster than real time and writes ten more operator actions to an audit log, with an optional reason. Labware barcodes must now be unique. **Why:** Audit rows and barcode checks are the kind of traceability a regulated ADME lab needs from any scheduler; Orca is still early-stage.

Sources: [Orca v2.3.0 release notes](https://github.com/Cheshire-Labs/orca/releases/tag/v2.3.0)

> **Rate:** _/5 · **Tags:** _ · `LAN-20261104-02`

### 2. Orca lab scheduler 2.0 adds daemon and REST API, relicenses to SSPL
✅ · community · Cheshire Labs · 23 Sep

Cheshire Labs' Orca, a Python scheduler for lab workflows, moved to a persistent local daemon with REST/SSE interface and CLI in v2.0.0. The same release relicensed it from AGPL-3.0 to the Server Side Public License. **Why:** Open schedulers are maturing, but SSPL is not OSI-approved open source, so pharma legal teams may treat it differently.

Sources: [Orca v2.0.0 pull request](https://github.com/Cheshire-Labs/orca/pull/14)

> **Rate:** _/5 · **Tags:** _ · `LAN-20261104-01`

## Filtered out

Found but not shown as stories:

- **PyLabRobot merges work-in-progress Kingfisher magnetic-particle processor support** (hold, facts verified): PR #1570 'Kingfisher Support (WIP Primarily Presto)' shown merged 3 Nov 2026 by rickwierenga, adding a Presto device API. [PyLabRobot PR 1570](https://github.com/PyLabRobot/pylabrobot/pull/1570)

Screened out during research:

- [Hamilton and Ahlstrom automated DBS processing](https://www.hamiltoncompany.com/press-releases) [hamilton]: 9 Oct, outside window
- [Tecan agentic AI with NVIDIA](https://www.tecan.com/news-archive) [tecan]: May/June, outside window
- [Shimadzu and ePrep sample prep partnership](https://www.selectscience.net/technique/automated-liquid-handling) [trade-press]: August, outside window
- [Latent-Y antibody design agent](https://www.businesswire.com/news/home/20260323538522/en/Latent-Y-The-Autonomous-AI-Agent-for-Drug-Design-at-Scale) [wires]: March, outside window
- [Caco-2 96-well platform (Cai et al.)](https://doi.org/10.1177/1540658x251408742) [pubmed]: duplicate of LAN-20261102-16

## Scope: sites and companies

What each site and company produced in this window. To add or remove one, fill in the **Scope** line at the very bottom; the next run applies it to `config/`.

| Site | Tier | Cadence | Checked via | Candidates | Stories |
|---|---|---|---|---:|---:|
| [Labautomation.io (community forum)](https://labautomation.io) | core | daily | site-search | 0 | 0 |
| [PyLabRobot (open-source lab automation library)](https://github.com/PyLabRobot/pylabrobot) | core | daily | feed+site-search | 1 | 0 |
| [SLAS (Society for Laboratory Automation and Screening)](https://www.slas.org/news-highlights/news-center/) | core | daily | site-search | 0 | 0 |
| [LRIG (Laboratory Robotics Interest Group) and chapters](https://www.lrig.org) | core | daily | site-search | 0 | 0 |
| [ELRIG (European Laboratory Research & Innovation Group)](https://www.elrig.org) | core | daily | site-search | 0 | 0 |
| [Hamilton Company (Robotics / liquid handling)](https://www.hamiltoncompany.com/automated-liquid-handling) | core | daily | site-search | 0 | 0 |
| [Tecan (lab automation)](https://www.tecan.com/news-archive) | core | daily | site-search | 0 | 0 |
| [Agilent (automation & liquid handling only)](https://www.agilent.com/en/product/automated-liquid-handling) | core | daily | site-search | 0 | 0 |
| [Beckman Coulter (Life Sciences automation + clinical lab automation)](https://www.beckman.com/news) | core | daily | site-search | 0 | 0 |
| [SLAS Discovery (journal)](https://www.sciencedirect.com/journal/slas-discovery) | core | weekly | site-search | 0 | 0 |
| [SLAS Technology (journal)](https://www.sciencedirect.com/journal/slas-technology) | core | weekly | site-search | 0 | 0 |
| [HardwareX (journal, open hardware)](https://www.sciencedirect.com/journal/hardwarex) | core | weekly | site-search | 0 | 0 |
| [PubMed (DMPK/ADME automation first, then pharma/biotech lab automation)](https://pubmed.ncbi.nlm.nih.gov/) | core | weekly | site-search | 0 | 0 |
| Lab trade press | secondary | daily | site-search | 0 | 0 |
| [LinkedIn (posts and articles, via search only)](https://www.linkedin.com/feed/hashtag/labautomation/) | secondary | daily | **not checked** | 0 | 0 |
| Press-release wires | secondary | daily | site-search | 0 | 0 |
| Preprints and other journals | secondary | weekly | **not checked** | 0 | 0 |
| Open web search (not a listed site) | — | daily | web-search | — | 2 |

**Companies watched** (stories this window):

- Core vendors: Hamilton 0 · Tecan 0 · Agilent 0 · Beckman Coulter 0
- Incumbents: Thermo Fisher 0 · Revvity 0 · Molecular Devices 0 · Eppendorf 0 · Sartorius 0 · Roche Diagnostics 0 · Siemens Healthineers 0 · Abbott 0 · Waters 0 · SPT Labtech 0 · Formulatrix 0 · Analytik Jena 0 · Gilson 0 · INTEGRA Biosciences 0
- Open source: PyLabRobot 0
- Growth: Opentrons 0 · Automata 0 · Biosero 0 · HighRes Biosolutions 0 · Synthace 0 · Benchling 0 · Emerald Cloud Lab 0 · Ginkgo Bioworks 0 · Cellares 0 · Retisoft 0 · Unchained Labs 0
- AI-native: Lila Sciences 0 · Periodic Labs 0 · Chemify 0 · Radical AI 0 · Medra 0 · Trilobio 0 · FutureHouse 0 · Arctoris 0 · Recursion 0

**In the news, not on the watchlist** (add?): Cheshire Labs

## Details <a id="details"></a>

**1. Orca 2.3.0 adds simulation time-scaling and audit reasons for scheduler actions** (`LAN-20261104-02`, software-orchestration, published 2026-10-19)
- Simulation time scale: 1 real time, 0.1 ten times faster, 0 no pacing; LIVE runs reject it [[1]](https://github.com/Cheshire-Labs/orca/releases/tag/v2.3.0)
- Ten more operator actions write audit rows; audited actions accept an optional reason [[1]](https://github.com/Cheshire-Labs/orca/releases/tag/v2.3.0)
- Two labware cannot share a barcode (409 barcode_in_use) [[1]](https://github.com/Cheshire-Labs/orca/releases/tag/v2.3.0)
- Verifier: facts verified, science sound. Release notes confirm sim_time_scale (1 real time, 0.1 ten times faster, 0 no pacing, LIVE refused with 422), ten more audited verbs with optional reason, and 409 barcode_in_use. Release page shows 19 October without a year (2026 inferred). Applies to simulated runs only, which the summary says.
- Sources: [1] [Orca v2.3.0 release notes](https://github.com/Cheshire-Labs/orca/releases/tag/v2.3.0) (primary)

**2. Orca lab scheduler 2.0 adds daemon and REST API, relicenses to SSPL** (`LAN-20261104-01`, software-orchestration, published 2026-09-23)
- v2.0.0 replaces 1.x authoring with four decorators; workflows stay plain Python [[1]](https://github.com/Cheshire-Labs/orca/pull/14)
- 'Relicensed from AGPL-3.0 to the Server Side Public License, version 1'; releases up to v1.0.0 stay AGPL-3.0 [[1]](https://github.com/Cheshire-Labs/orca/pull/14)
- Verifier: facts verified, science na. Merged PR #14 (23 Sep 2026) states daemon with REST/SSE, CLI, four decorators, AGPL-3.0 to SSPL v1, and 'Releases up to v1.0.0 stay under AGPL-3.0'. Primary source only (author merged own PR); SSPL not being OSI-approved is analysis, not in the source.
- Sources: [1] [Orca v2.0.0 pull request](https://github.com/Cheshire-Labs/orca/pull/14) (primary)

## Feedback

> **Brief:** _/5 · **Missed:** _ · **Notes:** _ · `LAN-B20261104`

> **Scope:** Add: _ · Remove: _ · `LAN-S20261104`

Rate stories 1-5 (5 = must-know) and tag freely (`must-know`, `useful`, `meh`, `off-topic`, `wrong`, `unsound`, `hype`, `stale`, `dup`, `shallow`, `great`, `more`, `less`). **Missed**: anything this brief should have had. **Scope**: sites, companies or topics to add or remove, e.g. `Add: Opentrons blog, Automata · Remove: Telescope Innovations`.
