# Lab automation weekly, 14 Nov 2026

10 Nov – 14 Nov 2026 · 3 stories · 1 papers · 4 filtered out · 🎯 your field (DMPK/ADME) · ✅ verified · 🟡 partly verified · ⚪ unverified · ⏳ not yet checked · ⚠️ technical claim questionable · ⛔ technical claim unsupported

## TL;DR
- **AutoDNA in Nature**: LLM agents ran a DNA lab across 20+ instruments, checking each procedure in a virtual copy first ([Nature](https://doi.org/10.1038/s41586-026-11228-6)).
- **Pierre Fabre picks XtalPi's AI-plus-robotics platform** for oncology small-molecule discovery ([release](https://www.prnewswire.com/news-releases/laboratoires-pierre-fabre-and-xtalpi-announce-an-ai-driven-collaboration-focused-on-drug-discovery-302932390.html)).
- **PyLabRobot adds Formulatrix Mantis, Inheco ODTC and Hamilton-over-TCP**; most commits credit an AI assistant ([PR](https://github.com/PyLabRobot/pylabrobot/pull/1612)).
- **No vendor automation news** from Hamilton, Tecan, Agilent or Beckman this week ([run log](https://github.com/bum94587/LabAutoNews/blob/claude/youthful-cerf-3xizid/data/runs/2026-11-14.json)).

## Stories

### 1. Pierre Fabre picks XtalPi's AI-plus-robotics platform for oncology small-molecule discovery
✅⚠️ · partnership · XtalPi, Pierre Fabre · 9 Nov

Laboratoires Pierre Fabre and XtalPi agreed to discover clinical candidates across several oncology programmes, with XtalPi designing and delivering small molecules using its AI and robotics capabilities. Financial terms were not disclosed in the release. **Why:** Another mid-size pharma outsourcing DMTA to a robot-backed AI shop; whether ADME data is generated in that loop is not stated.

Sources: [PR Newswire: Pierre Fabre and XtalPi](https://www.prnewswire.com/news-releases/laboratoires-pierre-fabre-and-xtalpi-announce-an-ai-driven-collaboration-focused-on-drug-discovery-302932390.html) · [XtalPi Autonomous Lab Solution page](https://en.xtalpi.com/lab_automation/)

> **Rate:** _/5 · **Tags:** _ · `LAN-20261114-03`

### 2. PyLabRobot week: Formulatrix Mantis, Inheco ODTC, Hamilton over TCP, finer STAR control
✅⚠️ · community · PyLabRobot, Formulatrix, Inheco · 13 Nov

PyLabRobot merged 34 commits from 8 to 13 Nov, adding drivers for the Formulatrix Mantis dispenser and Inheco ODTC thermocycler and a TCP transport for Hamilton machines. 23 of the 34 commits credit an AI coding assistant as co-author. **Why:** Mantis and ODTC are common in assay prep; open drivers make them schedulable from Python without vendor software. (Mantis dispensing not merged yet)

Sources: [PyLabRobot PR 1612: v1 Mantis](https://github.com/PyLabRobot/pylabrobot/pull/1612) · [PyLabRobot PR 1026: ODTC direct device API](https://github.com/PyLabRobot/pylabrobot/pull/1026) · [PyLabRobot PR 1556: HamiltonTextTCP](https://github.com/PyLabRobot/pylabrobot/pull/1556) · [+3 in Details](#details)

> **Rate:** _/5 · **Tags:** _ · `LAN-20261114-05`

### 3. Sino Biological launches 4RISE wet-lab validation service for AI-designed proteins
✅⚠️ · product · Sino Biological · 9 Nov

Sino Biological launched 4RISE, a service that takes AI-designed molecules through expression, binding, developability and functional assays. All performance figures come from the company. **Why:** The wet-lab 'test' step for AI design is becoming a CRO product; biologics-focused, so limited small-molecule ADME relevance.

Sources: [Sino Biological press release (via Placera)](https://www.placera.se/pressmeddelanden/sino-biological-advances-ai-designed-molecule-validation-with-4rise-tm-20261109) · [BioPharma APAC](https://biopharmaapac.com/news/44/8668/sino-biological-introduces-4rise-to-accelerate-validation-of-ai-designed-proteins.html)

> **Rate:** _/5 · **Tags:** _ · `LAN-20261114-04`

## From the journals

SLAS Discovery, SLAS Technology, HardwareX, PubMed and preprints; your field first.

### P1. Shanghai Jiao Tong's AutoDNA: AI agents run a DNA lab across 20+ instruments
*Nature* · Wu et al. · 4 Nov · 🟡

A Nature paper presents AutoDNA, a lab where a team of LLM agents plans and runs nucleic-acid synthesis, amplification, transcription and sequencing from a typed prompt. A virtual copy of the lab checks each procedure before robots execute it. **Why:** A peer-reviewed multi-agent lab that schedules many instruments end to end; the pattern (agents + digital-twin check) is what ADME workcells would need, not yet shown there.

[An AI-native experimental laboratory for autonomous biomolecular operations (Nature)](https://doi.org/10.1038/s41586-026-11228-6) · [Nature news: AI agents run this automated biology lab that sequences DNA and more](https://www.nature.com/articles/d41586-026-03552-8) · [36Kr: AutoDNA published in Nature](https://eu.36kr.com/en/p/4056341270860929)

> **Rate:** _/5 · **Tags:** _ · `LAN-20261114-01`

## Signals to watch (analysis)
- **Digital twin before robot**: AutoDNA checks each agent-written procedure in a virtual lab before the robots run it; expect that to become the trust step for agent-run labs (analysis) ([Nature](https://doi.org/10.1038/s41586-026-11228-6)).
- **Thin start-up week**: no new self-driving-lab raise or launch surfaced 7-14 Nov; partly a search blind spot while news sites are blocked (analysis) ([run log](https://github.com/bum94587/LabAutoNews/blob/claude/youthful-cerf-3xizid/data/runs/2026-11-14.json)).

## Filtered out

Found but not shown as stories:

- **Nature: AI agents plan a robot lab in a digital twin, then run it** (hold, facts unverified): Neither the Nature news piece (d41586-026-03587-x, 'These AI agents design your perfect robot-powered lab') nor the Lab Manager article (36255) appeared in search, and both… [Nature: These AI agents design your perfect robot-powered lab — and run it for you](https://www.nature.com/articles/d41586-026-03587-x)
- **PyLabRobot now requires drivers to restore a device's original state** (hold, facts verified): Commit 7c1dc1c (#1616, 11 Nov 2026 PST) adds one bullet to docs/contributor_guide/device-driver-guide.md. [PyLabRobot PR 1616: restore device state](https://github.com/PyLabRobot/pylabrobot/pull/1616)
- **Explainer: how PyLabRobot finds and talks to Hamilton machines over a network** (hold, facts verified): Code at c5386e8 confirms all of it: UDP port 34569 with bdc_ pairs (ipaddress, systemid, modulename, macaddress); TCP port 24652 with CRLF ASCII lines and… [discovery.py at c5386e8](https://github.com/PyLabRobot/pylabrobot/blob/c5386e8/pylabrobot/hamilton/transport/text_tcp/discovery.py)
- **Explainer: PyLabRobot's Mantis driver ships a design doc an AI co-wrote** (hold, facts partial): Confirmed at 7f075f9: the design.md layer list, recordings of a v4 and a v3, liquid classes by viscosity band and chip type, and RFID chip… [Mantis design.md at 7f075f9](https://github.com/PyLabRobot/pylabrobot/blob/7f075f9/pylabrobot/formulatrix/mantis/design.md)

Screened out during research:

- [Hamilton and Parallel Fluidics partnership](https://www.hamiltoncompany.com/press-releases) [hamilton]: duplicate of LAN-20261109-01
- [Ahlstrom and Hamilton automated DBS processing](https://www.hamiltoncompany.com/press-releases/ahlstrom-hamilton-automated-dbs-processing) [hamilton]: 12 Oct, outside window (DMPK-relevant microsampling; missed earlier)
- [Tecan Q3 2026 update](https://www.tecan.com/news-archive) [tecan]: financial results, 5 Nov, outside window
- [Agilent 5987A GC/MS MSD and Proscia acquisition close](https://www.agilent.com/about/newsroom/presrel/) [agilent]: not lab automation; 2-4 Nov
- [Exypnos Pivot plate rotator](https://labautomation.io/t/rotating-plates-90-degrees-around-z-axis/2806) [labautomation-io]: post is ~3 years old, not new
- [SLAS San Diego meet-up and liquid-handling boot camp (17-18 Nov)](https://www.slas.org/events-calendar/) [slas]: routine event listings
- [ELRIG Protein Sciences in Drug Discovery, 10-11 Nov](https://elrig.org/portfolio/protein-sciences-in-drug-discovery-2026/) [elrig]: protein science/AI meeting, no automation content found
- [Robotic safety in self-driving laboratories (SLAS Technology)](https://www.sciencedirect.com/science/article/pii/S2472630326000774) [slas-technology]: online 26 Aug 2026, outside 14-day window
- [Acoustic ejection native MS for protein-ligand screening (SLAS Discov)](https://pubmed.ncbi.nlm.nih.gov/42580591/) [pubmed]: publication date not verifiable (PubMed blocked)
- [Monterey Automation acquires DYNEX Technologies](https://app.dealroom.co/news/note/monterey-automation-buys-dynex-technologies-to-deepen-lab-automation-reach) [web]: 6 Nov, one day outside window
- [Lila Sciences Pd-oxide electrolysis catalysts](https://cen.acs.org/business/start-ups/lila-ai-hydrogen-catalyst-electrolyzer/104/web/2026/10) [web]: 4 Nov, outside window; materials
- [Lila CEO on Fast Company Tech Visionaries list](https://www.lila.ai/news) [web]: award, not news
- [NVIDIA GR00T 2 and Isaac Lab 3.0](https://therobotreport.com/nvidia-launches-gr00t-2-isaac-lab-3-0-corl) [trade-press]: general robot learning, not lab automation
- [Uncountable environmental monitoring](https://drugdiscoverynews.com/can-auditors-trace-every-swab-result-to-its-sampling-point-17663) [trade-press]: QC/EM software, not lab automation
- [mzio mzassist MS control layer](https://www.drugtargetreview.com/reports/lab-automation-2026-inside-the-labs-making-drug-discovery-faster-and-more-reliable/2136826.article) [trade-press]: 2 Nov, outside window; only secondary mention
- [Chai-Roche, Variational AI-Merck, VivoSim-Chemveda deals](https://www.biospace.com/press-releases/chai-discovery-announces-collaboration-with-roche-in-ai-driven-drug-discovery) [wires]: AI design deals without lab automation; 2-6 Nov
- [Applied Intuition, Opdo raises](https://tech.eu/2026/11/12/berlin-la-startup-opdo-raises-23m-to-automate-optical-engineering-with-ai) [web]: autonomous vehicles / optics, not labs
- [PyLabRobot single PRs (CI, docs, resources, visualizer tweaks)](https://github.com/PyLabRobot/pylabrobot/commits/main) [pylabrobot]: folded into weekly roll-up LAN-20261114-05

## Scope: sites and companies

What each site and company produced in this window. To add or remove one, fill in the **Scope** line at the very bottom; the next run applies it to `config/`.

| Site | Tier | Cadence | Checked via | Candidates | Stories |
|---|---|---|---|---:|---:|
| [Labautomation.io (community forum)](https://labautomation.io) | core | daily | site-search | 2 | 0 |
| [PyLabRobot (open-source lab automation library)](https://github.com/PyLabRobot/pylabrobot) | core | daily | feed | 34 | 1 |
| Autonomous / self-driving lab start-ups and players | core | daily | **not checked** | 0 | 0 |
| [SLAS (Society for Laboratory Automation and Screening)](https://www.slas.org/news-highlights/news-center/) | core | daily | site-search | 1 | 0 |
| [LRIG (Laboratory Robotics Interest Group) and chapters](https://www.lrig.org) | core | daily | site-search | 0 | 0 |
| [ELRIG (European Laboratory Research & Innovation Group)](https://www.elrig.org) | core | daily | site-search | 1 | 0 |
| [Hamilton Company (Robotics / liquid handling)](https://www.hamiltoncompany.com/automated-liquid-handling) | core | daily | site-search | 3 | 0 |
| [Tecan (lab automation)](https://www.tecan.com/news-archive) | core | daily | site-search | 1 | 0 |
| [Agilent (automation & liquid handling only)](https://www.agilent.com/en/product/automated-liquid-handling) | core | daily | site-search | 3 | 0 |
| [Beckman Coulter (Life Sciences automation + clinical lab automation)](https://www.beckman.com/news) | core | daily | site-search | 0 | 0 |
| [SLAS Discovery (journal)](https://www.sciencedirect.com/journal/slas-discovery) | core | weekly | site-search | 1 | 0 |
| [SLAS Technology (journal)](https://www.sciencedirect.com/journal/slas-technology) | core | weekly | site-search | 1 | 0 |
| [HardwareX (journal, open hardware)](https://www.sciencedirect.com/journal/hardwarex) | core | weekly | site-search | 0 | 0 |
| [PubMed (DMPK/ADME automation first, then pharma/biotech lab automation)](https://pubmed.ncbi.nlm.nih.gov/) | core | weekly | site-search | 2 | 0 |
| Lab trade press | secondary | daily | site-search | 5 | 0 |
| [LinkedIn (posts and articles, via search only)](https://www.linkedin.com/feed/hashtag/labautomation/) | secondary | daily | **not checked** | 0 | 0 |
| Press-release wires | secondary | daily | site-search | 6 | 1 |
| Preprints and other journals | secondary | weekly | site-search | 3 | 1 |
| Open web search (not a listed site) | — | daily | web-search | — | 1 |

**Companies watched** (stories this window):

- Core vendors: Hamilton 1 · Tecan 0 · Agilent 0 · Beckman Coulter 0
- Incumbents: Thermo Fisher 0 · Revvity 0 · Molecular Devices 0 · Eppendorf 0 · Sartorius 0 · Roche Diagnostics 0 · Siemens Healthineers 0 · Abbott 0 · Waters 0 · SPT Labtech 0 · Formulatrix 1 · Analytik Jena 0 · Gilson 0 · INTEGRA Biosciences 0
- Open source: PyLabRobot 1
- Growth: Opentrons 0 · Automata 0 · Biosero 0 · HighRes Biosolutions 0 · Synthace 0 · Benchling 0 · Emerald Cloud Lab 0 · Ginkgo Bioworks 0 · Cellares 0 · Retisoft 0 · Unchained Labs 0
- AI-native: Lila Sciences 0 · Periodic Labs 0 · Chemify 0 · Radical AI 0 · Medra 0 · Trilobio 0 · FutureHouse 0 · Arctoris 0 · Recursion 0 · Tetsuwan Scientific 0 · Potato 0 · Ginkgo Cloud Lab 0 · XtalPi 1 · Insilico Medicine 0 · Telescope Innovations 0 · ABLE Labs 0 · Monomer Bio 0 · Emerald Cloud Lab 0 · Automata 0 · Dunia Innovations 0 · Orbital Materials 0

**In the news, not on the watchlist** (add?): Inheco · Pierre Fabre · Shanghai Jiao Tong University · Sino Biological

## Details <a id="details"></a>

**1. Pierre Fabre picks XtalPi's AI-plus-robotics platform for oncology small-molecule discovery** (`LAN-20261114-03`, self-driving-labs, published 2026-11-09)
- Announced 9 Nov 2026; scope oncology, potentially dermatology and other diseases [[1]](https://www.prnewswire.com/news-releases/laboratoires-pierre-fabre-and-xtalpi-announce-an-ai-driven-collaboration-focused-on-drug-discovery-302932390.html)
- Pierre Fabre handles disease biology, translational and clinical development [[1]](https://www.prnewswire.com/news-releases/laboratoires-pierre-fabre-and-xtalpi-announce-an-ai-driven-collaboration-focused-on-drug-discovery-302932390.html)
- XtalPi says its autonomous-lab platform orchestrates hundreds of workstations for a 24/7 closed-loop DMTA cycle (company claim, not deal-specific) [[2]](https://en.xtalpi.com/lab_automation/)
- Verifier: facts verified, science questionable. The PR Newswire release title and the 9 Nov 2026 date are confirmed through search snippets and syndicated copies (Macau Business, BioSpectrum Asia, BioPharma APAC). They also confirm the oncology scope, possible expansion to dermatology and rare diseases, Pierre Fabre's role and that no financial terms were given. The '24/7 closed-loop DMTA, hundreds of workstations' line comes only from XtalPi's own marketing, and the item labels it correctly. No deal-specific automation detail was given.
- Sources: [1] [PR Newswire: Pierre Fabre and XtalPi](https://www.prnewswire.com/news-releases/laboratoires-pierre-fabre-and-xtalpi-announce-an-ai-driven-collaboration-focused-on-drug-discovery-302932390.html) (primary) · [2] [XtalPi Autonomous Lab Solution page](https://en.xtalpi.com/lab_automation/) (primary)

**2. PyLabRobot week: Formulatrix Mantis, Inheco ODTC, Hamilton over TCP, finer STAR control** (`LAN-20261114-05`, software-orchestration, published 2026-11-13)
- Mantis: connect, identify, plate clamp, RFID chip tags, arm and Z bring-up, sequencer (PRs 1612, 1621-1623) [[1]](https://github.com/PyLabRobot/pylabrobot/pull/1612)
- Inheco ODTC thermocycler driven through its SiLA 1 interface with the direct device API (PR 1026) [[2]](https://github.com/PyLabRobot/pylabrobot/pull/1026)
- HamiltonTextTCP transport plus UDP-broadcast discover_instruments (PR 1556) [[3]](https://github.com/PyLabRobot/pylabrobot/pull/1556)
- STAR pipette Y moves get a settable default speed of 275 mm/s; Y probe post-detection moves run per channel, enabling parallelism (PRs 1607, 1608) [[4]](https://github.com/PyLabRobot/pylabrobot/pull/1608)
- OT-2: unfinished runs, rail lights and door status readable (PRs 1587, 1588) [[5]](https://github.com/PyLabRobot/pylabrobot/pull/1587)
- 23 of 34 commits on main 8-13 Nov carry an AI-assistant Co-authored-by trailer (git log count) [[6]](https://github.com/PyLabRobot/pylabrobot/commits/main)
- Verifier: facts verified, science questionable. Checked in git: 34 commits on main dated 8-13 Nov, 23 of them with an AI Co-authored-by trailer. The commits for PRs 1612, 1621-1623 (Mantis), 1026 (ODTC over SiLA 1), 1556 (HamiltonTextTCP and discover_instruments), 1607 and 1608 (275 mm/s default Y speed) and 1587/1588 (OT-2) match the claims. Caveats: a legacy ODTC backend already existed, so #1026 is a new implementation rather than a first driver. The Mantis driver cannot dispense yet (design.md: 'the dispensing PR settles them'), so 'schedulable from Python' overstates it for now.
- Sources: [1] [PyLabRobot PR 1612: v1 Mantis](https://github.com/PyLabRobot/pylabrobot/pull/1612) (primary) · [2] [PyLabRobot PR 1026: ODTC direct device API](https://github.com/PyLabRobot/pylabrobot/pull/1026) (primary) · [3] [PyLabRobot PR 1556: HamiltonTextTCP](https://github.com/PyLabRobot/pylabrobot/pull/1556) (primary) · [4] [PyLabRobot PR 1608: STAR Y speed](https://github.com/PyLabRobot/pylabrobot/pull/1608) (primary) · [5] [PyLabRobot PR 1587: OT2 lights and door](https://github.com/PyLabRobot/pylabrobot/pull/1587) (primary) · [6] [PyLabRobot commit history](https://github.com/PyLabRobot/pylabrobot/commits/main) (primary)

**3. Sino Biological launches 4RISE wet-lab validation service for AI-designed proteins** (`LAN-20261114-04`, cloud-labs, published 2026-11-09)
- Press release dated 9-10 Nov 2026 [[1]](https://www.placera.se/pressmeddelanden/sino-biological-advances-ai-designed-molecule-validation-with-4rise-tm-20261109)
- More than 20 developability assays plus molecular and cell-based functional assays [[1]](https://www.placera.se/pressmeddelanden/sino-biological-advances-ai-designed-molecule-validation-with-4rise-tm-20261109)
- Cell-free expression in as little as three hours (company claim) [[1]](https://www.placera.se/pressmeddelanden/sino-biological-advances-ai-designed-molecule-validation-with-4rise-tm-20261109)
- Company claims collaborations with more than 50 AI companies [[2]](https://biopharmaapac.com/news/44/8668/sino-biological-introduces-4rise-to-accelerate-validation-of-ai-designed-proteins.html)
- Verifier: facts verified, science questionable. Search snippets of the company release (Placera/PR Newswire, 9-10 Nov 2026), TradingKey and BioPharma APAC confirm 4RISE, the 20+ developability assays, the roughly 3 h cell-free expression and the 50+ AI-company collaborations. Every figure is the company's own and there is no independent benchmark, which the item says.
- Sources: [1] [Sino Biological press release (via Placera)](https://www.placera.se/pressmeddelanden/sino-biological-advances-ai-designed-molecule-validation-with-4rise-tm-20261109) (primary) · [2] [BioPharma APAC](https://biopharmaapac.com/news/44/8668/sino-biological-introduces-4rise-to-accelerate-validation-of-ai-designed-proteins.html) (secondary)

**P1. Shanghai Jiao Tong's AutoDNA: AI agents run a DNA lab across 20+ instruments** (`LAN-20261114-01`, self-driving-labs, published 2026-11-04)
- Published in Nature on 4 Nov 2026 (doi 10.1038/s41586-026-11228-6) [[1]](https://doi.org/10.1038/s41586-026-11228-6)
- Coordinates more than 20 types of instruments; 36Kr reports over 11,000 experiment steps (step counts differ between outlets) [[3]](https://eu.36kr.com/en/p/4056341270860929)
- A preprint version was posted on arXiv in July 2025 (2507.02379) [[4]](https://arxiv.org/abs/2507.02379)
- Humans still restocked reagents and removed waste (Singularity Hub's account) [[5]](https://singularityhub.com/2026/11/10/ai-agents-ran-a-biology-lab-humans-popped-in-to-empty-the-trash/)
- Nature's news story calls it an AI-native self-driving biology lab built around AI from the start [[2]](https://www.nature.com/articles/d41586-026-03552-8)
- Verifier: facts partial, science sound. Search snippets from several outlets (Singularity Hub 10 Nov, 36Kr, Pebblous, Lifeboat) confirm a Shanghai Jiao Tong AutoDNA paper in Nature on 4 Nov 2026 at s41586-026-11228-6: over 20 instruments, synthesis/transcription/amplification/sequencing, humans restocking and removing waste, and a July 2025 arXiv preprint (2507.02379). Not confirmed: the 30 Sep acceptance date, the Nature news article d41586-026-03552-8 and its wording (search turned up a News & Views, d41586-026-03270-1, instead), and the author line. The preprint's first author is Mingyu Wu, not Wang. One run is reported at 11,382 steps (about 203.5 h), but another outlet gives 9,551 operations in 137 h for a different test. Evidence level is a peer-reviewed article, but neither the paper nor the abstract could be opened.
- Sources: [1] [An AI-native experimental laboratory for autonomous biomolecular operations (Nature)](https://doi.org/10.1038/s41586-026-11228-6) (paper) · [2] [Nature news: AI agents run this automated biology lab that sequences DNA and more](https://www.nature.com/articles/d41586-026-03552-8) (secondary) · [3] [36Kr: AutoDNA published in Nature](https://eu.36kr.com/en/p/4056341270860929) (secondary) · [4] [arXiv preprint 2507.02379](https://arxiv.org/abs/2507.02379) (paper) · [5] [Singularity Hub, 10 Nov 2026](https://singularityhub.com/2026/11/10/ai-agents-ran-a-biology-lab-humans-popped-in-to-empty-the-trash/) (secondary)

## Feedback

> **Brief:** _/5 · **Missed:** _ · **Notes:** _ · `LAN-W20261114`

> **Scope:** Add: _ · Remove: _ · `LAN-S20261114`

Rate stories 1-5 (5 = must-know) and tag freely (`must-know`, `useful`, `meh`, `off-topic`, `wrong`, `unsound`, `hype`, `stale`, `dup`, `shallow`, `great`, `more`, `less`). **Missed**: anything this brief should have had. **Scope**: sites, companies or topics to add or remove, e.g. `Add: Opentrons blog, Automata · Remove: Telescope Innovations`.
