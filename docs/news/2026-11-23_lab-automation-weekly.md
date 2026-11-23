# Lab automation weekly, 23 Nov 2026

17 Nov – 23 Nov 2026 · 3 stories · 2 papers · 0 filtered out · 🎯 your field (DMPK/ADME) · ✅ verified · 🟡 partly verified · ⚪ unverified · ⏳ not yet checked · ⚠️ technical claim questionable · ⛔ technical claim unsupported

## TL;DR
- **Danaher and Microsoft partner on agent-connected instruments**; first app is an imaging assistant, more instruments in 2027 ([release](https://investors.danaher.com/2026-11-20-Danaher-Collaborates-with-Microsoft-to-Make-Scientific-Instruments-Agentically-Connected-and-Laboratories-More-Intelligent)).
- **Learn: Google's VERID** puts a PyLabRobot workcell behind a digital twin; agents must simulate before acting ([blog](https://research.google/blog/grounding-ai-agents-in-biological-reality-building-blocks-for-autonomous-wet-labs/)).
- **PyLabRobot week**: Mantis chips and valves, a STAR crash guard on sideways moves; 16 of 23 commits AI-co-authored ([PR](https://github.com/PyLabRobot/pylabrobot/pull/1659)).
- **A $351 add-on** turns a Tecan Freedom EVO into a 96-well peptide synthesiser (preprint) ([bioRxiv](https://www.biorxiv.org/content/10.64898/2026.11.09.765483v1)).

## Stories

### 1. Danaher and Microsoft partner to make lab instruments agent-connected
✅⚠️ · partnership · Danaher, Microsoft, Molecular Devices · 20 Nov

Danaher and Microsoft announced a strategic partnership to build smart instruments and an interoperable agentic AI platform open to multi-vendor labs. The first application named is Molecular Devices' MetaXpress Acquire AI Assistant for high-content imaging. **Why:** A second big-vendor agent layer over instruments; for ADME labs the test is whether it opens to non-Danaher LC-MS and liquid handlers, not just imaging.

Sources: [Danaher press release](https://investors.danaher.com/2026-11-20-Danaher-Collaborates-with-Microsoft-to-Make-Scientific-Instruments-Agentically-Connected-and-Laboratories-More-Intelligent) · [Drug Target Review](https://www.drugtargetreview.com/danaher-and-microsoft-partner-to-build-ai-powered-intelligent-laboratories/2137059.article) · [GenomeWeb](https://genomeweb.com/business-news/deals/collaboration/gnw-danaher-microsoft-ai-partnership-20261120)

> **Rate:** _/5 · **Tags:** _ · `LAN-20261123-01`

### 2. PyLabRobot week: Mantis chips and arm, STAR traverse guard, CLARIOstar drawer
✅ · product · PyLabRobot, Formulatrix, Hamilton · 22 Nov

PyLabRobot merged 23 commits from 16 to 22 Nov, mostly v1 Formulatrix Mantis work (one arm for v3/v4, chips, valve sequences) plus PreciseFlex arm and gripper fixes. New labware includes KingFisher 96 deep-well and MicroAmp Fast plates. **Why:** Mantis nanolitre dispensing and plate-reader drawer state are common ADME-plate steps; the AI-assisted commit share keeps rising.

Sources: [PyLabRobot PR #1676: Mantis chip valve sequences](https://github.com/PyLabRobot/pylabrobot/pull/1676) · [PyLabRobot PR #1659: STAR X moves raise channels first](https://github.com/PyLabRobot/pylabrobot/pull/1659) · [PyLabRobot PR #1678: CLARIOstar drawer](https://github.com/PyLabRobot/pylabrobot/pull/1678) · [+1 in Details](#details)

> **Rate:** _/5 · **Tags:** _ · `LAN-20261123-02`

### 3. Explainer: how PyLabRobot stops a STAR crashing tips during sideways moves
🟡 · other · PyLabRobot, Hamilton · 18 Nov

Before any X move, the new STAR code reads each channel's lowest Z point, raises any below a traverse height, and lifts the 96/384 head to safe Z. Callers can skip the checks; the iSWAP is not yet covered. **Why:** When an AI agent writes the protocol, guards like this in the driver, not the script, are what keep a mis-planned move from crashing tips.

Sources: [PyLabRobot PR #1659](https://github.com/PyLabRobot/pylabrobot/pull/1659)

> **Rate:** _/5 · **Tags:** _ · `LAN-20261123-03`

## From the journals

SLAS Discovery, SLAS Technology, HardwareX, PubMed and preprints; your field first.

### P1. Explainer: Google's VERID lets AI agents run a PyLabRobot workcell via a digital twin
*arXiv (preprint) / Google Research blog* · Blog: Rao, Sirkovic, Pawlosky; arXiv 2610.32755: Delley et al. (15 authors) · 16 Oct · 🟡⚠️

Google Research's VERID, built on PyLabRobot, keeps a live digital twin of a liquid-handling workcell; agents must pass every command block through simulation before the robot runs it. Missed in October; covered here as a learning piece. **Why:** The clearest public template for AI-run liquid handling: state tracking plus mandatory simulation. Same gate an ADME lab would want before agent-run assays.

[Google Research blog](https://research.google/blog/grounding-ai-agents-in-biological-reality-building-blocks-for-autonomous-wet-labs/) · [Semantic Representation for Agentic Self-Play in Automated Laboratories (arXiv 2610.32755)](https://arxiv.org/pdf/2610.32755) · [FourWeekMBA](https://fourweekmba.com/ai-googles-wet-lab-agents-raise-aptamer-hit-rates-to-42-1/)

> **Rate:** _/5 · **Tags:** _ · `LAN-20261123-05`

### P2. Preprint: $351 add-on turns a Tecan Freedom EVO into a 96-well peptide synthesiser
*bioRxiv (preprint)* · ParSynt-P authors (names not confirmed; bioRxiv page unreachable) · 11 Nov · 🟡

ParSynt-P, a PTFE vacuum/gas manifold plus worklist software, runs up to 96 solid-phase peptide syntheses per run on a Freedom EVO. Built to make peptide standards for targeted plasma proteomics. **Why:** Shows a general pattern: repurpose an existing liquid handler with cheap hardware. Relevant to LC-MS bioanalysis labs needing many stable-isotope peptide standards.

[Affordable 96-parallel SPPS: hardware and software add-on for automated liquid handling platforms (bioRxiv)](https://www.biorxiv.org/content/10.64898/2026.11.09.765483v1)

> **Rate:** _/5 · **Tags:** _ · `LAN-20261123-04`

## Signals to watch (analysis)
- **Big vendors now each pick an AI partner**: Danaher has both NVIDIA and Microsoft; watch whether agent layers open to rival LC-MS and liquid handlers (speculation) ([GenomeWeb](https://genomeweb.com/business-news/deals/collaboration/gnw-danaher-microsoft-ai-partnership-20261120)).
- **Safety is moving into drivers and twins**: VERID's simulation gate and PyLabRobot's traverse guard put checks below the agent, where they belong (analysis) ([PR](https://github.com/PyLabRobot/pylabrobot/pull/1659)).
- **Third quiet week for self-driving-lab start-ups**: no new raise found 16-23 Nov; direct fetches still blocked (analysis) ([run log](https://github.com/bum94587/LabAutoNews/blob/claude/youthful-cerf-akb0aw/data/runs/2026-11-23.json)).

## Filtered out

Screened out during research:

- [Isomorphic Labs raises $5B Series C](https://www.fiercebiotech.com/biotech/isomorphic-labs-raises-5b-series-c-months-after-21b-round) [web]: AI drug-design funding; no confirmed lab-automation use of funds
- [Isomorphic Labs and MSD oncology collaboration](https://www.bioworld.com/articles/735488-isomorphic-labs-and-msd-collaborate-in-cancer-drug-discovery) [web]: computational deal, not lab automation
- [Exypnos Pivot soft launch (forum post)](https://labautomation.io/c/general/1) [labautomation-io]: 10 Nov, outside window; forum post only
- [ELRIG Drug Discovery 2026 award to Peapod Bio](https://elrig.org/drug-discovery-2026-meet-the-elrig-award-winners/) [elrig]: 12 Nov, outside window
- [SLAS Applied Liquid Handling Boot Camp (hosted by Eli Lilly, 17-18 Nov)](https://www.slas.org/events-calendar/applied-liquid-handling-boot-camp/) [slas]: training event listing, no news content
- [SLAS Technology NexusXp special issue, manuscripts due 30 Nov](https://www.slas.org/publications/call-for-papers/) [slas]: call for papers, not news
- [Robotic safety in self-driving laboratories (SLAS Technology vol 42)](https://www.sciencedirect.com/science/article/pii/S2472630326000774) [slas-technology]: online date unconfirmable; page blocked; retry next week
- [Tecan Q3 2026 update raises outlook](https://www.tecan.com/press-center) [tecan]: financial results, 5 Nov, outside window
- [Agilent completes Proscia acquisition](https://www.agilent.com/about/newsroom.html) [agilent]: digital pathology, not lab automation; 4 Nov
- [Agilent 5987A MSD with GC Assist](https://www.agilent.com/about/newsroom.html) [agilent]: GC/MS product, not lab automation; 2 Nov
- [Hamilton and Parallel Fluidics partnership](https://www.hamiltoncompany.com/press-releases/parallel-fluidics-and-hamilton-company-partner-to-automate-advanced-lab-workflows-on-liquid-handlers) [hamilton]: duplicate of LAN-20261109-01
- [Self-Building Labs (arXiv 2610.23826)](https://arxiv.org/pdf/2610.23826) [research]: October posting, outside window; rejected 16 Nov too
- [WuXi AppTec: 20 years of DMPK innovation](https://wuxiapptec.com/crdmo-news/crdmo-impact-in-action/from-exposure-to-insight-20-years-of-dmpk-innovation-at-wuxi-apptec) [web]: company retrospective, undated/August; no new facts
- [Basetwo/CPI/Labman/Nicoya autonomous bioreactor control](https://www.globenewswire.com/news-release/2026/11/11/3400756/0/en/canada-uk-collaboration-demonstrates-autonomous-bioreactor-control-for-a-her2-breast-cancer-therapeutic.html) [wires]: duplicate of LAN-20261116-01
- [X Square Robot WALL-OSS-1.0 foundation model](https://www.globenewswire.com/news-release/2026/11/23/3408046/0/en/x-square-robot-introduces-wall-oss-1-0-understand-more-act-better-a-native-foundation-model-for-the-physical-world.html) [wires]: general robotics, not lab automation
- [coprod raises $6M pre-seed](https://prnewswire.com/news-releases/coprod-raises-6m-to-make-robot-hardware-as-easy-to-build-as-software-302947695.html) [wires]: general robot hardware, not lab-specific
- [Singularity Hub: AI agents ran a biology lab](https://singularityhub.com/2026/11/10/ai-agents-ran-a-biology-lab-humans-popped-in-to-empty-the-trash/) [web]: 10 Nov, outside window; covers AutoDNA (LAN-20261114-01)
- [PyLabRobot labware additions (Cellvis P384, 12x75 tube)](https://github.com/PyLabRobot/pylabrobot/pull/1523) [pylabrobot]: folded into weekly roll-up LAN-20261123-02

## Scope: sites and companies

What each site and company produced in this window. To add or remove one, fill in the **Scope** line at the very bottom; the next run applies it to `config/`.

| Site | Tier | Cadence | Checked via | Candidates | Stories |
|---|---|---|---|---:|---:|
| [Labautomation.io (community forum)](https://labautomation.io) | core | daily | site-search | 1 | 0 |
| [PyLabRobot (open-source lab automation library)](https://github.com/PyLabRobot/pylabrobot) | core | daily | feed | 23 | 3 |
| [SLAS (Society for Laboratory Automation and Screening)](https://www.slas.org/news-highlights/news-center/) | core | daily | site-search | 3 | 0 |
| [LRIG (Laboratory Robotics Interest Group) and chapters](https://www.lrig.org) | core | daily | site-search | 0 | 0 |
| [ELRIG (European Laboratory Research & Innovation Group)](https://www.elrig.org) | core | daily | site-search | 2 | 0 |
| [Hamilton Company (Robotics / liquid handling)](https://www.hamiltoncompany.com/automated-liquid-handling) | core | daily | site-search | 1 | 0 |
| [Tecan (lab automation)](https://www.tecan.com/news-archive) | core | daily | site-search | 1 | 0 |
| [Agilent (automation & liquid handling only)](https://www.agilent.com/en/product/automated-liquid-handling) | core | daily | site-search | 2 | 0 |
| [Beckman Coulter (Life Sciences automation + clinical lab automation)](https://www.beckman.com/news) | core | daily | site-search | 0 | 0 |
| [SLAS Discovery (journal)](https://www.sciencedirect.com/journal/slas-discovery) | core | weekly | site-search | 0 | 0 |
| [SLAS Technology (journal)](https://www.sciencedirect.com/journal/slas-technology) | core | weekly | site-search | 1 | 0 |
| [HardwareX (journal, open hardware)](https://www.sciencedirect.com/journal/hardwarex) | core | weekly | site-search | 0 | 0 |
| [PubMed (DMPK/ADME automation first, then pharma/biotech lab automation)](https://pubmed.ncbi.nlm.nih.gov/) | core | weekly | site-search | 0 | 0 |
| Lab trade press | secondary | daily | site-search | 3 | 1 |
| [LinkedIn (posts and articles, via search only)](https://www.linkedin.com/feed/hashtag/labautomation/) | secondary | daily | site-search | 1 | 0 |
| Press-release wires | secondary | daily | site-search | 3 | 0 |
| Preprints and other journals | secondary | weekly | site-search | 3 | 1 |

**Companies watched** (stories this window):

- Core vendors: Hamilton 2 · Tecan 1 · Agilent 0 · Beckman Coulter 0
- Incumbents: Thermo Fisher 0 · Revvity 0 · Molecular Devices 1 · Eppendorf 0 · Sartorius 0 · Roche Diagnostics 0 · Siemens Healthineers 0 · Abbott 0 · Waters 0 · SPT Labtech 0 · Formulatrix 1 · Analytik Jena 0 · Gilson 0 · INTEGRA Biosciences 0
- Open source: PyLabRobot 3
- Growth: Opentrons 0 · Automata 0 · Biosero 0 · HighRes Biosolutions 0 · Synthace 0 · Benchling 0 · Emerald Cloud Lab 0 · Ginkgo Bioworks 0 · Cellares 0 · Retisoft 0 · Unchained Labs 0
- AI-native: Lila Sciences 0 · Periodic Labs 0 · Chemify 0 · Radical AI 0 · Medra 0 · Trilobio 0 · FutureHouse 0 · Arctoris 0 · Recursion 0

**In the news, not on the watchlist** (add?): BMG Labtech · Brooks · Danaher · Google · Microsoft

## Details <a id="details"></a>

**1. Danaher and Microsoft partner to make lab instruments agent-connected** (`LAN-20261123-01`, software-orchestration, published 2026-11-20)
- Press release dated 20 Nov 2026 on Danaher's investor site [[1]](https://investors.danaher.com/2026-11-20-Danaher-Collaborates-with-Microsoft-to-Make-Scientific-Instruments-Agentically-Connected-and-Laboratories-More-Intelligent)
- More agent-enabled instruments from Danaher businesses planned for 2027; first commercial applications expected in 2026 [[1]](https://investors.danaher.com/2026-11-20-Danaher-Collaborates-with-Microsoft-to-Make-Scientific-Instruments-Agentically-Connected-and-Laboratories-More-Intelligent)
- Preliminary internal company testing on a Leica microscope workflow: novices with an AI assistant took up to 83% less time and up to 68% fewer steps (unverified) [[2]](https://www.drugtargetreview.com/danaher-and-microsoft-partner-to-build-ai-powered-intelligent-laboratories/2137059.article)
- Follows Danaher's NVIDIA collaboration (14 Oct) and its Abcam autonomous-lab plan (7 Oct) [[3]](https://genomeweb.com/business-news/deals/collaboration/gnw-danaher-microsoft-ai-partnership-20261120)
- Verifier: facts verified, science questionable. Danaher's 20 Nov 2026 release (title and date via search snippet; site not fetchable) plus Drug Target Review, GenomeWeb and Fierce confirm the partnership on Azure/Foundry, MetaXpress Acquire AI Assistant as the first application in 2026, and more agent-enabled instruments in 2027. The 83% time / 68% steps figures come from preliminary internal testing on a Leica microscope workflow, not the MetaXpress assistant, which is a product-support tool rather than instrument control. They are company maximums with no independent data.
- Sources: [1] [Danaher press release](https://investors.danaher.com/2026-11-20-Danaher-Collaborates-with-Microsoft-to-Make-Scientific-Instruments-Agentically-Connected-and-Laboratories-More-Intelligent) (primary) · [2] [Drug Target Review](https://www.drugtargetreview.com/danaher-and-microsoft-partner-to-build-ai-powered-intelligent-laboratories/2137059.article) (secondary) · [3] [GenomeWeb](https://genomeweb.com/business-news/deals/collaboration/gnw-danaher-microsoft-ai-partnership-20261120) (secondary)

**2. PyLabRobot week: Mantis chips and arm, STAR traverse guard, CLARIOstar drawer** (`LAN-20261123-02`, software-orchestration, published 2026-11-22)
- Mantis: single arm model for v3 and v4 with zone routes and approach paths (#1631); chips, nozzles and per-slot chip spots (#1670); per-chip valve sequences (#1676); chip pick and place (#1677) [[1]](https://github.com/PyLabRobot/pylabrobot/pull/1676)
- STAR v1: X moves first raise low channels and the 96/384 head to a minimum traverse height (#1659) [[2]](https://github.com/PyLabRobot/pylabrobot/pull/1659)
- CLARIOstar v1: the plate holder now follows the drawer in and out (#1678) [[3]](https://github.com/PyLabRobot/pylabrobot/pull/1678)
- 16 of the 23 commits carry a Claude co-author trailer (count from git log) [[4]](https://github.com/PyLabRobot/pylabrobot/commits/main)
- Verifier: facts verified, science sound. git log on main confirms 23 first-parent commits after the last commit covered on 16 Nov (067aa1d, #1555) up to 46d068a (22 Nov), and 16 of them carry a Claude Co-authored-by trailer. Subjects of #1631, #1670, #1676, #1677, #1659 and #1678, the PreciseFlex arm and gripper commits (#1671-#1674), and the KingFisher (#1658) and MicroAmp Fast (#1655) plates all match.
- Sources: [1] [PyLabRobot PR #1676: Mantis chip valve sequences](https://github.com/PyLabRobot/pylabrobot/pull/1676) (primary) · [2] [PyLabRobot PR #1659: STAR X moves raise channels first](https://github.com/PyLabRobot/pylabrobot/pull/1659) (primary) · [3] [PyLabRobot PR #1678: CLARIOstar drawer](https://github.com/PyLabRobot/pylabrobot/pull/1678) (primary) · [4] [PyLabRobot commit log](https://github.com/PyLabRobot/pylabrobot/commits/main) (primary)

**3. Explainer: how PyLabRobot stops a STAR crashing tips during sideways moves** (`LAN-20261123-03`, liquid-handling, published 2026-11-18)
- move_to_x_position raises 'everything low on the arm first, then the arm'; height defaults to default_minimum_traverse_height, and 0 raises nothing [[1]](https://github.com/PyLabRobot/pylabrobot/pull/1659)
- Raises ValueError if a channel cannot be lifted to the required height [[1]](https://github.com/PyLabRobot/pylabrobot/pull/1659)
- perform_safety_checks=False sends the move without reads or raises; a TODO notes the iSWAP is excluded until its safety design is decided [[1]](https://github.com/PyLabRobot/pylabrobot/pull/1659)
- Change: 177 lines added, 65 removed; tests file +64/-3 [[1]](https://github.com/PyLabRobot/pylabrobot/pull/1659)
- The low-channel raise already existed for XY moves; this change applies it to X-only moves and adds the head raise [[1]](https://github.com/PyLabRobot/pylabrobot/pull/1659)
- Verifier: facts partial, science sound. The diff of 21207d4 (#1659, 18 Nov) confirms the docstring, the default_minimum_traverse_height default, '0 raises nothing', ValueError, perform_safety_checks=False and the iSWAP TODO. The 96/384 head goes to its safe Z, not to the traverse height. Line counts are 177 added and 65 removed overall, but the tests are +64/-3, not 67 new lines. The channel-raise helper already existed for XY moves; this commit adds it to X moves along with the head raise.
- Sources: [1] [PyLabRobot PR #1659](https://github.com/PyLabRobot/pylabrobot/pull/1659) (primary)

**P1. Explainer: Google's VERID lets AI agents run a PyLabRobot workcell via a digital twin** (`LAN-20261123-05`, self-driving-labs, published 2026-10-16)
- Blog post 'Grounding AI agents in biological reality' dated 16 Oct 2026 (Rao, Sirkovic, Pawlosky) [[1]](https://research.google/blog/grounding-ai-agents-in-biological-reality-building-blocks-for-autonomous-wet-labs/)
- Digital twin tracks arm geometry, well volumes, reagent identities and tip inventory; services: introspection, time-compressed simulation, multimodal trace logging, safe execution [[2]](https://arxiv.org/pdf/2610.32755)
- Agent improved reconstruction of unknown dye mixtures more than 5x across cycles; twin state let it recover from a plate-reader failure without re-pipetting [[1]](https://research.google/blog/grounding-ai-agents-in-biological-reality-building-blocks-for-autonomous-wet-labs/)
- A separate aptamer study (arXiv 2610.24806) reports bead-corrected hit rates of 42.1% (alpha-thrombin) and 33.5% (myoglobin) by round 3, with humans running pulldown, PCR and sequencing between rounds [[3]](https://fourweekmba.com/ai-googles-wet-lab-agents-raise-aptamer-hit-rates-to-42-1/)
- Verifier: facts partial, science questionable. The 16 Oct 2026 Google blog (via snippets) confirms VERID on PyLabRobot, twin state, no unverified code to the robot, the >5x dye result and the plate-reader recovery. The arXiv 2610.32755 authors are Delley +14, not Rao/Sirkovic/Pawlosky (who wrote the blog). The 42.1%/33.5% aptamer rates come from a separate preprint (arXiv 2610.24806), where humans did the wet-lab work between rounds, so that loop was not robot-autonomous. Out of window (16 Oct), as intended.
- Sources: [1] [Google Research blog](https://research.google/blog/grounding-ai-agents-in-biological-reality-building-blocks-for-autonomous-wet-labs/) (primary) · [2] [Semantic Representation for Agentic Self-Play in Automated Laboratories (arXiv 2610.32755)](https://arxiv.org/pdf/2610.32755) (paper) · [3] [FourWeekMBA](https://fourweekmba.com/ai-googles-wet-lab-agents-raise-aptamer-hit-rates-to-42-1/) (secondary)

**P2. Preprint: $351 add-on turns a Tecan Freedom EVO into a 96-well peptide synthesiser** (`LAN-20261123-04`, open-hardware, published 2026-11-11)
- Hardware cost $351; synthesis cost $0.23 per coupling and $1.14 per mg crude product (authors' figures, not peer reviewed) [[1]](https://www.biorxiv.org/content/10.64898/2026.11.09.765483v1)
- One residue coupling takes 94 min; software generates robot worklists from a peptide sequence table and switches gas and vacuum [[1]](https://www.biorxiv.org/content/10.64898/2026.11.09.765483v1)
- Uniformity tested on three fully loaded plates with a NAT/SIL standard pair [[1]](https://www.biorxiv.org/content/10.64898/2026.11.09.765483v1)
- Verifier: facts partial, science sound. A bioRxiv search snippet confirms the title, ParSynt-P on a Tecan Freedom EVO, the PTFE manifold, up to 96 syntheses per run, 94 min per coupling, $351 hardware, $0.23 per coupling and $1.14/mg, and testing on three fully loaded plates for plasma-proteomics standards. Not confirmed: the NAT/SIL standard pair, the authors, and the 11 Nov posting date (the DOI suffix implies on or after 9 Nov, so it is in the 14-day window). The figures are plausible, but the evidence level is a non-peer-reviewed preprint.
- Sources: [1] [Affordable 96-parallel SPPS: hardware and software add-on for automated liquid handling platforms (bioRxiv)](https://www.biorxiv.org/content/10.64898/2026.11.09.765483v1) (paper)

## Feedback

> **Brief:** _/5 · **Missed:** _ · **Notes:** _ · `LAN-W20261123`

> **Scope:** Add: _ · Remove: _ · `LAN-S20261123`

Rate stories 1-5 (5 = must-know) and tag freely (`must-know`, `useful`, `meh`, `off-topic`, `wrong`, `unsound`, `hype`, `stale`, `dup`, `shallow`, `great`, `more`, `less`). **Missed**: anything this brief should have had. **Scope**: sites, companies or topics to add or remove, e.g. `Add: Opentrons blog, Automata · Remove: Telescope Innovations`.
