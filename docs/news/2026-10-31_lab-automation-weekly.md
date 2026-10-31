# Lab automation weekly, 31 Oct 2026

Week of 2026-10-01 to 2026-10-31. 8 stories from 11 items found by the daily research runs. Every story links to its sources; badges show what the independent verifier agent could confirm. Fill in the **Rate** lines in the myday viewer (Edit) so the next runs learn what you want.

*First issue: an October backfill, so it covers the whole month rather than one week. From
next Monday each brief covers the previous seven days.*

## TL;DR
- **Opentrons raised a $40M Series E** led by Avego, pitching its open, API-driven robots as the physical layer for AI-driven science ([press release](https://www.biospace.com/press-releases/opentrons-announces-40m-series-e-round-to-standardize-ai-driven-science-on-its-robots)).
- **Self-driving labs are scaling up as infrastructure**: SLAC leads SPIRE, a DOE-selected, five-partner autonomous-experiment platform ([SLAC](https://www6.slac.stanford.edu/news/2026-10-08-slac-leads-new-project-build-self-driving-laboratory-future)), and Texas A&M is building an AI foundry for alloys ([Texas A&M](https://stories.tamu.edu/news/2026/10/26/texas-am-to-create-ai-powered-foundry-for-faster-alloy-discovery/)).
- **Agilent automated flow-cytometry sample prep** with NovoStation; the >90% hands-on-time reduction is so far Agilent's own data ([Agilent](https://www.agilent.com/about/newsroom/presrel/2026/01oct-ca26033.html)).
- **Quiet month for Hamilton and Beckman**: no October lab-automation releases found in search (direct site checks are blocked from the cloud; see Coverage).

## Signals to watch (analysis)
- **"AI needs a physical lab" is now the funding and valuation story** at both ends of the market: Opentrons' round ([Axios Pro](https://www.axios.com/pro/biotech-deals/2026/10/29/opentrons-labworks-raises-40m)) and Tecan's ~92% share rally ([Yahoo Finance](https://finance.yahoo.com/markets/stocks/articles/tecan-group-swx-tecn-stock-010902622.html)). Speculation: expect more incumbents to rebrand workcells as "AI-ready", so watch for real closed loops versus scripted workflows. Tecan's 5 Nov Q3 update is the next data point.
- **Integration is still the pain point.** ELRIG's framing is about connecting instruments into low-touch workflows ([Drug Target Review](https://www.drugtargetreview.com/news/self-driving-labs-and-advanced-cell-models-feature-at-elrig-2026/2136745.article)), and community effort on labautomation.io goes into simulation and firmware-level control ([thread](https://labautomation.io/t/alpha-testers-wanted-protocol-factory-live-opentrons-protocol-simulation-in-vscode/8101)).
- **Vendor-bundled front-end automation**: Agilent's NovoStation pairs a cytometer with its own prep robot, a pattern to watch at Beckman (Biomek + CytoFLEX) and Tecan.

## Top stories

### 1. Opentrons raises $40M Series E led by Avego to scale AI-driven lab automation
*Funding · Funding, M&A, partnerships, leadership, market · Opentrons · published 2026-10-29*  
✅ facts verified

Opentrons Labworks raised a $40M Series E led by healthcare investor Avego, with BroadOak Capital Partners participating. The company says it will use the money to scale its robotics, software and data infrastructure and expand into new markets. Coverage cites more than 11,000 Opentrons robots deployed in over 80 countries. [1] [2] [3] [4] [5]

- $40M Series E led by Avego; BroadOak Capital Partners participated [1]
- >11,000 robots deployed in >80 countries [1]
- Reported by Axios Pro the same day [3]

**Why it matters (analysis):** Opentrons is the low-cost, open-API end of liquid handling. A late-stage round pitched on 'AI needs physical labs' shows investors still back that bet. It follows a ~$20.1M round in Dec 2025 (CB Insights) and is far smaller than the $200M Series C of 2021; valuation not disclosed (analysis: possibly flat or down).

**Verifier:** Primary press release (via BioSpace/RoboticsTomorrow, 29 Oct 2026) confirms $40M Series E led by Avego with BroadOak Capital Partners, use of funds and >11,000 robots in >80 countries; Axios Pro (CEO James Atwood) and GEN corroborate. Rests on search snippets: WebFetch to siliconangle, citybiz, finsmes and axios failed (ENOTFOUND), and the SiliconANGLE ref itself was not seen in any result.

Sources: [1] [Opentrons press release (BioSpace)](https://www.biospace.com/press-releases/opentrons-announces-40m-series-e-round-to-standardize-ai-driven-science-on-its-robots) (primary) · [2] [SiliconANGLE](https://siliconangle.com/2026/10/29/science-robotics-startup-opentrons-raises-40m-to-standardize-laboratory-automation/) (secondary) · [3] [Axios Pro](https://www.axios.com/pro/biotech-deals/2026/10/29/opentrons-labworks-raises-40m) (secondary) · [4] [citybiz (press release text)](https://www.citybiz.co/article/926621/opentrons-raises-40-million-series-e-led-by-avego-to-expand-ai-driven-laboratory-automation/) (secondary) · [5] [FinSMEs](https://www.finsmes.com/2026/10/opentrons-labworks-raises-40m-in-series-e-funding.html) (secondary)

> **Rate:** _/5 · **Tags:** _ · `LAN-20261031-01`

### 2. SLAC leads SPIRE, a multi-lab project to build self-driving experiments at X-ray and electron facilities
*Research · Self-driving labs / autonomous discovery / AI scientists · SLAC, Argonne, Brookhaven, LBNL · published 2026-10-08*  
✅ facts verified

SLAC National Accelerator Laboratory is leading a new project in which AI agents, robots and instrumented detectors run experiments end to end across SLAC's X-ray and electron user facilities. Partners include Stanford, the University of Chicago, Argonne, Brookhaven and Lawrence Berkeley national laboratories. SLAC says the platform keeps existing hardware safety systems and human control of scientific objectives. SPIRE is a DOE Genesis Mission selection, announced at the Golden Age of Science Summit and still under award negotiation. [1] [2] [3] [4]

- Partners: Stanford, UChicago, Argonne, Brookhaven, LBNL [1]
- Announced 8 Oct 2026 [1]
- DOE Genesis Mission selection, under negotiation [4]

**Why it matters (analysis):** A national-lab consortium treating autonomy as shared infrastructure (reusable agents, robots, detectors) rather than one-off demos. Whether the loop really closes, with the system choosing the next experiment, is what to watch in its first results.

**Verifier:** SLAC release dated 8 Oct 2026 (also on Newswise) confirms SPIRE, the five partners, the end-to-end AI-agent/robot/detector aim, and that hard-wired safety systems stay with researchers setting scientific goals. It is a project announcement with no results yet, so there is no autonomy claim to assess. Per coverage it is a DOE Genesis Mission selection for negotiation, not a final funding award. Based on search snippets (SLAC domain not fetched).

Sources: [1] [SLAC news release](https://www6.slac.stanford.edu/news/2026-10-08-slac-leads-new-project-build-self-driving-laboratory-future) (primary) · [2] [Newswise (DOE science)](https://www.newswise.com/doescience/slac-leads-new-project-to-build-the-self-driving-laboratory-of-the-future) (secondary) · [3] [ORNL Autonomous Science (DOE selections context)](https://www.ornl.gov/autonomous-science/) (secondary) · [4] [ExecutiveGov: SPIRE and the Genesis Mission](https://www.executivegov.com/articles/slac-spire-doe-autonomous-lab-genesis-mission) (secondary)

> **Rate:** _/5 · **Tags:** _ · `LAN-20261031-02`

### 3. Agilent launches NovoStation to automate flow cytometry sample preparation
*Product · Liquid handling & benchtop automation · Agilent · published 2026-10-01*  
✅ facts verified · ⚠️ science/engineering questionable

Agilent introduced the NovoStation Sample Preparation System, which automates 96-well flow cytometry sample prep including onboard reagent cocktailing and washing. It runs standalone or connected to Agilent NovoCyte cytometers. Agilent claims more than 90% less hands-on time with data comparable to manual prep, based on its own studies; announced 1 Oct and unveiled at ICCS 2026 (2-6 Oct). [1] [2] [3] [4]

- >90% reduction in hands-on time vs manual (Agilent's own validation) [1]
- Application notes: 25-colour PBMC immunophenotyping; kappa/lambda light chains [3]
- Kappa/lambda app note [4]

**Why it matters (analysis):** Flow cytometry prep is still largely manual pipetting; a cytometer vendor bundling its own prep robot is the 'vertical workcell' pattern (instrument + front-end automation from one vendor). The 90% figure is vendor data; independent user reports will matter.

**Verifier:** Agilent's 1 Oct 2026 release confirms the launch, standalone/NovoCyte integration, unveiling at ICCS 2026 (2-6 Oct) and '>90%' hands-on-time reduction (7.9 vs 85.5 min for 30 samples, 25-colour; 6.8 vs 89.4 min, kappa/lambda). Both app notes exist. The time savings are plausible for walk-away prep but come only from Agilent app notes, with no independent data. Based on search snippets (agilent.com not fetched).

Sources: [1] [Agilent press release](https://www.agilent.com/about/newsroom/presrel/2026/01oct-ca26033.html) (primary) · [2] [Agilent product page](https://www.agilent.com/en/product/research-flow-cytometry/flow-cytometers/flow-cytometry-automation/novostation-sample-preparation-system) (primary) · [3] [Agilent application note (25-colour PBMC)](https://www.agilent.com/cs/library/applications/an-automated-25-color-immunophenotyping-human-pbmcs-5994-9416en-agilent.pdf) (data) · [4] [Agilent application note (kappa/lambda, 5994-9401EN)](https://www.agilent.com/cs/library/applications/an-automated-sample-prep-kappa-lamda-novostation-5994-9401en-agilent.pdf) (data)

> **Rate:** _/5 · **Tags:** _ · `LAN-20261031-03`

### 4. Tecan shares up ~92% this year as investors price in lab-automation demand
*Market · Funding, M&A, partnerships, leadership, market · Tecan, NVIDIA · published 2026-10-30*  
🟡 facts partly verified

Investor coverage on 29-30 October reports Tecan Group shares up about 92.5% year to date, with commentary tying the rally to demand for lab automation in AI-driven labs. Earlier in 2026 Tecan added agentic AI features with NVIDIA to its Introspect lab analytics platform. [1] [2] [3]

- +92.5% YTD (Simply Wall St analysis, syndicated on Yahoo Finance; not two independent sources) [2]
- Tecan/NVIDIA agentic AI in Introspect (June 2026) [3]

**Why it matters (analysis):** Analysis: the market is rewarding the 'AI needs automated wet labs' story at an incumbent, not just at startups. This is commentary, not a company announcement; watch Tecan's Q3 trading update (5 Nov) for whether orders back it.

**Verifier:** The Yahoo Finance piece ('Could Be A Bargain On Its 92% Run', syndicated Simply Wall St content, so not independent of the Simply Wall St ref) confirms +92.5% YTD, and Tecan/NVIDIA agentic AI in Introspect is confirmed (24 Jun 2026). CHF 255.20 was not found anywhere, and +92.5% implies a base near CHF 132.6 vs Tecan's 2025 close of CHF 128.50. This is algorithmic market commentary, not a company announcement; Tecan reports on 5 Nov.

Sources: [1] [Yahoo Finance](https://finance.yahoo.com/markets/stocks/articles/tecan-group-swx-tecn-stock-010902622.html) (secondary) · [2] [Simply Wall St](https://simplywall.st/stocks/ch/pharmaceuticals-biotech/vtx-tecn/tecan-group-shares/news/should-ai-lab-demand-require-action-from-tecan-swxtecn-inves/amp) (secondary) · [3] [CLP: Tecan and NVIDIA add AI to Introspect](https://clpmag.com/lab-management/company-news/tecan-nvidia-add-ai-introspect-lab-analytics-platform/) (secondary)

> **Rate:** _/5 · **Tags:** _ · `LAN-20261031-06`

### 5. SLAS, ELRIG and One Nucleus team up again for London Bio-Innovation Week, 7-11 Dec 2026
*Event · Conferences, user groups, community discussion · SLAS, ELRIG, One Nucleus · published 2026-10-14*  
✅ facts verified

SLAS, ELRIG and One Nucleus announced they will collaborate on the second London Bio-Innovation Week, 7-11 December 2026, with cross-event networking and partnering. The week is a set of independently organised events across London. [1] [2] [3]

- Dates 7-11 December 2026; announced 14 Oct 2026 [1]

**Why it matters (analysis):** SLAS and ELRIG keep co-programming in the UK, which makes London in December a fixture in the European lab-automation calendar alongside SLAS Europe in May.

**Verifier:** Joint release dated 14 Oct 2026 (Newswise, One Nucleus, EurekAlert, Cambridge Network) confirms One Nucleus, SLAS and ELRIG collaborating on the second London Bio-Innovation Week, 7-11 Dec 2026, with cross-event networking and independently organised events. The slas.org news page was not reachable; confirmed via search snippets.

Sources: [1] [Joint release (Newswise)](https://www.newswise.com/articles/leading-life-science-organisations-collaborate-for-second-London-Bio-Innovation-Week) (primary) · [2] [Cambridge Network](https://www.cambridgenetwork.co.uk/news/leading-life-science-organisations-collaborate-second-london-bio-innovation-week) (secondary) · [3] [SLAS 2026 news releases](https://www.slas.org/news-highlights/news-center/2026-news-releases/) (primary)

> **Rate:** _/5 · **Tags:** _ · `LAN-20261031-04`

## More this week

#### Self-driving labs / autonomous discovery / AI scientists

### Texas A&M gets $2M WoodNext grant for an 'Aggie AI Foundry' for automated alloy development
*Research · Self-driving labs / autonomous discovery / AI scientists · Texas A&M · published 2026-10-26*  
✅ facts verified · ⚠️ science/engineering questionable

Texas A&M announced a $2M WoodNext Foundation grant to its materials science department for the Aggie AI Foundry, an automated, AI-driven lab for metal alloys that it says could cut development from months to about a week. It is a separate award from the NSF-funded autonomous metals platform (ARM-MIP) Texas A&M announced in August; Raymundo Arróyave is involved in both. [1] [2] [3]

- $2M WoodNext Foundation grant (confirmed by Texas A&M) [1]
- ARM-MIP: separate NSF-funded national self-driving metals lab, announced Aug 2026 [3]

**Why it matters (analysis):** Self-driving labs are spreading from chemistry and biology into metallurgy, where synthesis and testing are slow and expensive. 'Months to a week' is a goal for a facility not yet built.

**Verifier:** Texas A&M's own story (26 Oct 2026) confirms the $2M WoodNext Foundation grant for the Aggie AI Foundry (Karaman, Arróyave), so this is not single-outlet. ARM-MIP (~$25M NSF, Aug 2026) is confirmed and is a separate award. The 'months to a week or less' figure is a goal for an unbuilt facility, not a demonstrated result. Based on search snippets.

Sources: [1] [Texas A&M Today](https://stories.tamu.edu/news/2026/10/26/texas-am-to-create-ai-powered-foundry-for-faster-alloy-discovery/) (primary) · [2] [Interesting Engineering](https://interestingengineering.com/ai-robotics/us-foundry-lab-robots-alloy-discovery) (secondary) · [3] [Texas A&M Engineering (ARM-MIP)](https://news.engineering.tamu.edu/news/2026/08/03/texas-am-to-build-first-national-self-driving-laboratory-for-metals-open-to-researchers-nationwide/) (primary)

> **Rate:** _/5 · **Tags:** _ · `LAN-20261031-07`

#### Scheduling, orchestration, LIMS/ELN, data & device integration

### Labautomation.io: alpha testers wanted for 'Protocol Factory', live Opentrons protocol simulation in VS Code
*Community · Scheduling, orchestration, LIMS/ELN, data & device integration · Opentrons, Hamilton · published 2026-10-06*  
🟡 facts partly verified

A community developer is recruiting alpha testers on Labautomation.io for Protocol Factory, a VS Code extension that simulates Opentrons protocols live while they are written (posted around 6 Oct; exact date unconfirmed). Other active threads this month covered Hamilton VENUS firmware commands and clot detection during aspiration. [1] [2] [3]

- Thread posted around 6 Oct 2026 [1]

**Why it matters (analysis):** Tooling for writing and testing protocols is still community-built; fast simulation is a precondition for AI-generated protocols to be safe to run.

**Verifier:** The Protocol Factory alpha-tester thread exists (developer Koji, private alpha, ~10 testers, not affiliated with Opentrons), and a 'Clot Detection Not Triggering During Aspiration' VENUS thread was active 10 Oct. However, the Protocol Factory post appears to date from about 6 Oct, so '10 Oct' looks borrowed from the clot thread, and the refs are category pages rather than the thread. Based on search snippets (labautomation.io not fetched).

Sources: [1] [Labautomation.io thread: Protocol Factory](https://labautomation.io/t/alpha-testers-wanted-protocol-factory-live-opentrons-protocol-simulation-in-vscode/8101) (primary) · [2] [Labautomation.io Opentrons category](https://labautomation.io/c/opentrons/9) (primary) · [3] [Labautomation.io Hamilton (VENUS) category](https://labautomation.io/c/hamilton-venus/7) (primary)

> **Rate:** _/5 · **Tags:** _ · `LAN-20261031-08`

#### Conferences, user groups, community discussion

### ELRIG Drug Discovery 2026 (London) puts self-driving lab infrastructure on the agenda
*Event · Conferences, user groups, community discussion · ELRIG, Peak Analysis & Automation · published 2026-10-14*  
🟡 facts partly verified

ELRIG Drug Discovery 2026 ran 14-15 October at ExCeL London, its 20th year. Preview coverage highlighted laboratory automation, including Peak Analysis & Automation's work on the infrastructure needed for self-driving labs, alongside advanced cell models and imaging. [1] [2]

- 14-15 Oct 2026, ExCeL London [1]
- 20th ELRIG Drug Discovery [2]

**Why it matters (analysis):** Integration (instruments into low-touch workflows) remains the stated pain point at Europe's largest free-to-attend drug discovery conference (the organiser's description), which is the gap self-driving-lab vendors are selling into.

**Verifier:** Dates (14-15 Oct 2026), ExCeL London, 20th edition and PAA's self-driving-lab infrastructure topic are confirmed (Drug Target Review, Eppendorf, European Biotechnology). However, `published` is the event start date: the DTR preview's own publication date was not found, and the preview gives no detail of what PAA presented. Based on search snippets.

Sources: [1] [Drug Target Review preview](https://www.drugtargetreview.com/news/self-driving-labs-and-advanced-cell-models-feature-at-elrig-2026/2136745.article) (secondary) · [2] [Eppendorf event page](https://www.eppendorf.com/se-en/company-careers/events/elrig-drug-discovery-2026/) (secondary)

> **Rate:** _/5 · **Tags:** _ · `LAN-20261031-05`

## Verification log

Shown: partial 3, verified 5.

Left out:
- Telescope Innovations hosts Canadian officials at the self-driving lab it supplied to Korea's KPBMA (`LAN-20261031-09`, hold, verified): Telescope Innovations' press release (Newsfile via Stockhouse/StockTitan) dated 29 Oct 2026 confirms Canadian officials toured the self-driving lab it installed at KPBMA in Seoul (installed Dec 2025), tied to the BIX 2026 delegation. The hold reason is confirmed: it is a visit story with no new capability. Based on search snippets. — [Stockhouse (press release)](https://stockhouse.com/news/press-releases/2026/10/29/senior-canadian-officials-and-diplomatic-leaders-tour-the-self-driving-lab)
- Hamilton and Biosero co-marketing agreement (resurfaced as new) (`LAN-20261031-10`, drop, verified): Drop reason confirmed: the Hamilton-Biosero co-marketing agreement was announced 9 May 2023 (Business Wire, Biosero, News-Medical), outside the window. The October 2026 date on the BICO blog was not confirmed, and BICO is Biosero's parent company, not an aggregator. — [Business Wire, 9 May 2023](https://www.businesswire.com/news/home/20230509005128/en)
- Imperial spinout Machenta raises $40M seed for robot learning (`LAN-20261031-11`, drop, verified): Imperial's release (27 Oct 2026) confirms a $40M seed co-led by Creandum and Union Square Ventures for a simulation-trained, one-demonstration robot foundation model. Drop reason confirmed: the coverage shows only general manipulation demos (packing, tidying, humanoids) and no lab-automation angle. — [Imperial news](https://www.imperial.ac.uk/news/articles/2026/imperial-ai-spinout-machenta-raises-40-million-to-make-robots-instant-learners/)

## Coverage

- Labautomation.io (community forum): site-search
- SLAS (Society for Laboratory Automation and Screening): site-search
- LRIG (Laboratory Robotics Interest Group) and chapters: site-search
- ELRIG (European Laboratory Research & Innovation Group): site-search
- Hamilton Company (Robotics / liquid handling): site-search
- Tecan (lab automation): site-search
- Agilent (automation & liquid handling only): site-search
- Beckman Coulter (Life Sciences automation + clinical lab automation): site-search
- Lab trade press: web-search

## Your feedback on this brief

> **Brief:** _/5 · **Missed:** _ · **Notes:** _ · `LAN-W20261031`

Rate 1-5 (5 = must-know). Tags are free text, comma-separated; the usual ones are `must-know`, `useful`, `meh`, `off-topic`, `wrong`, `unsound`, `hype`, `stale`, `dup`, `shallow`, `great`, `more`, `less`. **Missed** = anything you saw elsewhere that this brief should have had (a link or a few words); the next run follows it up.
