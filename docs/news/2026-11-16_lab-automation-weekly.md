# Lab automation weekly, 16 Nov 2026

10 Nov – 16 Nov 2026 · 7 stories · 1 papers · 5 filtered out · 🎯 your field (DMPK/ADME) · ✅ verified · 🟡 partly verified · ⚪ unverified · ⏳ not yet checked · ⚠️ technical claim questionable · ⛔ technical claim unsupported

## TL;DR
- **AutoDNA in Nature**: LLM agents ran a DNA lab across 20+ instruments, checking each procedure in a virtual copy first ([Nature](https://doi.org/10.1038/s41586-026-11228-6)).
- **AI ran bioreactor feeds on its own**: Basetwo, CPI, Labman and Nicoya closed the loop with robotic sampling (company claim) ([release](https://www.globenewswire.com/news-release/2026/11/11/3400756/0/en/canada-uk-collaboration-demonstrates-autonomous-bioreactor-control-for-a-her2-breast-cancer-therapeutic.html)).
- **Pierre Fabre picks XtalPi's AI-plus-robotics platform** for oncology small-molecule discovery ([release](https://www.prnewswire.com/news-releases/laboratoires-pierre-fabre-and-xtalpi-announce-an-ai-driven-collaboration-focused-on-drug-discovery-302932390.html)).
- **PyLabRobot adds a KX2 arm, a nanolitre dispenser and Mantis v3**; open drivers keep piling up ([PR](https://github.com/PyLabRobot/pylabrobot/pull/1637)).

## Stories

### 1. PyLabRobot weekend: PAA KX2 arm, Gyger CERTUS FLEX dispenser, Mantis v3 hardware
🟡 · product · PyLabRobot, PAA, Gyger · 16 Nov

PyLabRobot merged drivers for the PAA KX2 plate-handling arm and the Gyger CERTUS FLEX nanolitre valve dispenser, plus Mantis v3 arm, plate clamp and LC3 carousel control. A STAR reply-routing fix landed on 16 Nov. **Why:** Nanolitre dispensing and plate movers are ADME-plate building blocks; open drivers for both lower the cost of a scripted, AI-drivable workcell.

Sources: [PyLabRobot PR #880: PAA KX2 arm driver](https://github.com/PyLabRobot/pylabrobot/pull/880) · [PyLabRobot PR #1637: CERTUS FLEX driver](https://github.com/PyLabRobot/pylabrobot/pull/1637) · [PyLabRobot merge of #1635 (Mantis LC3 carousel)](https://github.com/PyLabRobot/pylabrobot/commit/4924ac1) · [+2 in Details](#details)

> **Rate:** _/5 · **Tags:** _ · `LAN-20261116-02`

### 2. Explainer: what 'hardware verified' means in PyLabRobot's CERTUS FLEX driver
✅ · other · PyLabRobot, Gyger · 15 Nov

The driver's protocol notes list each operation with the test it got on one named dispenser, and say what was not tested. They state that command checks do not prove delivered volume; that needs measured valve calibration curves. **Why:** A model for judging any AI-written driver: scoped evidence per command, honest gaps. Volume accuracy still needs a balance, as in any ADME assay qualification.

Sources: [PyLabRobot: CERTUS FLEX protocol and verification](https://github.com/PyLabRobot/pylabrobot/blob/7d8f270/docs/user_guide/gyger/certus_flex/protocol.md)

> **Rate:** _/5 · **Tags:** _ · `LAN-20261116-03`

### 3. Basetwo, CPI, Labman and Nicoya run fed-batch bioreactors under autonomous AI feed control
🟡⚠️ · other · Basetwo, CPI, Labman · 11 Nov

Four Canadian and UK organisations report closed-loop AI control of fed-batch bioreactors making a trastuzumab biosimilar candidate. Robotic sampling and a hybrid glucose model fed a predictive controller that set nutrient feeds without human input. **Why:** Robot sampling plus fast at-line assays closing a loop; the same pattern applies to timed ADME sampling. Bioprocess, not discovery, and results are unpublished.

Sources: [GlobeNewswire: Canada-UK collaboration demonstrates autonomous bioreactor control](https://www.globenewswire.com/news-release/2026/11/11/3400756/0/en/canada-uk-collaboration-demonstrates-autonomous-bioreactor-control-for-a-her2-breast-cancer-therapeutic.html) · [CPI: joins Canada-UK BALANCE collaboration](https://www.uk-cpi.com/news/cpi-joins-canada-uk-collaboration-developing-ai-powered-bioreactors-to-revolutionise-biopharmaceutical-manufacturing)

> **Rate:** _/5 · **Tags:** _ · `LAN-20261116-01`

### 4. Pierre Fabre picks XtalPi's AI-plus-robotics platform for oncology small-molecule discovery
✅⚠️ · partnership · XtalPi, Pierre Fabre · 9 Nov

Laboratoires Pierre Fabre and XtalPi agreed to discover clinical candidates across several oncology programmes, with XtalPi designing and delivering small molecules using its AI and robotics capabilities. Financial terms were not disclosed in the release. **Why:** Another mid-size pharma outsourcing DMTA to a robot-backed AI shop; whether ADME data is generated in that loop is not stated.

Sources: [PR Newswire: Pierre Fabre and XtalPi](https://www.prnewswire.com/news-releases/laboratoires-pierre-fabre-and-xtalpi-announce-an-ai-driven-collaboration-focused-on-drug-discovery-302932390.html) · [XtalPi Autonomous Lab Solution page](https://en.xtalpi.com/lab_automation/)

> **Rate:** _/5 · **Tags:** _ · `LAN-20261114-03`

### 5. Explainer: PyLabRobot drives the PAA KX2 arm over CANopen, not a vendor DLL
✅ · other · PyLabRobot, PAA · 14 Nov

The KX2 driver talks to the arm's motor drives over a CAN bus at 500 kbit/s through a new asynchronous CANopen transport. Setup records each drive's network state and restores it on teardown. **Why:** Talking to the motor drives directly makes an arm scriptable from any OS; the restore-state rule protects shared pharma workcells.

Sources: [PyLabRobot: KX2 installation](https://github.com/PyLabRobot/pylabrobot/blob/c2a33ca/docs/user_guide/paa/kx2/installation.md) · [PyLabRobot: io/canopen.py](https://github.com/PyLabRobot/pylabrobot/blob/c2a33ca/pylabrobot/io/canopen.py)

> **Rate:** _/5 · **Tags:** _ · `LAN-20261116-04`

### 6. PyLabRobot week: Formulatrix Mantis, Inheco ODTC, Hamilton over TCP, finer STAR control
✅⚠️ · community · PyLabRobot, Formulatrix, Inheco · 13 Nov

PyLabRobot merged 34 commits from 8 to 13 Nov, adding drivers for the Formulatrix Mantis dispenser and Inheco ODTC thermocycler and a TCP transport for Hamilton machines. 23 of the 34 commits credit an AI coding assistant as co-author. **Why:** Mantis and ODTC are common in assay prep; open drivers make them schedulable from Python without vendor software. (Mantis dispensing not merged yet)

Sources: [PyLabRobot PR 1612: v1 Mantis](https://github.com/PyLabRobot/pylabrobot/pull/1612) · [PyLabRobot PR 1026: ODTC direct device API](https://github.com/PyLabRobot/pylabrobot/pull/1026) · [PyLabRobot PR 1556: HamiltonTextTCP](https://github.com/PyLabRobot/pylabrobot/pull/1556) · [+3 in Details](#details)

> **Rate:** _/5 · **Tags:** _ · `LAN-20261114-05`

### 7. Sino Biological launches 4RISE wet-lab validation service for AI-designed proteins
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
- **Loops close where the assay is fast**: bioreactor and DNA-lab loops worked because readouts came at-line; ADME loops still wait on LC-MS/MS (analysis) ([release](https://www.globenewswire.com/news-release/2026/11/11/3400756/0/en/canada-uk-collaboration-demonstrates-autonomous-bioreactor-control-for-a-her2-breast-cancer-therapeutic.html)).
- **Drivers now ship with evidence tables**: PyLabRobot's CERTUS FLEX notes list what was tested on which unit; a useful bar for AI-written device code (analysis) ([docs](https://github.com/PyLabRobot/pylabrobot/blob/7d8f270/docs/user_guide/gyger/certus_flex/protocol.md)).
- **Second quiet start-up week**: no new self-driving-lab raise found 7-16 Nov, partly because news sites are blocked to direct fetch (analysis) ([run log](https://github.com/bum94587/LabAutoNews/blob/claude/youthful-cerf-ym1g2g/data/runs/2026-11-16.json)).

## Filtered out

Found but not shown as stories:

- **Nature: AI agents plan a robot lab in a digital twin, then run it** (hold, facts unverified): Neither the Nature news piece (d41586-026-03587-x, 'These AI agents design your perfect robot-powered lab') nor the Lab Manager article (36255) appeared in search, and both… [Nature: These AI agents design your perfect robot-powered lab — and run it for you](https://www.nature.com/articles/d41586-026-03587-x)
- **PyLabRobot now requires drivers to restore a device's original state** (hold, facts verified): Commit 7c1dc1c (#1616, 11 Nov 2026 PST) adds one bullet to docs/contributor_guide/device-driver-guide.md. [PyLabRobot PR 1616: restore device state](https://github.com/PyLabRobot/pylabrobot/pull/1616)
- **Explainer: how PyLabRobot finds and talks to Hamilton machines over a network** (hold, facts verified): Code at c5386e8 confirms all of it: UDP port 34569 with bdc_ pairs (ipaddress, systemid, modulename, macaddress); TCP port 24652 with CRLF ASCII lines and… [discovery.py at c5386e8](https://github.com/PyLabRobot/pylabrobot/blob/c5386e8/pylabrobot/hamilton/transport/text_tcp/discovery.py)
- **Explainer: PyLabRobot's Mantis driver ships a design doc an AI co-wrote** (hold, facts partial): Confirmed at 7f075f9: the design.md layer list, recordings of a v4 and a v3, liquid classes by viscosity band and chip type, and RFID chip… [Mantis design.md at 7f075f9](https://github.com/PyLabRobot/pylabrobot/blob/7f075f9/pylabrobot/formulatrix/mantis/design.md)
- **Preprint: how optimiser repair rules behave in living-cell self-driving labs** (hold, facts partial): A search snippet confirms the preprint, the DOI, Duke, simulation on synthetic landscapes, and that it is not peer reviewed. [bioRxiv: Optimiser Repairs for Living-Cell Self-Driving Laboratories: Performance and Redundancy under Experimental Constraints](https://www.biorxiv.org/content/10.64898/2026.11.03.763926v1)

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
- [Flagship Pioneering commits £100M to London AI-biotech outpost](https://fiercebiotech.com/biotech/flagship-commits-ps100-million-set-ai-focused-biotech-incubation-outpost-london) [trade-press]: venture incubator, no lab-automation content
- [Yuyao Technology launches MatterSeek materials platform](https://www.prnewswire.com/news-releases/global-launch-of-matterseek-redefining-the-materials-rd-paradigm-with-a-focus-on-industrial-viability-302940318.html) [wires]: materials AI software; automated-lab claim too thin
- [BioNexus BGLC 1Lab pilot at MRNA Scientific](https://www.globenewswire.com/news-release/2026/11/03/3394297/0/en/bionexus-launches-bglc-1lab-pilot-for-genematrix-workflows-at-mrna-scientific.html) [wires]: clinical lab workflow software; 3 Nov, outside window
- [ABLE Labs $8.7M Series A, moving to self-driving labs](https://www.mt.co.kr/en/future/2026/08/31/2026083111374557367) [web]: 31 Aug 2026, outside window
- [Anthropic opens Bay Area wet lab](https://www.staradvertiser.com/2026/09/18/breaking-news/anthropic-sets-up-wet-lab-as-it-expands-ai-drug-program/) [web]: 18 Sep 2026, outside window
- [Insilico LabClaw lab autonomy system](https://www.eurekalert.org/news-releases/1127117) [web]: launched May 2026, outside window
- [Scispot $8M Series A](https://betakit.com/scispot-closes-8-million-usd-series-a-to-become-the-operating-layer-for-life-sciences-labs/) [web]: date not in window / unconfirmed; LIMS software
- [Technology Networks: automation in clinical mass spectrometry](https://www.technologynetworks.com/analysis/articles/advancing-automation-and-workflow-innovation-in-clinical-mass-spectrometry-418096) [trade-press]: clinical opinion piece, no news
- [ELRIG Drug Discovery 2026 award winners](https://elrig.org/drug-discovery-2026-meet-the-elrig-award-winners/) [elrig]: awards post, no automation news
- [ELRIG Protein Sciences in Drug Discovery, 10-11 Nov](https://elrig.org/portfolio/protein-sciences-in-drug-discovery-2026/) [elrig]: already screened out 14 Nov
- [SLAS liquid-handling boot camp and San Diego meet-up, 17-18 Nov](https://www.slas.org/events/) [slas]: routine event listing; screened 14 Nov
- [Exypnos Pivot plate rotator soft launch](https://labautomation.io/t/rotating-plates-90-degrees-around-z-axis/2806) [labautomation-io]: post date unreliable; screened 14 Nov
- [Genentech lab automation job post; Munich meetup](https://labautomation.io/c/job-postings/10) [labautomation-io]: job post / meetup listing
- [Robotic safety in self-driving laboratories (SLAS Technology)](https://www.sciencedirect.com/science/article/pii/S2472630326000774) [slas-technology]: online Aug 2026, outside 14-day window
- [arXiv 2611.18496: telerobotic interventions for resilient SDLs](https://arxiv.org/pdf/2611.18496) [research]: could not open or confirm title/date (arXiv blocked)
- [ChemRxiv sdl-workflows database of 237 SDL papers](https://chemrxiv.org/browse) [research]: primary listing not found
- [Self-Building Labs (arXiv 2610.23826)](https://arxiv.org/html/2610.23826) [research]: October posting, likely outside window; unverifiable
- [PyLabRobot test/type fixes in Mantis PRs](https://github.com/PyLabRobot/pylabrobot/commits/main) [pylabrobot]: folded into weekly roll-up LAN-20261116-02

## Scope: sites and companies

What each site and company produced in this window. To add or remove one, fill in the **Scope** line at the very bottom; the next run applies it to `config/`.

| Site | Tier | Cadence | Checked via | Candidates | Stories |
|---|---|---|---|---:|---:|
| [Labautomation.io (community forum)](https://labautomation.io) | core | daily | site-search | 5 | 0 |
| [PyLabRobot (open-source lab automation library)](https://github.com/PyLabRobot/pylabrobot) | core | daily | feed | 40 | 4 |
| [SLAS (Society for Laboratory Automation and Screening)](https://www.slas.org/news-highlights/news-center/) | core | daily | site-search | 2 | 0 |
| [LRIG (Laboratory Robotics Interest Group) and chapters](https://www.lrig.org) | core | daily | site-search | 0 | 0 |
| [ELRIG (European Laboratory Research & Innovation Group)](https://www.elrig.org) | core | daily | site-search | 3 | 0 |
| [Hamilton Company (Robotics / liquid handling)](https://www.hamiltoncompany.com/automated-liquid-handling) | core | daily | site-search | 3 | 0 |
| [Tecan (lab automation)](https://www.tecan.com/news-archive) | core | daily | site-search | 1 | 0 |
| [Agilent (automation & liquid handling only)](https://www.agilent.com/en/product/automated-liquid-handling) | core | daily | site-search | 4 | 0 |
| [Beckman Coulter (Life Sciences automation + clinical lab automation)](https://www.beckman.com/news) | core | daily | site-search | 0 | 0 |
| [SLAS Discovery (journal)](https://www.sciencedirect.com/journal/slas-discovery) | core | weekly | site-search | 1 | 0 |
| [SLAS Technology (journal)](https://www.sciencedirect.com/journal/slas-technology) | core | weekly | site-search | 2 | 0 |
| [HardwareX (journal, open hardware)](https://www.sciencedirect.com/journal/hardwarex) | core | weekly | site-search | 0 | 0 |
| [PubMed (DMPK/ADME automation first, then pharma/biotech lab automation)](https://pubmed.ncbi.nlm.nih.gov/) | core | weekly | site-search | 2 | 0 |
| Lab trade press | secondary | daily | site-search | 9 | 0 |
| [LinkedIn (posts and articles, via search only)](https://www.linkedin.com/feed/hashtag/labautomation/) | secondary | daily | **not checked** | 0 | 0 |
| Press-release wires | secondary | daily | site-search | 10 | 2 |
| Preprints and other journals | secondary | weekly | site-search | 6 | 1 |
| Open web search (not a listed site) | — | daily | web-search | — | 1 |

**Companies watched** (stories this window):

- Core vendors: Hamilton 1 · Tecan 0 · Agilent 0 · Beckman Coulter 0
- Incumbents: Thermo Fisher 0 · Revvity 0 · Molecular Devices 0 · Eppendorf 0 · Sartorius 0 · Roche Diagnostics 0 · Siemens Healthineers 0 · Abbott 0 · Waters 0 · SPT Labtech 0 · Formulatrix 2 · Analytik Jena 0 · Gilson 0 · INTEGRA Biosciences 0
- Open source: PyLabRobot 4
- Growth: Opentrons 0 · Automata 0 · Biosero 0 · HighRes Biosolutions 0 · Synthace 0 · Benchling 0 · Emerald Cloud Lab 0 · Ginkgo Bioworks 0 · Cellares 0 · Retisoft 0 · Unchained Labs 0
- AI-native: Lila Sciences 0 · Periodic Labs 0 · Chemify 0 · Radical AI 0 · Medra 0 · Trilobio 0 · FutureHouse 0 · Arctoris 0 · Recursion 0

**In the news, not on the watchlist** (add?): Basetwo · CPI · Gyger · Inheco · Labman · Nicoya · PAA · Pierre Fabre · Shanghai Jiao Tong University · Sino Biological · XtalPi

## Details <a id="details"></a>

**1. PyLabRobot weekend: PAA KX2 arm, Gyger CERTUS FLEX dispenser, Mantis v3 hardware** (`LAN-20261116-02`, software-orchestration, published 2026-11-16)
- KX2 arm driver merged 14 Nov (PR #880), with a new CANopen transport in pylabrobot/io [[1]](https://github.com/PyLabRobot/pylabrobot/pull/880)
- CERTUS FLEX driver merged 15 Nov (PR #1637): a 1,237-line device module within 6,367 added lines, with recorded hardware replies as test fixtures [[2]](https://github.com/PyLabRobot/pylabrobot/pull/1637)
- Mantis v3 arm initialisation, pneumatic plate clamp and calibrated LC3 carousel merged 16 Nov (PRs #1633-#1635) [[3]](https://github.com/PyLabRobot/pylabrobot/commit/4924ac1)
- ReplyRouter now drops unsolicited machine lines and never uses command id 0 (PR #1555) [[4]](https://github.com/PyLabRobot/pylabrobot/pull/1555)
- Device registry lists 85 entries after these merges [[5]](https://github.com/PyLabRobot/pylabrobot/blob/067aa1d/docs/_static/devices.json)
- Verifier: facts partial, science sound. Local git confirms each item. KX2 #880 merged 14 Nov (c2a33ca), adding pylabrobot/io/canopen.py. CERTUS FLEX #1637 merged 15 Nov (7d8f270). Mantis #1633-#1635 merged 16 Nov (ff670c6, ff61bcc, 4924ac1). ReplyRouter #1555 merged 16 Nov (067aa1d): it drops spontaneous lines and uses ids 1-9999. devices.json has 85 entries. One wrong detail: CERTUS FLEX is not 'about 1,200 lines'. Its device.py alone is 1,237 lines, and the PR adds 6,367 lines in 36 files.
- Sources: [1] [PyLabRobot PR #880: PAA KX2 arm driver](https://github.com/PyLabRobot/pylabrobot/pull/880) (primary) · [2] [PyLabRobot PR #1637: CERTUS FLEX driver](https://github.com/PyLabRobot/pylabrobot/pull/1637) (primary) · [3] [PyLabRobot merge of #1635 (Mantis LC3 carousel)](https://github.com/PyLabRobot/pylabrobot/commit/4924ac1) (primary) · [4] [PyLabRobot PR #1555: ReplyRouter](https://github.com/PyLabRobot/pylabrobot/pull/1555) (primary) · [5] [PyLabRobot devices.json at 067aa1d](https://github.com/PyLabRobot/pylabrobot/blob/067aa1d/docs/_static/devices.json) (primary)

**2. Explainer: what 'hardware verified' means in PyLabRobot's CERTUS FLEX driver** (`LAN-20261116-03`, liquid-handling, published 2026-11-15)
- Verified on one dispenser with firmware 1.0.7.378-trunk and an angled FLEX8 head; controller replies kept as regression fixtures [[1]](https://github.com/PyLabRobot/pylabrobot/blob/7d8f270/docs/user_guide/gyger/certus_flex/protocol.md)
- Talks to the controller directly over UDP (port 1964) or through the vendor INCO server over TCP (port 7979); no Windows DLL or SiLA needed [[1]](https://github.com/PyLabRobot/pylabrobot/blob/7d8f270/docs/user_guide/gyger/certus_flex/protocol.md)
- Dispense plans accept CSV volume maps, gradients and row/column/snake orders, with pause, resume and abort [[1]](https://github.com/PyLabRobot/pylabrobot/blob/7d8f270/docs/user_guide/gyger/certus_flex/protocol.md)
- Unverified: full travel envelope, other heads, cleaning effectiveness; volumes depend on supplied calibration [[1]](https://github.com/PyLabRobot/pylabrobot/blob/7d8f270/docs/user_guide/gyger/certus_flex/protocol.md)
- Verifier: facts verified, science sound. protocol.md at 7d8f270 confirms everything. Dispenser C196069 runs firmware 1.0.7.378-trunk with an angled FLEX8 head. It uses UDP 1964 or INCO TCP 7979, with no Windows DLL or SiLA. It has CSV maps, gradients, row/column/snake orders, pause/resume/abort, and the stated unverified items. It also says outright that command checks do not prove delivered volume. Caveat: the INCO TCP path was tested only against fixtures, not on hardware.
- Sources: [1] [PyLabRobot: CERTUS FLEX protocol and verification](https://github.com/PyLabRobot/pylabrobot/blob/7d8f270/docs/user_guide/gyger/certus_flex/protocol.md) (primary)

**3. Basetwo, CPI, Labman and Nicoya run fed-batch bioreactors under autonomous AI feed control** (`LAN-20261116-01`, self-driving-labs, published 2026-11-11)
- Announced 11 Nov 2026 by Basetwo AI (Toronto) with CPI, Labman and Nicoya [[1]](https://www.globenewswire.com/news-release/2026/11/11/3400756/0/en/canada-uk-collaboration-demonstrates-autonomous-bioreactor-control-for-a-her2-breast-cancer-therapeutic.html)
- Partners say autonomous control improved viability and titer versus manual control, which ran glucose-limited (company claim, no paper) [[1]](https://www.globenewswire.com/news-release/2026/11/11/3400756/0/en/canada-uk-collaboration-demonstrates-autonomous-bioreactor-control-for-a-her2-breast-cancer-therapeutic.html)
- Works with existing process instrumentation; no extra spectroscopy needed (company claim) [[1]](https://www.globenewswire.com/news-release/2026/11/11/3400756/0/en/canada-uk-collaboration-demonstrates-autonomous-bioreactor-control-for-a-her2-breast-cancer-therapeutic.html)
- Part of the 20-month BALANCE project funded by Innovate UK and NRC IRAP; Labman builds the automated aseptic sub-sampler, Nicoya the Alto SPR titer sensor [[2]](https://www.uk-cpi.com/news/cpi-joins-canada-uk-collaboration-developing-ai-powered-bioreactors-to-revolutionise-biopharmaceutical-manufacturing)
- Verifier: facts partial, science questionable. A search snippet of the GlobeNewswire release (11 Nov 2026) confirms the four partners, closed-loop fed-batch control of trastuzumab, a hybrid model with MPC feeds, existing instrumentation and robotic sampling. Search coverage confirms the BALANCE roles and funders. I could not see the 'better viability and titer than glucose-limited manual control' result or the claim that SPR titer readings fed the controller in this run. The only evidence is the partners' own press release, with no data or paper. CPI is a not-for-profit innovation centre, not a firm.
- Sources: [1] [GlobeNewswire: Canada-UK collaboration demonstrates autonomous bioreactor control](https://www.globenewswire.com/news-release/2026/11/11/3400756/0/en/canada-uk-collaboration-demonstrates-autonomous-bioreactor-control-for-a-her2-breast-cancer-therapeutic.html) (primary) · [2] [CPI: joins Canada-UK BALANCE collaboration](https://www.uk-cpi.com/news/cpi-joins-canada-uk-collaboration-developing-ai-powered-bioreactors-to-revolutionise-biopharmaceutical-manufacturing) (primary)

**4. Pierre Fabre picks XtalPi's AI-plus-robotics platform for oncology small-molecule discovery** (`LAN-20261114-03`, self-driving-labs, published 2026-11-09)
- Announced 9 Nov 2026; scope oncology, potentially dermatology and other diseases [[1]](https://www.prnewswire.com/news-releases/laboratoires-pierre-fabre-and-xtalpi-announce-an-ai-driven-collaboration-focused-on-drug-discovery-302932390.html)
- Pierre Fabre handles disease biology, translational and clinical development [[1]](https://www.prnewswire.com/news-releases/laboratoires-pierre-fabre-and-xtalpi-announce-an-ai-driven-collaboration-focused-on-drug-discovery-302932390.html)
- XtalPi says its autonomous-lab platform orchestrates hundreds of workstations for a 24/7 closed-loop DMTA cycle (company claim, not deal-specific) [[2]](https://en.xtalpi.com/lab_automation/)
- Verifier: facts verified, science questionable. The PR Newswire release title and the 9 Nov 2026 date are confirmed through search snippets and syndicated copies (Macau Business, BioSpectrum Asia, BioPharma APAC). They also confirm the oncology scope, possible expansion to dermatology and rare diseases, Pierre Fabre's role and that no financial terms were given. The '24/7 closed-loop DMTA, hundreds of workstations' line comes only from XtalPi's own marketing, and the item labels it correctly. No deal-specific automation detail was given.
- Sources: [1] [PR Newswire: Pierre Fabre and XtalPi](https://www.prnewswire.com/news-releases/laboratoires-pierre-fabre-and-xtalpi-announce-an-ai-driven-collaboration-focused-on-drug-discovery-302932390.html) (primary) · [2] [XtalPi Autonomous Lab Solution page](https://en.xtalpi.com/lab_automation/) (primary)

**5. Explainer: PyLabRobot drives the PAA KX2 arm over CANopen, not a vendor DLL** (`LAN-20261116-04`, robotics-workcells, published 2026-11-14)
- Needs a CAN-USB adapter via python-can, e.g. SocketCAN can0 on Linux; no vendor DLL [[1]](https://github.com/PyLabRobot/pylabrobot/blob/c2a33ca/docs/user_guide/paa/kx2/installation.md)
- Arm must expose CANopen nodes 1, 2, 3, 4 and 6; optional rail and gripper-less configurations unsupported [[1]](https://github.com/PyLabRobot/pylabrobot/blob/c2a33ca/docs/user_guide/paa/kx2/installation.md)
- The transport serialises SDO transfers and refuses to release a channel while a cancelled transfer is still running [[2]](https://github.com/PyLabRobot/pylabrobot/blob/c2a33ca/pylabrobot/io/canopen.py)
- Optional barcode reader on a separate 9600-baud serial link [[1]](https://github.com/PyLabRobot/pylabrobot/blob/c2a33ca/docs/user_guide/paa/kx2/installation.md)
- Verifier: facts verified, science sound. installation.md and io/canopen.py at c2a33ca confirm all of it: CANopen at 500 kbit/s over python-can (SocketCAN can0) with no vendor DLL; nodes 1, 2, 3, 4 and 6 required; no rail and no gripper-less configurations. The NMT state is saved and restored on teardown, and SDO transfers are serialised under per-node asyncio locks with no channel release while a cancelled transfer runs. The barcode reader runs at 9600 baud.
- Sources: [1] [PyLabRobot: KX2 installation](https://github.com/PyLabRobot/pylabrobot/blob/c2a33ca/docs/user_guide/paa/kx2/installation.md) (primary) · [2] [PyLabRobot: io/canopen.py](https://github.com/PyLabRobot/pylabrobot/blob/c2a33ca/pylabrobot/io/canopen.py) (primary)

**6. PyLabRobot week: Formulatrix Mantis, Inheco ODTC, Hamilton over TCP, finer STAR control** (`LAN-20261114-05`, software-orchestration, published 2026-11-13)
- Mantis: connect, identify, plate clamp, RFID chip tags, arm and Z bring-up, sequencer (PRs 1612, 1621-1623) [[1]](https://github.com/PyLabRobot/pylabrobot/pull/1612)
- Inheco ODTC thermocycler driven through its SiLA 1 interface with the direct device API (PR 1026) [[2]](https://github.com/PyLabRobot/pylabrobot/pull/1026)
- HamiltonTextTCP transport plus UDP-broadcast discover_instruments (PR 1556) [[3]](https://github.com/PyLabRobot/pylabrobot/pull/1556)
- STAR pipette Y moves get a settable default speed of 275 mm/s; Y probe post-detection moves run per channel, enabling parallelism (PRs 1607, 1608) [[4]](https://github.com/PyLabRobot/pylabrobot/pull/1608)
- OT-2: unfinished runs, rail lights and door status readable (PRs 1587, 1588) [[5]](https://github.com/PyLabRobot/pylabrobot/pull/1587)
- 23 of 34 commits on main 8-13 Nov carry an AI-assistant Co-authored-by trailer (git log count) [[6]](https://github.com/PyLabRobot/pylabrobot/commits/main)
- Verifier: facts verified, science questionable. Checked in git: 34 commits on main dated 8-13 Nov, 23 of them with an AI Co-authored-by trailer. The commits for PRs 1612, 1621-1623 (Mantis), 1026 (ODTC over SiLA 1), 1556 (HamiltonTextTCP and discover_instruments), 1607 and 1608 (275 mm/s default Y speed) and 1587/1588 (OT-2) match the claims. Caveats: a legacy ODTC backend already existed, so #1026 is a new implementation rather than a first driver. The Mantis driver cannot dispense yet (design.md: 'the dispensing PR settles them'), so 'schedulable from Python' overstates it for now.
- Sources: [1] [PyLabRobot PR 1612: v1 Mantis](https://github.com/PyLabRobot/pylabrobot/pull/1612) (primary) · [2] [PyLabRobot PR 1026: ODTC direct device API](https://github.com/PyLabRobot/pylabrobot/pull/1026) (primary) · [3] [PyLabRobot PR 1556: HamiltonTextTCP](https://github.com/PyLabRobot/pylabrobot/pull/1556) (primary) · [4] [PyLabRobot PR 1608: STAR Y speed](https://github.com/PyLabRobot/pylabrobot/pull/1608) (primary) · [5] [PyLabRobot PR 1587: OT2 lights and door](https://github.com/PyLabRobot/pylabrobot/pull/1587) (primary) · [6] [PyLabRobot commit history](https://github.com/PyLabRobot/pylabrobot/commits/main) (primary)

**7. Sino Biological launches 4RISE wet-lab validation service for AI-designed proteins** (`LAN-20261114-04`, cloud-labs, published 2026-11-09)
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

> **Brief:** _/5 · **Missed:** _ · **Notes:** _ · `LAN-W20261116`

> **Scope:** Add: _ · Remove: _ · `LAN-S20261116`

Rate stories 1-5 (5 = must-know) and tag freely (`must-know`, `useful`, `meh`, `off-topic`, `wrong`, `unsound`, `hype`, `stale`, `dup`, `shallow`, `great`, `more`, `less`). **Missed**: anything this brief should have had. **Scope**: sites, companies or topics to add or remove, e.g. `Add: Opentrons blog, Automata · Remove: Telescope Innovations`.
