# Lab automation weekly, 9 Nov 2026

3 Nov – 9 Nov 2026 · 33 stories · 8 papers · 7 filtered out · 🎯 your field (DMPK/ADME) · ✅ verified · 🟡 partly verified · ⚪ unverified · ⏳ not yet checked · ⚠️ technical claim questionable · ⛔ technical claim unsupported

## TL;DR
- **Quiet week**: no new Tecan, Agilent or Beckman automation release found; Hamilton lists a Parallel Fluidics partnership, terms unseen ([Hamilton](https://www.hamiltoncompany.com/press-releases)).
- **PyLabRobot** keeps building simulation-first drivers (VANTAstar simulation, animated 3D visualizer) ([PR](https://github.com/PyLabRobot/pylabrobot/pull/1585)).

## Stories

### 1. 🎯 PyLabRobot covers microsomal-stability handling but not LC-MS/MS, TEER or Transwell labware
🟡⚠️ · other · PyLabRobot, QInstruments · 3 Nov

PLR has the pieces for liquid handling, 37 °C shaking (QInstruments BioShake Q1), plate moves, sealing and centrifugation, but no mass-spec or TEER driver and no Transwell resources at 7779f50. **Why:** A DMPK lab could script the wet steps in Python today, but the readout loop still needs other software.

Sources: [BioShake driver](https://github.com/PyLabRobot/pylabrobot/blob/7779f506d12755f5f274b4c5cab4d095f4fccb62/pylabrobot/qinstruments/bioshake.py#L20-L280) · [Repository tree](https://github.com/PyLabRobot/pylabrobot/tree/7779f506d12755f5f274b4c5cab4d095f4fccb62/pylabrobot) · [AZ DMPK panel paper](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7567642/)

> **Rate:** _/5 · **Tags:** _ · `LAN-20261102-15`

### 2. 🎯 OpenADMET releases open CYP data, reactivity read on Echo MS+
✅ · research · OpenADMET, Octant, SCIEX · 2 Mar

OpenADMET and Octant released CYP3A4/CYP2J2 reactivity and CYP3A4 inhibition data under CC BY 4.0; the reactivity readout ran on a SCIEX Echo MS+ with a ZenoTOF 7600. **Why:** Open, single-platform ADMET data generated on automated hardware for model training.

Sources: [OpenADMET Octant CYP repo](https://github.com/OpenADMET/Octant_CYP_blog_post)

> **Rate:** _/5 · **Tags:** _ · `LAN-20261102-32`

### 3. 🎯 Apheris launches a federated ADMET network with Lundbeck, Orion, Recursion and Servier
✅ · partnership · Apheris, Lundbeck, Orion · 25 Feb

Apheris launched an ADMET Network in which founding pharma and biotech members contribute about 80% of their relevant ADMET data to a federated foundation model without sharing it. **Why:** Automated assay data becomes shared AI training material without leaving each company.

Sources: [Apheris](https://www.apheris.com/resources/apheris-launches-admet-network) · [GEN](https://www.genengnews.com/topics/artificial-intelligence/admet-predictions-get-ai-boost-federated-data-network-unites-pharma/)

> **Rate:** _/5 · **Tags:** _ · `LAN-20261102-31`

### 4. 🎯 SCIEX Echo MS+ (2024) adds a ZenoTOF 8600 option in 2026
🟡⚠️ · product · SCIEX · 1 Feb

SCIEX launched Echo MS+ in Feb 2024 and added a ZenoTOF 8600 integration in Feb 2026; its ~10x metabolic-stability throughput claim comes from an Echo MS tech note, not peer review. **Why:** Vendor throughput claims remain unreviewed; independent ADME data is what to look for.

Sources: [SCIEX release](https://sciex.com/about-us/press-releases/2024/sciex-expands-high-throughput-screening-solutions-with-echo-ms-system) · [SCIEX tech note](https://sciex.com/tech-notes/pharma/discovery/10x-increased-throughput-for-metabolic-stability-assays)

> **Rate:** _/5 · **Tags:** _ · `LAN-20261102-26`

### 5. 🎯 CROs claim up to 500 compounds a week and sub-72-hour ADME turnaround
🟡⚠️ · market · Charles River, Cyprotex, Evotec · date unknown

CRO web pages claim: Charles River up to 500 compounds/week for primary HT-ADME assays; Cyprotex under 72 h on key assays for high-capacity contracts; WuXi over 300,000 in vitro studies a year. **Why:** Self-reported, mostly undated capacity claims that set expectations for outsourced ADME speed.

Sources: [Charles River HT-ADME](https://www.criver.com/products-services/lab-sciences/dmpk/high-throughput-adme-ht-adme) · [Cyprotex](https://www.evotec.com/solutions/drug-discovery-preclinical-development/cyprotex-adme-tox-solutions/about-cyprotex/working-with-cyprotex) · [WuXi DMPK](https://dmpkservice.wuxiapptec.com/about-wuxi-apptec-dmpk.html)

> **Rate:** _/5 · **Tags:** _ · `LAN-20261102-23`

### 6. 🎯 Evotec poster: Echo MS is fast but less sensitive than LC-MS/MS for HT-ADME
🟡 · research · Evotec, Cyprotex, SCIEX · date unknown

An Evotec poster on Echo MS for high-throughput ADME cites 2.5 nL droplets and the potential for 1 s cycle times, but lower sensitivity than LC-MS/MS and interference from having no separation. **Why:** A CRO's (not peer-reviewed) caution on acoustic-ejection MS for metabolic stability and CYP work.

Sources: [Evotec poster](https://www.evotec.com/sciencepool/echo-ms-in-high-throughput-adme)

> **Rate:** _/5 · **Tags:** _ · `LAN-20261102-27`

### 7. Over half of PyLabRobot's recent commits credit an AI coding assistant
🟡 · community · PyLabRobot, Anthropic, GitHub · 3 Nov

Since Nov 2025 PyLabRobot had 790 commits from 53 authors; 54% carry an AI co-author trailer, rising from 9% (Nov–Dec 2025) to 80% (Oct–Nov 2026). Two maintainers made 655 of them. **Why:** A clear public case of lab-automation code written largely with AI coding assistants, within strict written rules.

Sources: [PyLabRobot commit history (main)](https://github.com/PyLabRobot/pylabrobot/commits/main) · [AGENTS.md](https://github.com/PyLabRobot/pylabrobot/blob/7779f506d12755f5f274b4c5cab4d095f4fccb62/AGENTS.md)

> **Rate:** _/5 · **Tags:** _ · `LAN-20261102-06`

### 8. PyLabRobot ships no LLM or agent layer; AGENTS.md requires per-run hardware approval
✅ · other · PyLabRobot · 3 Nov

A search of PyLabRobot at 7779f50 finds no LLM, agent or MCP code. AGENTS.md tells coding agents: 'Never drive real hardware without explicit, per-run approval.' **Why:** Agents must be added around PLR, and the project's own rule sets the safety bar for them.

Sources: [AGENTS.md](https://github.com/PyLabRobot/pylabrobot/blob/7779f506d12755f5f274b4c5cab4d095f4fccb62/AGENTS.md) · [PreciseFlex error table](https://github.com/PyLabRobot/pylabrobot/blob/7779f506d12755f5f274b4c5cab4d095f4fccb62/pylabrobot/brooks/precise_flex/driver/errors.py) · [EventBus guide](https://github.com/PyLabRobot/pylabrobot/blob/7779f506d12755f5f274b4c5cab4d095f4fccb62/docs/contributor_guide/event-bus.md) · [+1 in Details](#details)

> **Rate:** _/5 · **Tags:** _ · `LAN-20261102-09`

### 9. No vendor-published SiLA 2 interface found for Hamilton, Biomek or Opentrons
🟡 · other · Hamilton, Beckman Coulter, Opentrons · 3 Nov

No Hamilton-, Beckman- or Opentrons-published SiLA 2 server was found (community Opentrons connectors exist). UniteLabs says it sells Hamilton STAR and VANTAGE connectors, but they are not in its public repositories. **Why:** A Hamilton lab wanting SiLA 2 needs a commercial integrator, a scheduler driver, or its own wrapper.

Sources: [UniteLabs liquid handling (vendor claim)](https://unitelabs.io/lab-automation-solutions/liquid-handling/) · [UniteLabs public GitLab group](https://gitlab.com/unitelabs)

> **Rate:** _/5 · **Tags:** _ · `LAN-20261103-10`

### 10. Third-party AI agents drive PyLabRobot only in simulation so far
✅ · community · PyLabRobot · 27 Oct

plr-mcp, OpenLabAI and labloop expose PyLabRobot to AI agents but default to chatterbox simulation, gate motion behind confirmation, and none reports driving a physical liquid handler. **Why:** The agent layer exists but is unproven on hardware; simulation-first plus human gates is the emerging norm.

Sources: [plr-mcp server.py](https://github.com/di-omics/plr-mcp/blob/db90c579439bdea0930be5f7dc0ac5fddb93b3b3/plr_mcp/server.py#L199-L206) · [OpenLabAI hamilton_server.py](https://github.com/nygmeta/OpenLabAI/blob/daade8e9f92e573362b20f9c46738b60db55cb6d/mcp_servers/hamilton_server.py) · [labloop plr_bridge.py](https://github.com/sl148/closed-loop-lab-demo/blob/86b27d6c66d54e57abd22e93fefa084d2dc20f15/src/labloop/execution/plr_bridge.py#L21-L65)

> **Rate:** _/5 · **Tags:** _ · `LAN-20261102-10`

### 11. Official SiLA 2 Python SDK marked unmaintained; users pointed to UniteLabs
✅ · standards · SiLA Consortium, UniteLabs · 17 Sep

The sila_python README was changed to 'Project Status: Unmaintained' on 17 Sep 2026, pointing to UniteLabs' unitelabs-sila; the last sila2 PyPI release is 0.14.0 (1 Dec 2025). **Why:** Python SiLA 2 work, including agent bridges built on sila2, now depends on a commercial company's open libraries.

Sources: [sila_python repository (README)](https://gitlab.com/SiLA2/sila_python) · [PyPI sila2](https://pypi.org/project/sila2/) · [PyPI unitelabs-sila](https://pypi.org/project/unitelabs-sila/)

> **Rate:** _/5 · **Tags:** _ · `LAN-20261103-05`

### 12. PyLabRobot moves its universal LiquidHandler to legacy and rewrites drivers per device
✅ · product · PyLabRobot, Hamilton · 1 Aug

PR #1000 (1 Aug 2026, 759 files) moved the front end/back end stack to pylabrobot.legacy. New v1 drivers are one plain class per device, and the guide calls the old split deprecated. **Why:** Trades one universal API for fidelity to each machine; protocols written for the old API still run but are now legacy.

Sources: [PR #1000 commit](https://github.com/PyLabRobot/pylabrobot/commit/14a776625) · [Device-driver guide](https://github.com/PyLabRobot/pylabrobot/blob/7779f506d12755f5f274b4c5cab4d095f4fccb62/docs/contributor_guide/device-driver-guide.md) · [v1 STAR Pipettes.aspirate](https://github.com/PyLabRobot/pylabrobot/blob/7779f506d12755f5f274b4c5cab4d095f4fccb62/pylabrobot/hamilton/star/driver/features/pipettes.py#L6101-L6140) · [+1 in Details](#details)

> **Rate:** _/5 · **Tags:** _ · `LAN-20261102-05`

### 13. SiLA feature library has no standard liquid-handling feature
✅ · standards · SiLA Consortium · 1 Jun

The SiLA feature library offers generic core features (SiLAService, Lock, Simulation, Cancel, Pause, ErrorRecovery) and labware-transfer features, but no standard aspirate/dispense, deck, labware or tip feature. **Why:** Each liquid-handler SiLA server defines its own commands, so clients are not portable across vendors.

Sources: [sila_base feature_definitions](https://gitlab.com/SiLA2/sila_base/-/tree/master/feature_definitions)

> **Rate:** _/5 · **Tags:** _ · `LAN-20261103-07`

### 14. Tecan's open-source FluentControl SiLA 2 connector (since 2020, updated Oct 2025)
🟡 · product · Tecan · 15 Jun

Tecan's fluent-sila2-connector (C#/.NET server plus Python client, BSD-3) exposes FluentControl over SiLA 2: start Fluent or simulation mode, run and pause methods, set variables, worklist-style pipetting. **Why:** The clearest case of a liquid-handler vendor shipping an open SiLA 2 interface.

Sources: [Tecan fluent-sila2-connector](https://gitlab.com/tecan/fluent-sila2-connector)

> **Rate:** _/5 · **Tags:** _ · `LAN-20261103-08`

### 15. PyLabRobot registry lists 84 devices, 50 on the new v1 API
✅ · product · PyLabRobot · 3 Nov

The device registry at 3 Nov 2026 has 84 entries: 50 v1, 26 v0 (legacy). The STAR's entry is still v0 'full'; Tecan EVO is v0 'basic'. The project started in Aug 2022. **Why:** Shows how far the v1 rewrite has reached, and which robots a lab can drive today.

Sources: [Device registry](https://github.com/PyLabRobot/pylabrobot/blob/7779f506d12755f5f274b4c5cab4d095f4fccb62/docs/_static/devices.json) · [Wierenga et al., Device 2023](https://www.cell.com/device/fulltext/S2666-9986(23)00170-9)

> **Rate:** _/5 · **Tags:** _ · `LAN-20261102-07`

### 16. OpentronsAI's open-source server now defaults to an Anthropic Claude model
✅ · product · Opentrons, Anthropic, OpenAI · 3 Nov

The OpentronsAI protocol assistant (launched Feb 2024) is open source; its settings default to claude-sonnet-5-5 with a legacy OpenAI path, and the model gets two tools: simulate_protocol and get_relevant_api_docs. **Why:** The most mature LLM-to-robot path checks protocols only by simulation, which catches errors in code, not science.

Sources: [OpentronsAI settings.py](https://github.com/Opentrons/opentrons/blob/631207155300fe9e96e08e4cfca48d11837fbd0c/opentrons-ai-server/api/settings.py#L32-L34) · [anthropic_predict.py tools](https://github.com/Opentrons/opentrons/blob/631207155300fe9e96e08e4cfca48d11837fbd0c/opentrons-ai-server/api/domain/anthropic_predict.py#L145-L160) · [Opentrons launch release, Feb 2024](https://www.businesswire.com/news/home/20240201923858/en/)

> **Rate:** _/5 · **Tags:** _ · `LAN-20261102-11`

### 17. Closed-loop optimisers hand experiments to robots through a simple ask/tell loop
✅ · research · Merck KGaA, Meta, Argonne · 3 Nov

BayBE, Ax, Atlas and MADSci all return the next conditions and accept results back; none ships a robot driver. CRESt's GPT front end requires three human confirmations before posting recipes to an OT-2. **Why:** PyLabRobot is the kind of glue these optimisers assume you write yourself.

Sources: [BayBE campaign.py](https://github.com/emdgroup/baybe/blob/ed54e0092acd0dc07b2a920ef4b58198f608bfa1/baybe/campaign.py#L495) · [Ax README](https://github.com/facebook/Ax/blob/5a7b3367f2d372e1653fd6c6ff1eaf8069ecc850/README.md) · [MADSci example](https://github.com/AD-SDL/MADSci/blob/bbfcba5efcaeacb750252a921256de5d61d51bb2/examples/example_experiment.py#L105) · [+1 in Details](#details)

> **Rate:** _/5 · **Tags:** _ · `LAN-20261102-12`

### 18. PyLabRobot uses SiLA only to reach devices that already have a SiLA server
✅ · other · PyLabRobot, Molecular Devices, INHECO · 3 Nov

PyLabRobot discovers SiLA 1 and SiLA 2 devices, talks raw gRPC to Molecular Devices' ImageXpress Pico and SiLA 1 SOAP to INHECO devices, but drives liquid handlers through firmware, not SiLA. **Why:** PLR control and a thin SiLA 2 server on top can be combined, as in this folder's POC.

Sources: [PLR SiLA discovery](https://github.com/PyLabRobot/pylabrobot/blob/7779f506d12755f5f274b4c5cab4d095f4fccb62/pylabrobot/io/sila/discovery.py) · [PLR SiLA gRPC helpers](https://github.com/PyLabRobot/pylabrobot/blob/7779f506d12755f5f274b4c5cab4d095f4fccb62/pylabrobot/io/sila/grpc.py)

> **Rate:** _/5 · **Tags:** _ · `LAN-20261103-13`

### 19. PyLabRobot's PreciseFlex driver adds force-sensed Z probing and collision guards
✅ · community · PyLabRobot, Brooks Automation · 2 Nov

Between 29 Oct and 2 Nov PyLabRobot added a PF400 simulator, refusal of moves into the arm's column or base plate, force-limited gripping, Z-touch probing (15 N default) and safe setup failure. **Why:** Force and vision sensing callable from Python are the raw inputs for closed-loop workcells.

Sources: [probe_z_using_ztouch](https://github.com/PyLabRobot/pylabrobot/blob/7779f506d12755f5f274b4c5cab4d095f4fccb62/pylabrobot/brooks/precise_flex/driver/features/arm.py#L2422-L2470) · [PR #1577](https://github.com/PyLabRobot/pylabrobot/pull/1577)

> **Rate:** _/5 · **Tags:** _ · `LAN-20261102-08`

### 20. Orca 2.3.0 adds simulation time-scaling and audit reasons for scheduler actions
✅ · community · Cheshire Labs · 19 Oct

Orca 2.3.0 lets simulated runs be paced faster than real time and writes ten more operator actions to an audit log, with an optional reason. Labware barcodes must now be unique. **Why:** Audit rows and barcode checks are the kind of traceability a regulated ADME lab needs from any scheduler; Orca is still early-stage.

Sources: [Orca v2.3.0 release notes](https://github.com/Cheshire-Labs/orca/releases/tag/v2.3.0)

> **Rate:** _/5 · **Tags:** _ · `LAN-20261104-02`

### 21. Roche says it has started building autonomous AI labs
🟡 · market · Roche · 28 Sep

At its 28 September 2026 Pharma Day, Roche outlined a move to autonomous AI labs and said building has begun, without claiming a deployed autonomous lab. **Why:** Another big pharma committing to lab autonomy; assay specifics, including ADME, were not given.

Sources: [Global Banking & Finance coverage](https://www.globalbankingandfinance.com/roche-outlines-plans-move-towards-autonomous-ai-labs/)

> **Rate:** _/5 · **Tags:** _ · `LAN-20261102-20`

### 22. labmcp-sila2 lets AI agents call SiLA 2 servers, tested only in simulation
✅ · community · K-Dense · 26 Sep

K-Dense's labmcp-sila2 MCP server reads a SiLA feature definition, validates parameters and tracks observable commands; it is self-described as 'simulated', tested against an in-process sila2 server. **Why:** Agent access to SiLA devices exists, but is unproven on vendor servers and built on the unmaintained SDK.

Sources: [labmcp-sila2 README](https://github.com/K-Dense-AI/lab-instrument-mcps/tree/46545ea7eb818249a524c3340dc80657f448430f/servers/protocols/sila2)

> **Rate:** _/5 · **Tags:** _ · `LAN-20261103-14`

### 23. Orca lab scheduler 2.0 adds daemon and REST API, relicenses to SSPL
✅ · community · Cheshire Labs · 23 Sep

Cheshire Labs' Orca, a Python scheduler for lab workflows, moved to a persistent local daemon with REST/SSE interface and CLI in v2.0.0. The same release relicensed it from AGPL-3.0 to the Server Side Public License. **Why:** Open schedulers are maturing, but SSPL is not OSI-approved open source, so pharma legal teams may treat it differently.

Sources: [Orca v2.0.0 pull request](https://github.com/Cheshire-Labs/orca/pull/14)

> **Rate:** _/5 · **Tags:** _ · `LAN-20261104-01`

### 24. Court blocks WuXi AppTec's Pentagon 1260H listing; BIOSECURE now law
✅ · market · WuXi AppTec · 7 Aug

The BIOSECURE Act was enacted on 18 Dec 2025 without naming WuXi; WuXi AppTec was added to the DoD 1260H list on 8 Jun 2026 and a federal court enjoined that designation on 7 Aug 2026. **Why:** Outsourcing ADME screening to China-based CROs now carries policy risk for US sponsors.

Sources: [Ropes & Gray: BIOSECURE enacted](https://www.ropesgray.com/en/insights/alerts/2026/01/biosecure-act-enacted) · [Ropes & Gray: court enjoins 1260H designation](https://www.ropesgray.com/en/insights/alerts/2026/08/federal-court-enjoins-dod-designation-of-wuxi-apptec-as-a-chinese-military-company-under-section)

> **Rate:** _/5 · **Tags:** _ · `LAN-20261102-24`

### 25. OpenAI and Ginkgo: GPT-5-designed experiments cut cell-free protein cost 40%
✅ · research · OpenAI, Ginkgo Bioworks · 5 Feb

OpenAI and Ginkgo report GPT-5 designing about 36,000 cell-free protein-synthesis reactions on Ginkgo's automation, with schema checks before execution and humans preparing reagents; cost per gram fell about 40%. **Why:** A large public LLM-designed experiment campaign on lab automation, with strict validation before anything runs.

Sources: [OpenAI announcement](https://openai.com/index/gpt-5-lowers-protein-synthesis-cost/)

> **Rate:** _/5 · **Tags:** _ · `LAN-20261102-13`

### 26. Labman builds a robotic design-make-test-analyse lab for an unnamed big pharma
🟡 · partnership · Labman · 7 Jan

Labman is building a robotic design-make-test-analyse platform with mobile robots for an unnamed global pharma, over two years from January 2025 (company announcement). **Why:** Integrators, not just vendors, are building end-to-end discovery automation for pharma.

Sources: [Labman news](https://live.labmanautomation.com/news/DMTA-drug-discovery-lab)

> **Rate:** _/5 · **Tags:** _ · `LAN-20261102-28`

### 27. Dispendix I.DOT ships a native SiLA 2 server
🟡 · product · Dispendix · 14 Sep

Dispendix's I.DOT non-contact dispenser runs a SiLA 2 server on the instrument (client-initiated connections, mDNS discovery); the vendor publishes C# client samples. **Why:** One of few dispensers with vendor-native SiLA 2.

Sources: [Dispendix I.DOT SiLA 2 samples](https://github.com/Dispendix/dx-idot-sila2-samples)

> **Rate:** _/5 · **Tags:** _ · `LAN-20261103-09`

### 28. PyLabRobot week: STAR/Prep probing offsets, VANTAstar simulation, animated 3D visualizer
🟡 · community · PyLabRobot, Hamilton, BMG Labtech · 9 Nov

PyLabRobot merged PRs since 2 Nov: STAR and Prep pipettes get probe offsets and renamed offsets/jets arguments, the VANTAstar reader gains simulation, and the 3D visualizer animates joint moves. **Why:** Simulation-first drivers let scripts, and any AI-written ones, be tested before touching hardware; a recurring pattern in this repo.

Sources: [PR #1592 offsets and jets](https://github.com/PyLabRobot/pylabrobot/pull/1592) · [PR #1593 blow-out mode](https://github.com/PyLabRobot/pylabrobot/pull/1593) · [PR #1585 VANTAstar simulation](https://github.com/PyLabRobot/pylabrobot/pull/1585) · [+2 in Details](#details)

> **Rate:** _/5 · **Tags:** _ · `LAN-20261109-02`

### 29. Hamilton and Parallel Fluidics partner to automate advanced workflows on liquid handlers
🟡 · partnership · Hamilton, Parallel Fluidics · 5 Nov

Hamilton's press-release page lists a partnership with Parallel Fluidics, a Boston microfluidic-consumables maker, to automate advanced lab workflows on Hamilton liquid handlers. Only the headline was retrievable; terms are not visible. **Why:** Consumable-level integrations widen what a standard liquid handler can run; terms unseen, and LNP work is more biologics than core ADME.

Sources: [Hamilton press releases](https://www.hamiltoncompany.com/press-releases) · [Parallel Fluidics LNP Screening Array](https://www.parallelfluidics.com/lnp-screening-array/starter-kit)

> **Rate:** _/5 · **Tags:** _ · `LAN-20261109-01`

### 30. SiLA Rust 0.1.0 published to crates.io
✅ · standards · SiLA Consortium · 3 Nov

The SiLA consortium's Rust implementation published version 0.1.0 to crates.io on 3 Nov 2026 and reports full interop with the Python test client and server. **Why:** A new, maintained SiLA 2 implementation language for device builders.

Sources: [sila_rust repository](https://gitlab.com/SiLA2/sila_rust)

> **Rate:** _/5 · **Tags:** _ · `LAN-20261103-11`

### 31. OPC Foundation merges LADS 1.0.0 packages into its .NET SDK
✅ · standards · OPC Foundation · 1 Nov

OPC Foundation's UA-.NETStandard pull request #4945 added LADS 1.0.0 model, server and client packages with a shaking-incubator sample, merged 1 Nov 2026. **Why:** The rival open device standard gets an official SDK; liquid-handler support is still absent.

Sources: [UA-.NETStandard PR #4945](https://github.com/OPCFoundation/UA-.NETStandard/pull/4945)

> **Rate:** _/5 · **Tags:** _ · `LAN-20261103-12`

### 32. SiLA 2 base repository tags release v1.2
✅ · standards · SiLA Consortium · 5 Feb

The sila_base repository carries a v1.2 'Official Release 1.2' tag dated 5 Feb 2026, after v1.0 (Oct 2019) and v1.1 (Mar 2022); no separate v1.2 specification announcement was found. **Why:** Incremental standard; the published Part A/B documents may still read v1.1.

Sources: [sila_base repository (tags)](https://gitlab.com/SiLA2/sila_base)

> **Rate:** _/5 · **Tags:** _ · `LAN-20261103-06`

### 33. BioIVT acquires BeCytes Biotechnologies to expand NAMs and ADME
🟡 · acquisition · BioIVT, BeCytes · 28 Oct

BioIVT bought Barcelona-based BeCytes Biotechnologies, a tissue and cell supplier, framing the deal as strengthening new approach methodologies and ADME studies. **Why:** Consolidation in the cell and tissue supply that in vitro ADME assays depend on.

Sources: [Biotech Spain](https://biotech-spain.com/en/articles/bioivt-acquires-becytes-biotechnologies-to-boost-preclinical-research-in-europe/)

> **Rate:** _/5 · **Tags:** _ · `LAN-20261102-25`

## From the journals

SLAS Discovery, SLAS Technology, HardwareX, PubMed and preprints; your field first.

### P1. 🎯 BMS automates 96-well Caco-2 permeability, matching 24-well classification for 94%
*ASSAY Drug Dev Technol* · Cai X. et al. · 26 Dec · ✅

Bristol Myers Squibb moved Caco-2 from 24- to 96-well on an integrated platform covering cell culture and assay, with plate tracking and dynamic scheduling; 94% of 50 reference compounds classified concordantly. **Why:** The newest pharma ADME-automation paper, built to feed predict-first design; no throughput figure given.

[PubMed 41468180](https://pubmed.ncbi.nlm.nih.gov/41468180/)

> **Rate:** _/5 · **Tags:** _ · `LAN-20261102-16`

### P2. 🎯 WuXi reads flux-dialysis protein binding by acoustic-ejection MS, ~25x faster
*Drug Metab Dispos* · Wen X. et al. · 10 Nov · ✅

WuXi AppTec paired flux-dialysis plasma protein binding with acoustic-ejection MS readout; unbound fractions agreed with LC-MS/MS (R² > 0.96) with about 25-fold faster analysis. **Why:** Puts AEMS into a peer-reviewed ADME workflow, the readout step most likely to change next.

[PubMed 41386030](https://pubmed.ncbi.nlm.nih.gov/41386030/)

> **Rate:** _/5 · **Tags:** _ · `LAN-20261102-17`

### P3. 🎯 Genentech combines hepatocyte stability and metabolite profiling in one automated assay
*Drug Metab Dispos* · Leung C. et al. · 4 Mar · 🟡

A Genentech DMD paper integrates hepatocyte metabolic stability with metabolite profiling using automation and high-resolution MS, covering three species in about 4.5 hours (30 min preparation plus 4 h). **Why:** Shows automation merging two DMPK readouts, cutting a separate MetID step.

[PubMed 38438166](https://pubmed.ncbi.nlm.nih.gov/38438166/)

> **Rate:** _/5 · **Tags:** _ · `LAN-20261102-19`

### P4. 🎯 AstraZeneca's Wave 1: five DMPK assays on three Hamilton STARplus robots, weekly
*ASSAY Drug Dev Technol* · Wernevik J. et al. · 14 May · ✅

AstraZeneca's Wave 1 panel runs HLM and rat hepatocyte CLint, PPB, solubility and logD7.4 weekly on all newly synthesised compounds, using three identically configured Hamilton STARplus robots. **Why:** Still the best-documented in-house ADME platform; no big pharma has published newer throughput figures.

[PMC7567642](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7567642/)

> **Rate:** _/5 · **Tags:** _ · `LAN-20261102-18`

### P5. 🎯 End-to-end automated platform screens solubility and logD with 20x less material
*AAPS Open* · 27 Aug · ✅⚠️

An AAPS Open paper describes an end-to-end automated high-throughput platform with analytics software for solubility, logD and amorphous dispersion screening, reporting over 10x efficiency and 20x less material. **Why:** Physicochemical ADME screening gets end-to-end automation; the 10x has no stated baseline.

[AAPS Open](https://link.springer.com/article/10.1186/s41120-026-00192-0)

> **Rate:** _/5 · **Tags:** _ · `LAN-20261102-29`

### P6. 🎯 Merck's Juncai Meng presents acoustic-ejection MS uses in discovery at Pittcon 2026
2026-02 · 🟡⚠️

A Pittcon 2026 talk by Juncai Meng (Merck) covered applying acoustic-ejection MS in discovery, including QC, peptide conformation and solubility; a 2026 review by Meng et al. covers AEMS including ADME profiling. **Why:** Shows AEMS spreading inside pharma discovery; metabolic-stability use was not described.

[Pittcon 2026 abstract](https://labscievents.pittcon.org/event/pittcon-2026/planning/UGxhbm5pbmdfNDI4ODM1MQ==) · [Meng et al., Analysis & Sensing](https://chemistry-europe.onlinelibrary.wiley.com/doi/abs/10.1002/anse.202500218)

> **Rate:** _/5 · **Tags:** _ · `LAN-20261102-21`

### P7. 🎯 Mdr1-knockout MDCK cells estimate human intestinal permeability
*Mol Pharm* · Beran K. et al. · 7 Sep · ✅

A Mol Pharm paper reports canine Mdr1-knockout MDCK cells reliably estimating human jejunal permeability and fraction absorbed, with 3–7 days of culture versus 14–28 for Caco-2. **Why:** Faster-growing cell models suit automated, high-throughput permeability screening.

[Mol Pharm 22(10):6067](https://pubs.acs.org/mpohbp/article/22/10/6067/3749648/)

> **Rate:** _/5 · **Tags:** _ · `LAN-20261102-30`

### P8. LabSafety Bench: no AI model above 70% on lab hazard identification
14 Jan · 🟡

LabSafety Bench tested 19 language and vision-language models on laboratory safety; none scored above 70% on hazard identification. **Why:** A reason to keep humans and hard interlocks between an agent and moving hardware.

[LabSafety Bench, Nat Mach Intell](https://www.nature.com/articles/s42256-025-01152-1) · [arXiv 2410.14182](https://arxiv.org/abs/2410.14182)

> **Rate:** _/5 · **Tags:** _ · `LAN-20261102-14`

## Signals to watch (analysis)
- **Blind spot**: vendor sites and journal feeds were blocked again, so a quiet week may be partly search coverage ([run log](https://github.com/bum94587/LabAutoNews)).

## Filtered out

Found but not shown as stories:

- **Novartis validates a robotic high-throughput equilibrium solubility assay on 85 compounds** (drop, facts contradicted): contradicted: merged two papers (ARIA robot in ACS Omega 2024, not shown as Novartis; Novartis shake-flask in J Pharm Sci 2007) [ACS Omega 2024](https://pubs.acs.org/doi/full/10.1021/acsomega.4c02003)
- **ISSX 2025 poster: automated 96-well metabolic stability matches 24-well** (hold, facts verified): Search snippets of the ISSX 2025 abstract book (14th ISSX meeting, 21-24 Sep 2025) confirm poster P9: hepatocyte stability in 96-well on automated workstations, compared… [ISSX 2025 abstracts](https://cdn.ymaws.com/www.issx.org/resource/resmgr/meetings_-_general/2025/ISSX_2025_Complete_Abstract_.pdf)
- **SLAS Technology paper applies acoustic ejection MS to covalent BTK inhibitor screening** (hold, facts verified): Search snippet of the DOAJ record confirms title, SLAS Technology Aug 2025 (vol 33, 100307, DOI 10.1016/j.slast.2025.100307), BTK pipeline (screening, GSH reactivity, kinact/Ki) on Echo… [DOAJ record, SLAS Technology (Aug 2025)](https://doaj.org/article/07194c6df2a2440497f6c7b117155dcc)
- **Hu and Blair: acoustic ejection MS analyses reactions without chromatography (Nature)** (hold, facts partial): Nature 636:374-379, Dec 2024, DOI, St. [Continuous collective analysis of chemical reactions, Nature](https://doi.org/10.1038/s41586-024-08211-4)
- **Pittcon 2026 talk: acoustic ejection MS used by Merck for small-molecule discovery** (hold, facts partial): Pittcon listing 'Application of Acoustic Ejection MS to Accelerate Small Molecules Discovery Process', Sun 8 Mar 2026 9:10-9:30, and the ADE/OPI/ESI-MS description confirmed via search… [Pittcon 2026 session listing](https://labscievents.pittcon.org/event/pittcon-2026/planning/UGxhbm5pbmdfNDI4ODM1MQ==)
- **SCIEX claims Echo MS cuts metabolic-stability analysis time about 10x versus LC-MS/MS** (hold, facts partial): Published date 2026-11-03 is a placeholder (SCIEX tech notes are undated); real date unknown. [SCIEX tech note: up to 10x metabolic stability](https://sciex.com/tech-notes/pharma/discovery/10x-increased-throughput-for-metabolic-stability-assays)
- **PyLabRobot merges work-in-progress Kingfisher magnetic-particle processor support** (hold, facts verified): PR #1570 'Kingfisher Support (WIP Primarily Presto)' shown merged 3 Nov 2026 by rickwierenga, adding a Presto device API. [PyLabRobot PR 1570](https://github.com/PyLabRobot/pylabrobot/pull/1570)

Screened out during research:

- [Beckman Echo 650 Plus Series](https://www.beckman.com/news/echo-650-plus-series-acoustic-liquid-handlers) [beckman]: published 13 May 2026, outside window
- [Beckman and Automata partnership](https://www.beckman.com/news) [beckman]: January 2026, outside window
- [Tecan agentic AI in Introspect with NVIDIA](https://www.tecan.com/customer-news/tecan-accelerates-data-driven-lab-journey-with-agentic-ai-developments-powered-by-nvidia-2412) [tecan]: June 2026, outside window
- [Hamilton nRichDX partnership](https://www.hamiltoncompany.com/press-releases/strategic-partnership-between-nrichdx-and-hamilton) [hamilton]: January 2026, outside window
- [Is the autonomous lab finally achievable? MCP, MHS](https://www.drugdiscoverynews.com/is-the-autonomous-lab-finally-achievable-17574) [web]: about 2 weeks old, outside 7-day window; page not fetchable; Anthropic MHS claim unverified
- [Robotic safety in self-driving laboratories (SLAS Technology)](https://www.sciencedirect.com/science/article/pii/S2472630326000774) [slas-technology]: online date unconfirmed, page not fetchable
- [Biotech instrumentation / pharma robots market reports](https://globenewswire.com/news-release/2026/11/02/3393460/28124/en/) [wires]: market-research ad, not lab automation news
- [Lab Innovations 2026 speaker lineup](https://www.selectscience.net/article/lab-innovations-2026-reveals-its-speaker-lineup) [trade-press]: generic UK trade show, 4-5 Nov, low relevance
- [Atinary Boston Self-Driving Labs](https://www.selectscience.net/article/atinary-launches-self-driving-labs-r-in-boston-bringing-ai-into-the-physical-world-of-r-and-d) [trade-press]: old/conflicting dates
- [Veon Scientific i.prep 2 teaser](https://www.linkedin.com/) [linkedin]: about 100 days old, teaser only
- [Meng 2026 AEMS review (Analysis & Sensing)](https://chemistry-europe.onlinelibrary.wiley.com/doi/abs/10.1002/anse.202500218) [web]: could not confirm paper on re-search; omitted
- [Nature Protocols Hu & Blair 2026](https://www.nature.com/articles/s41596-025-01320-y) [web]: author attribution not confirmed; Hu and Blair work is Nature 2024
- [Hamilton and Ahlstrom automated DBS processing](https://www.hamiltoncompany.com/press-releases) [hamilton]: 9 Oct, outside window
- [Tecan agentic AI with NVIDIA](https://www.tecan.com/news-archive) [tecan]: May/June, outside window
- [Shimadzu and ePrep sample prep partnership](https://www.selectscience.net/technique/automated-liquid-handling) [trade-press]: August, outside window
- [Latent-Y antibody design agent](https://www.businesswire.com/news/home/20260323538522/en/Latent-Y-The-Autonomous-AI-Agent-for-Drug-Design-at-Scale) [wires]: March, outside window
- [Caco-2 96-well platform (Cai et al.)](https://doi.org/10.1177/1540658x251408742) [pubmed]: duplicate of LAN-20261102-16
- [Hamilton Duo Syringe Pump launch](https://macaubusiness.com/hamilton-launches-the-duo-syringe-pump-for-flexible-precise-liquid-delivery-in-research-applications/) [hamilton]: 27 Oct, outside 7-day window; OEM pump
- [Ahlstrom and Hamilton automated DBS sample processing](https://www.hamiltoncompany.com/press-releases) [hamilton]: 9 Oct, outside window
- [Tecan Q3 update (5 Nov)](https://www.tecan.com/corporate-news) [tecan]: financial update, not found, not automation
- [SLAS Innovation Award finalists](https://www.slas.org/events-calendar/slas2026-international-conference-exhibition/present/innovation-award/) [slas]: announcement not found yet
- [Passive AI system verifying deck state on liquid handlers (arXiv 2610.02668)](https://arxiv.org/html/2610.02668v1) [web]: early Oct, outside 14-day window
- [Caco-2 96-well automation (ADDT)](https://pubmed.ncbi.nlm.nih.gov/41468180/) [pubmed]: already covered LAN-20261102-16
- [GPT-enhanced robotic automation platform (SLAS Technol)](https://pubmed.ncbi.nlm.nih.gov/42002231/) [slas-technology]: publication date unclear, not DMPK; unconfirmed in window
- [Ginkgo ADME-One with Tangible and Inductive Bio](https://www.drugdiscoverytrends.com/ginkgo-tangible-and-inductive-bio-aim-to-move-adme-decisions-from-lead-optimization-to-hit-id/) [web]: June 2026, outside window
- [Beckman Biomek i3](https://www.beckman.com/news/biomek-i3-benchtop-liquid-handler) [beckman]: Dec 2025, old
- [Agilent OmixAI partnership](https://www.agilent.com/about/newsroom/presrel/2026/14apr-ca26012.html) [agilent]: April, old
- [Protein Sciences in Drug Discovery, 10-11 Nov](https://elrig.org/elrig-unveils-keynote-speakers-for-protein-sciences-2026/) [elrig]: event listing, protein science not automation

## Scope: sites and companies

What each site and company produced in this window. To add or remove one, fill in the **Scope** line at the very bottom; the next run applies it to `config/`.

| Site | Tier | Cadence | Checked via | Candidates | Stories |
|---|---|---|---|---:|---:|
| [Labautomation.io (community forum)](https://labautomation.io) | core | daily | site-search | 0 | 0 |
| [PyLabRobot (open-source lab automation library)](https://github.com/PyLabRobot/pylabrobot) | core | daily | feed, feed+site-search | 9 | 7 |
| [SLAS (Society for Laboratory Automation and Screening)](https://www.slas.org/news-highlights/news-center/) | core | daily | site-search | 4 | 0 |
| [LRIG (Laboratory Robotics Interest Group) and chapters](https://www.lrig.org) | core | daily | site-search | 0 | 0 |
| [ELRIG (European Laboratory Research & Innovation Group)](https://www.elrig.org) | core | daily | site-search | 1 | 0 |
| [Hamilton Company (Robotics / liquid handling)](https://www.hamiltoncompany.com/automated-liquid-handling) | core | daily | site-search | 4 | 1 |
| [Tecan (lab automation)](https://www.tecan.com/news-archive) | core | daily | site-search | 2 | 0 |
| [Agilent (automation & liquid handling only)](https://www.agilent.com/en/product/automated-liquid-handling) | core | daily | site-search | 0 | 0 |
| [Beckman Coulter (Life Sciences automation + clinical lab automation)](https://www.beckman.com/news) | core | daily | site-search | 2 | 0 |
| [SLAS Discovery (journal)](https://www.sciencedirect.com/journal/slas-discovery) | core | weekly | site-search | 0 | 0 |
| [SLAS Technology (journal)](https://www.sciencedirect.com/journal/slas-technology) | core | weekly | site-search | 1 | 0 |
| [HardwareX (journal, open hardware)](https://www.sciencedirect.com/journal/hardwarex) | core | weekly | site-search | 0 | 0 |
| [PubMed (DMPK/ADME automation first, then pharma/biotech lab automation)](https://pubmed.ncbi.nlm.nih.gov/) | core | weekly | site-search | 3 | 4 |
| Lab trade press | secondary | daily | site-search | 0 | 0 |
| [LinkedIn (posts and articles, via search only)](https://www.linkedin.com/feed/hashtag/labautomation/) | secondary | daily | **not checked** | 0 | 0 |
| Press-release wires | secondary | daily | site-search | 0 | 0 |
| Preprints and other journals | secondary | weekly | **not checked** | 0 | 3 |
| Open web search (not a listed site) | — | daily | web-search | — | 26 |

**Companies watched** (stories this window):

- Core vendors: Hamilton 5 · Tecan 1 · Agilent 0 · Beckman Coulter 1
- Incumbents: Thermo Fisher 0 · Revvity 0 · Molecular Devices 1 · Eppendorf 0 · Sartorius 0 · Roche Diagnostics 0 · Siemens Healthineers 0 · Abbott 0 · Waters 0 · SPT Labtech 0 · Formulatrix 0 · Analytik Jena 0 · Gilson 0 · INTEGRA Biosciences 0
- Open source: PyLabRobot 9
- Growth: Opentrons 2 · Automata 0 · Biosero 0 · HighRes Biosolutions 0 · Synthace 0 · Benchling 0 · Emerald Cloud Lab 0 · Ginkgo Bioworks 1 · Cellares 0 · Retisoft 0 · Unchained Labs 0
- AI-native: Lila Sciences 0 · Periodic Labs 0 · Chemify 0 · Radical AI 0 · Medra 0 · Trilobio 0 · FutureHouse 0 · Arctoris 0 · Recursion 1

**In the news, not on the watchlist** (add?): Anthropic · Apheris · Argonne · AstraZeneca · BMG Labtech · BeCytes · BioIVT · Bristol Myers Squibb · Brooks Automation · Charles River · Cheshire Labs · Cyprotex · Dispendix · Evotec · Genentech · GitHub · INHECO · K-Dense · Labman · Lundbeck · MIT · Merck · Merck KGaA · Meta · OPC Foundation · Octant · OpenADMET · OpenAI · Orion · Parallel Fluidics · QInstruments · Roche · SCIEX · Servier · SiLA Consortium · St. Jude · UniteLabs · WuXi AppTec

## Details <a id="details"></a>

**1. PyLabRobot covers microsomal-stability handling but not LC-MS/MS, TEER or Transwell labware** (`LAN-20261102-15`, dmpk-adme, published 2026-11-03)
- BioShake API: set_temperature, start_shaking; BioShakeQ1 is the implemented heated model (BioShake3000T raises NotImplementedError) [[1]](https://github.com/PyLabRobot/pylabrobot/blob/7779f506d12755f5f274b4c5cab4d095f4fccb62/pylabrobot/qinstruments/bioshake.py#L20-L280)
- No LC-MS, TEER or Transwell modules or resources found in pylabrobot/ [[2]](https://github.com/PyLabRobot/pylabrobot/tree/7779f506d12755f5f274b4c5cab4d095f4fccb62/pylabrobot)
- AZ automates HLM/hepatocyte CLint on Hamilton STARplus robots [[3]](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7567642/)
- Verifier: facts partial, science questionable. BioShake start_shaking/set_temperature exist, and there is no LC-MS, TEER or Transwell support at 7779f50; the AZ STARplus panel is confirmed in snippets. Only the Q1 is an implemented, 'full' heated BioShake, though: the article's BioShake3000T is 'wip' and raises NotImplementedError, and the sketch would also raise TooLittleLiquidError because volume tracking is on with no starting volumes.
- Sources: [1] [BioShake driver](https://github.com/PyLabRobot/pylabrobot/blob/7779f506d12755f5f274b4c5cab4d095f4fccb62/pylabrobot/qinstruments/bioshake.py#L20-L280) (primary) · [2] [Repository tree](https://github.com/PyLabRobot/pylabrobot/tree/7779f506d12755f5f274b4c5cab4d095f4fccb62/pylabrobot) (primary) · [3] [AZ DMPK panel paper](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7567642/) (paper)

**2. OpenADMET releases open CYP data, reactivity read on Echo MS+** (`LAN-20261102-32`, dmpk-adme, published 2026-03-02)
- Verifier: facts verified, science sound. Repo opened directly: the blog post 'Building the OpenADMET Data Engine' (Warneford-Thomson, Simpkins, Edgar, MacDermott-Opeskin) is dated 2 Mar 2026. It covers about 1,200 compounds with CYP3A4/CYP2J2 reactivity read on SCIEX Echo MS+ ZenoTOF 7600, plus CYP3A4 inhibition (fluorescence, incl. TDI). Data CC BY 4.0, code Apache-2.0, Zenodo 10.5281/zenodo.21504217. Primary open data; 'single-platform consistency' is the consortium's own framing.
- Sources: [1] [OpenADMET Octant CYP repo](https://github.com/OpenADMET/Octant_CYP_blog_post) (primary)

**3. Apheris launches a federated ADMET network with Lundbeck, Orion, Recursion and Servier** (`LAN-20261102-31`, dmpk-adme, published 2026-02-25)
- Verifier: facts verified, science na. From search snippets: Apheris' release (Berlin, 25 Feb 2026) names Lundbeck, Orion Pharma, Recursion and Servier among the founding members. GEN reports five founders (one undisclosed) committing about 80% of relevant ADMET data, and an Apheris post repeats the 80%. The title's four names are not the full membership.
- Sources: [1] [Apheris](https://www.apheris.com/resources/apheris-launches-admet-network) (primary) · [2] [GEN](https://www.genengnews.com/topics/artificial-intelligence/admet-predictions-get-ai-boost-federated-data-network-unites-pharma/) (secondary)

**4. SCIEX Echo MS+ (2024) adds a ZenoTOF 8600 option in 2026** (`LAN-20261102-26`, dmpk-adme, published 2024-02-01)
- Echo MS+ launched at SLAS, Feb 2024 [[1]](https://sciex.com/about-us/press-releases/2024/sciex-expands-high-throughput-screening-solutions-with-echo-ms-system)
- ~10x throughput for metabolic stability (Echo MS vendor tech note) [[2]](https://sciex.com/tech-notes/pharma/discovery/10x-increased-throughput-for-metabolic-stability-assays)
- Verifier: facts partial, science questionable. The Echo MS+ launch (ZenoTOF 7600 or Triple Quad 6500+) at SLAS 2024 is confirmed: SCIEX page dated 1 Feb 2024, Business Wire 2 Feb. But the '10x for metabolic stability' tech note is for the Echo MS system (vendor-run, RUO), not specifically Echo MS+. 'No newer ADME-relevant hardware' misses the 9 Feb 2026 Echo MS+ + ZenoTOF 8600 integration, sold on higher sensitivity. Vendor-only evidence.
- Sources: [1] [SCIEX release](https://sciex.com/about-us/press-releases/2024/sciex-expands-high-throughput-screening-solutions-with-echo-ms-system) (primary) · [2] [SCIEX tech note](https://sciex.com/tech-notes/pharma/discovery/10x-increased-throughput-for-metabolic-stability-assays) (primary)

**5. CROs claim up to 500 compounds a week and sub-72-hour ADME turnaround** (`LAN-20261102-23`, dmpk-adme, published )
- Charles River: up to 500 compounds/week (Hamilton and ≤5-day turnaround per an older CRL article) [[1]](https://www.criver.com/products-services/lab-sciences/dmpk/high-throughput-adme-ht-adme)
- Cyprotex: <72 h on key assays for high-capacity contracts [[2]](https://www.evotec.com/solutions/drug-discovery-preclinical-development/cyprotex-adme-tox-solutions/about-cyprotex/working-with-cyprotex)
- WuXi: 300k+ in vitro studies per year [[3]](https://dmpkservice.wuxiapptec.com/about-wuxi-apptec-dmpk.html)
- Verifier: facts partial, science questionable. Self-reported, from snippets: Charles River up to 500 compounds/week is on its HT-ADME page, but Hamilton and <=5-day turnaround come from an old (about 2019) CR insight article. Cyprotex <72 h applies to regular high-capacity contracts only (standard is 3-5 days). WuXi 200k+ samples/week is on its 'Why choose' page, not the cited About page (a test page says 180k+). Medicilon 240/day is not confirmed: the only match is a mirror post where 240/day is a spectral-gradient-analysis method's throughput, not Medicilon capacity.
- Sources: [1] [Charles River HT-ADME](https://www.criver.com/products-services/lab-sciences/dmpk/high-throughput-adme-ht-adme) (primary) · [2] [Cyprotex](https://www.evotec.com/solutions/drug-discovery-preclinical-development/cyprotex-adme-tox-solutions/about-cyprotex/working-with-cyprotex) (primary) · [3] [WuXi DMPK](https://dmpkservice.wuxiapptec.com/about-wuxi-apptec-dmpk.html) (primary)

**6. Evotec poster: Echo MS is fast but less sensitive than LC-MS/MS for HT-ADME** (`LAN-20261102-27`, dmpk-adme, published )
- Verifier: facts partial, science sound. Snippets of the Evotec poster page confirm 2.5 nL droplets (scalable to 25 nL), 'potential to run 1 second cycle times', and reduced sensitivity vs LC-MS/MS plus interference from no separation, tested on microsomal stability and CYP inhibition samples. Publication date not found (left empty). Evotec is not SCIEX but sells AEMS services, so it is a CRO poster, not independent peer-reviewed evidence. The caution matches the 2022 AEMS review.
- Sources: [1] [Evotec poster](https://www.evotec.com/sciencepool/echo-ms-in-high-throughput-adme) (primary)

**7. Over half of PyLabRobot's recent commits credit an AI coding assistant** (`LAN-20261102-06`, software-orchestration, published 2026-11-03)
- 790 commits, 53 authors, ~533k lines added since 2025-11-01 [[1]](https://github.com/PyLabRobot/pylabrobot/commits/main)
- Camillo Moschner 389 commits, Rick Wierenga 266 [[1]](https://github.com/PyLabRobot/pylabrobot/commits/main)
- AI co-author trailers: Claude 444, Copilot 60 (voluntary, so a floor) [[1]](https://github.com/PyLabRobot/pylabrobot/commits/main)
- AGENTS.md and the driver guide address AI coding agents directly [[2]](https://github.com/PyLabRobot/pylabrobot/blob/7779f506d12755f5f274b4c5cab4d095f4fccb62/AGENTS.md)
- Verifier: facts partial, science sound. Recomputed from git log at 7779f50: 790 commits, 53 author names, Moschner 389 and Wierenga 266, 444 Claude and 60 Copilot trailers, 54% overall, and 9/56/69/62/80% by quarter (author date) all reproduce, but lines added are ~533k, not ~538k. The trailers are a floor for AI-assisted commits, not a share of code written, and AGENTS.md says nothing about human review.
- Sources: [1] [PyLabRobot commit history (main)](https://github.com/PyLabRobot/pylabrobot/commits/main) (primary) · [2] [AGENTS.md](https://github.com/PyLabRobot/pylabrobot/blob/7779f506d12755f5f274b4c5cab4d095f4fccb62/AGENTS.md) (primary)

**8. PyLabRobot ships no LLM or agent layer; AGENTS.md requires per-run hardware approval** (`LAN-20261102-09`, software-orchestration, published 2026-11-03)
- 'MCP' hits are Brooks Manual Control Pendant error strings [[2]](https://github.com/PyLabRobot/pylabrobot/blob/7779f506d12755f5f274b4c5cab4d095f4fccb62/pylabrobot/brooks/precise_flex/driver/errors.py)
- EventBus is 'an observation mechanism, not a control mechanism' [[3]](https://github.com/PyLabRobot/pylabrobot/blob/7779f506d12755f5f274b4c5cab4d095f4fccb62/docs/contributor_guide/event-bus.md)
- RPC listener 'does not authenticate callers' [[4]](https://github.com/PyLabRobot/pylabrobot/blob/7779f506d12755f5f274b4c5cab4d095f4fccb62/pylabrobot/rpc/README.md)
- Verifier: facts verified, science sound. A search of pylabrobot/, docs/ and pyproject at 7779f50 finds no LLM, agent-framework or MCP-protocol code; the MCP hits are Brooks Manual Control Pendant errors. The AGENTS.md, event-bus.md and rpc/README.md quotes are exact.
- Sources: [1] [AGENTS.md](https://github.com/PyLabRobot/pylabrobot/blob/7779f506d12755f5f274b4c5cab4d095f4fccb62/AGENTS.md) (primary) · [2] [PreciseFlex error table](https://github.com/PyLabRobot/pylabrobot/blob/7779f506d12755f5f274b4c5cab4d095f4fccb62/pylabrobot/brooks/precise_flex/driver/errors.py) (primary) · [3] [EventBus guide](https://github.com/PyLabRobot/pylabrobot/blob/7779f506d12755f5f274b4c5cab4d095f4fccb62/docs/contributor_guide/event-bus.md) (primary) · [4] [RPC README](https://github.com/PyLabRobot/pylabrobot/blob/7779f506d12755f5f274b4c5cab4d095f4fccb62/pylabrobot/rpc/README.md) (primary)

**9. No vendor-published SiLA 2 interface found for Hamilton, Biomek or Opentrons** (`LAN-20261103-10`, software-orchestration, published 2026-11-03)
- UniteLabs public GitLab: 19 projects, none for Hamilton [[2]](https://gitlab.com/unitelabs)
- Verifier: facts partial, science na. The GitLab API returns 19 projects for the unitelabs group (18 in its namespace), none for Hamilton. UniteLabs' STAR/VANTAGE connectors show up only in vendor docs and hub snippets. The title overstates: public community Opentrons SiLA 2 connectors exist (Acceleration Consortium). The SiLA directory also lists a Zeus (Hamilton OEM channel) driver, interface v1.2, probably SiLA 1-style.
- Sources: [1] [UniteLabs liquid handling (vendor claim)](https://unitelabs.io/lab-automation-solutions/liquid-handling/) (secondary) · [2] [UniteLabs public GitLab group](https://gitlab.com/unitelabs) (primary)

**10. Third-party AI agents drive PyLabRobot only in simulation so far** (`LAN-20261102-10`, software-orchestration, published 2026-10-27)
- plr-mcp: destructiveHint on motion tools; confirm=true required on real STAR [[1]](https://github.com/di-omics/plr-mcp/blob/db90c579439bdea0930be5f7dc0ac5fddb93b3b3/plr_mcp/server.py#L199-L206)
- OpenLabAI Hamilton server 'does not execute protocols on a physical Hamilton' [[2]](https://github.com/nygmeta/OpenLabAI/blob/daade8e9f92e573362b20f9c46738b60db55cb6d/mcp_servers/hamilton_server.py)
- labloop pipettes every plate on STARChatterboxBackend [[3]](https://github.com/sl148/closed-loop-lab-demo/blob/86b27d6c66d54e57abd22e93fefa084d2dc20f15/src/labloop/execution/plr_bridge.py#L21-L65)
- Verifier: facts verified, science sound. The plr-mcp, OpenLabAI and labloop quotes match their clones at the cited SHAs, and plr-mcp's own bring-up doc says nothing has been run on a physical STAR. Note that the article TL;DR needs 'through PyLabRobot': Coscientist and CRESt drove real OT-2s.
- Sources: [1] [plr-mcp server.py](https://github.com/di-omics/plr-mcp/blob/db90c579439bdea0930be5f7dc0ac5fddb93b3b3/plr_mcp/server.py#L199-L206) (primary) · [2] [OpenLabAI hamilton_server.py](https://github.com/nygmeta/OpenLabAI/blob/daade8e9f92e573362b20f9c46738b60db55cb6d/mcp_servers/hamilton_server.py) (primary) · [3] [labloop plr_bridge.py](https://github.com/sl148/closed-loop-lab-demo/blob/86b27d6c66d54e57abd22e93fefa084d2dc20f15/src/labloop/execution/plr_bridge.py#L21-L65) (primary)

**11. Official SiLA 2 Python SDK marked unmaintained; users pointed to UniteLabs** (`LAN-20261103-05`, standards, published 2026-09-17)
- README status 'Unmaintained' since 2026-09-17 [[1]](https://gitlab.com/SiLA2/sila_python)
- sila2 0.14.0 released 2025-12-01 [[2]](https://pypi.org/project/sila2/)
- unitelabs-sila 0.14.0 released 2026-11-02 [[3]](https://pypi.org/project/unitelabs-sila/)
- Verifier: facts verified, science na. Fresh clone of sila_python: README commit 9b0ef09 'Change status to Unmaintained' on 2026-09-17 points to gitlab.com/unitelabs/sila2/sila-python; Maintainer field is blank. PyPI JSON confirms sila2 0.14.0 uploaded 2025-12-01 (still latest) and unitelabs-sila 0.14.0 uploaded 2026-11-02.
- Sources: [1] [sila_python repository (README)](https://gitlab.com/SiLA2/sila_python) (primary) · [2] [PyPI sila2](https://pypi.org/project/sila2/) (primary) · [3] [PyPI unitelabs-sila](https://pypi.org/project/unitelabs-sila/) (primary)

**12. PyLabRobot moves its universal LiquidHandler to legacy and rewrites drivers per device** (`LAN-20261102-05`, software-orchestration, published 2026-08-01)
- PR #1000 'v1b1 changes', 1 Aug 2026, 759 files changed [[1]](https://github.com/PyLabRobot/pylabrobot/commit/14a776625)
- 'The old Driver/Backend split and capability machinery are deprecated' [[2]](https://github.com/PyLabRobot/pylabrobot/blob/7779f506d12755f5f274b4c5cab4d095f4fccb62/docs/contributor_guide/device-driver-guide.md)
- v1 STAR Pipettes.aspirate exposes 30+ firmware-level arguments [[3]](https://github.com/PyLabRobot/pylabrobot/blob/7779f506d12755f5f274b4c5cab4d095f4fccb62/pylabrobot/hamilton/star/driver/features/pipettes.py#L6101-L6140)
- Importing pylabrobot.liquid_handling raises a DeprecationWarning [[4]](https://github.com/PyLabRobot/pylabrobot/blob/7779f506d12755f5f274b4c5cab4d095f4fccb62/pylabrobot/liquid_handling/__init__.py)
- Verifier: facts verified, science sound. I checked these in a git clone at 7779f50: commit 14a776625 'v1b1 changes (#1000)' (1 Aug 2026, 759 files) created pylabrobot/legacy and moved the LiquidHandler and backend into it, and importing pylabrobot.liquid_handling now raises a DeprecationWarning. The guide quote is exact, and v1 STAR aspirate has 33 parameters (the article's '20 rules' should be 21).
- Sources: [1] [PR #1000 commit](https://github.com/PyLabRobot/pylabrobot/commit/14a776625) (primary) · [2] [Device-driver guide](https://github.com/PyLabRobot/pylabrobot/blob/7779f506d12755f5f274b4c5cab4d095f4fccb62/docs/contributor_guide/device-driver-guide.md) (primary) · [3] [v1 STAR Pipettes.aspirate](https://github.com/PyLabRobot/pylabrobot/blob/7779f506d12755f5f274b4c5cab4d095f4fccb62/pylabrobot/hamilton/star/driver/features/pipettes.py#L6101-L6140) (primary) · [4] [Deprecation shim](https://github.com/PyLabRobot/pylabrobot/blob/7779f506d12755f5f274b4c5cab4d095f4fccb62/pylabrobot/liquid_handling/__init__.py) (primary)

**13. SiLA feature library has no standard liquid-handling feature** (`LAN-20261103-07`, standards, published 2026-06-01)
- LabwareTransferManipulatorController and LabwareTransferSiteController are Verified (2023) [[1]](https://gitlab.com/SiLA2/sila_base/-/tree/master/feature_definitions)
- Verifier: facts verified, science sound. sila_base feature_definitions at master (last commit 2026-06-01): the org/silastandard core and instruments features match the summary. Both LabwareTransfer features are MaturityLevel Verified (created Dec 2022, moved to instruments Apr 2023) and CoverController is Draft. No feature in any namespace covers aspirate, dispense, deck, labware or tips.
- Sources: [1] [sila_base feature_definitions](https://gitlab.com/SiLA2/sila_base/-/tree/master/feature_definitions) (primary)

**14. Tecan's open-source FluentControl SiLA 2 connector (since 2020, updated Oct 2025)** (`LAN-20261103-08`, software-orchestration, published 2020-06-15)
- BSD-3-Clause; first published 2020-06-15; packaging update 2025-10-31; requires FluentControl [[1]](https://gitlab.com/tecan/fluent-sila2-connector)
- Verifier: facts partial, science sound. Clone confirms a BSD-3 licence (Tecan Trading AG), a C#/.NET server plus Python client, a FluentControl requirement, and commands StartFluentInSimulationMode, RunMethod, PauseRun, SetVariableValue and Aspirate/Dispense/GetTips/DropTips. The last commit is 2025-10-31, but that is a packaging update: the repo was first published 2020-06-15, so the 'publishes' framing and published date are wrong.
- Sources: [1] [Tecan fluent-sila2-connector](https://gitlab.com/tecan/fluent-sila2-connector) (primary)

**15. PyLabRobot registry lists 84 devices, 50 on the new v1 API** (`LAN-20261102-07`, software-orchestration, published 2026-11-03)
- 84 registry entries; api_version v1: 50, v0: 26, unset: 8 [[1]](https://github.com/PyLabRobot/pylabrobot/blob/7779f506d12755f5f274b4c5cab4d095f4fccb62/docs/_static/devices.json)
- Hamilton STAR listed v0 'full'; Tecan EVO v0 'basic'; Opentrons OT-2 v1 'mostly' [[1]](https://github.com/PyLabRobot/pylabrobot/blob/7779f506d12755f5f274b4c5cab4d095f4fccb62/docs/_static/devices.json)
- Described in Wierenga et al., Device (2023) [[2]](https://www.cell.com/device/fulltext/S2666-9986(23)00170-9)
- Verifier: facts verified, science na. The registry at 7779f50 has 84 entries (v1 50, v0 26, unset 8), with STAR v0 'full', EVO v0 'basic' and OT-2 v1 'mostly'; the first commit is 12 Aug 2022 by Rick Wierenga. The Device 1(4):100111 (2023) paper is confirmed by the README citation and search snippets; cell.com is blocked.
- Sources: [1] [Device registry](https://github.com/PyLabRobot/pylabrobot/blob/7779f506d12755f5f274b4c5cab4d095f4fccb62/docs/_static/devices.json) (primary) · [2] [Wierenga et al., Device 2023](https://www.cell.com/device/fulltext/S2666-9986(23)00170-9) (paper)

**16. OpentronsAI's open-source server now defaults to an Anthropic Claude model** (`LAN-20261102-11`, software-orchestration, published 2026-11-03)
- anthropic_model_name = 'claude-sonnet-5-5'; openai_model_name = 'gpt-4-1106-preview' [[1]](https://github.com/Opentrons/opentrons/blob/631207155300fe9e96e08e4cfca48d11837fbd0c/opentrons-ai-server/api/settings.py#L32-L34)
- Two tools: simulate_protocol, get_relevant_api_docs [[2]](https://github.com/Opentrons/opentrons/blob/631207155300fe9e96e08e4cfca48d11837fbd0c/opentrons-ai-server/api/domain/anthropic_predict.py#L145-L160)
- Launched 1 Feb 2024 [[3]](https://www.businesswire.com/news/home/20240201923858/en/)
- Verifier: facts verified, science sound. At 631207155, settings.py defaults to claude-sonnet-5-5 (OpenAI path kept as gpt-4-1106-preview) and anthropic_predict.py defines exactly two tools. The 1 Feb 2024 BusinessWire announcement of an 'AI-powered protocol generation tool' is confirmed in snippets only; the OpentronsAI name appears later.
- Sources: [1] [OpentronsAI settings.py](https://github.com/Opentrons/opentrons/blob/631207155300fe9e96e08e4cfca48d11837fbd0c/opentrons-ai-server/api/settings.py#L32-L34) (primary) · [2] [anthropic_predict.py tools](https://github.com/Opentrons/opentrons/blob/631207155300fe9e96e08e4cfca48d11837fbd0c/opentrons-ai-server/api/domain/anthropic_predict.py#L145-L160) (primary) · [3] [Opentrons launch release, Feb 2024](https://www.businesswire.com/news/home/20240201923858/en/) (primary)

**17. Closed-loop optimisers hand experiments to robots through a simple ask/tell loop** (`LAN-20261102-12`, self-driving-labs, published 2026-11-03)
- BayBE Campaign.recommend / add_measurements [[1]](https://github.com/emdgroup/baybe/blob/ed54e0092acd0dc07b2a920ef4b58198f608bfa1/baybe/campaign.py#L495)
- Ax Client get_next_trials / complete_trial [[2]](https://github.com/facebook/Ax/blob/5a7b3367f2d372e1653fd6c6ff1eaf8069ecc850/README.md)
- MADSci ExperimentScript -> workcell_client.start_workflow [[3]](https://github.com/AD-SDL/MADSci/blob/bbfcba5efcaeacb750252a921256de5d61d51bb2/examples/example_experiment.py#L105)
- CRESt checks recipe_confirm, ot2_deck_check, start [[4]](https://github.com/zhang21mit/CRESt/blob/8bcb140d285b58508c9b34d53bf2dc39360b2b64/Auto_SEM/main_workflow/main_workflow_func_list.py#L193-L210)
- Verifier: facts verified, science sound. The ask/tell calls and CRESt's three confirmation flags match the clones at the cited SHAs. MADSci is an orchestration framework rather than an optimiser and keeps instrument nodes in separate repos, so 'no robot driver' holds per repo only.
- Sources: [1] [BayBE campaign.py](https://github.com/emdgroup/baybe/blob/ed54e0092acd0dc07b2a920ef4b58198f608bfa1/baybe/campaign.py#L495) (primary) · [2] [Ax README](https://github.com/facebook/Ax/blob/5a7b3367f2d372e1653fd6c6ff1eaf8069ecc850/README.md) (primary) · [3] [MADSci example](https://github.com/AD-SDL/MADSci/blob/bbfcba5efcaeacb750252a921256de5d61d51bb2/examples/example_experiment.py#L105) (primary) · [4] [CRESt workflow functions](https://github.com/zhang21mit/CRESt/blob/8bcb140d285b58508c9b34d53bf2dc39360b2b64/Auto_SEM/main_workflow/main_workflow_func_list.py#L193-L210) (primary)

**18. PyLabRobot uses SiLA only to reach devices that already have a SiLA server** (`LAN-20261103-13`, software-orchestration, published 2026-11-03)
- Verifier: facts verified, science sound. At commit 7779f50 (2026-11-03): discovery.py covers SiLA 1 (NetBIOS + GetDeviceIdentification) and SiLA 2 (mDNS). grpc.py raw-protobuf helpers are used by the ImageXpress Pico backend, and the INHECO SiLA SOAP transport is used by SCILA and the legacy ODTC backend. No SiLA code exists in the liquid-handling or Hamilton modules.
- Sources: [1] [PLR SiLA discovery](https://github.com/PyLabRobot/pylabrobot/blob/7779f506d12755f5f274b4c5cab4d095f4fccb62/pylabrobot/io/sila/discovery.py) (primary) · [2] [PLR SiLA gRPC helpers](https://github.com/PyLabRobot/pylabrobot/blob/7779f506d12755f5f274b4c5cab4d095f4fccb62/pylabrobot/io/sila/grpc.py) (primary)

**19. PyLabRobot's PreciseFlex driver adds force-sensed Z probing and collision guards** (`LAN-20261102-08`, robotics-workcells, published 2026-11-02)
- probe_z_using_ztouch returns the contact height or None; detection_force default 15.0 N [[1]](https://github.com/PyLabRobot/pylabrobot/blob/7779f506d12755f5f274b4c5cab4d095f4fccb62/pylabrobot/brooks/precise_flex/driver/features/arm.py#L2422-L2470)
- PRs #1550, #1551, #1552, #1577, #1586 [[2]](https://github.com/PyLabRobot/pylabrobot/pull/1577)
- Verifier: facts verified, science sound. Git log dates #1550 to 29 Oct, #1551/#1552 to 30 Oct and #1577/#1586 to 2 Nov 2026, and probe_z_using_ztouch defaults to detection_force 15.0 N and returns a height or None. The evidence is source code only; its docstring warns that a halt from elsewhere also returns a height.
- Sources: [1] [probe_z_using_ztouch](https://github.com/PyLabRobot/pylabrobot/blob/7779f506d12755f5f274b4c5cab4d095f4fccb62/pylabrobot/brooks/precise_flex/driver/features/arm.py#L2422-L2470) (primary) · [2] [PR #1577](https://github.com/PyLabRobot/pylabrobot/pull/1577) (primary)

**20. Orca 2.3.0 adds simulation time-scaling and audit reasons for scheduler actions** (`LAN-20261104-02`, software-orchestration, published 2026-10-19)
- Simulation time scale: 1 real time, 0.1 ten times faster, 0 no pacing; LIVE runs reject it [[1]](https://github.com/Cheshire-Labs/orca/releases/tag/v2.3.0)
- Ten more operator actions write audit rows; audited actions accept an optional reason [[1]](https://github.com/Cheshire-Labs/orca/releases/tag/v2.3.0)
- Two labware cannot share a barcode (409 barcode_in_use) [[1]](https://github.com/Cheshire-Labs/orca/releases/tag/v2.3.0)
- Verifier: facts verified, science sound. Release notes confirm sim_time_scale (1 real time, 0.1 ten times faster, 0 no pacing, LIVE refused with 422), ten more audited verbs with optional reason, and 409 barcode_in_use. Release page shows 19 October without a year (2026 inferred). Applies to simulated runs only, which the summary says.
- Sources: [1] [Orca v2.3.0 release notes](https://github.com/Cheshire-Labs/orca/releases/tag/v2.3.0) (primary)

**21. Roche says it has started building autonomous AI labs** (`LAN-20261102-20`, self-driving-labs, published 2026-09-28)
- Verifier: facts partial, science na. Reuters (via syndicated copies) and FirstWord confirm that at its 28 Sep 2026 Pharma Day Roche said it has begun building autonomous AI labs (Aviv Regev; Medra and Anthropic named as collaborators). The 'six-level ladder' comes only from blogs (FourWeekMBA, saifhegazy.com); FirstWord describes a staged progression without a level count. The cited globalbankingandfinance page could not be opened.
- Sources: [1] [Global Banking & Finance coverage](https://www.globalbankingandfinance.com/roche-outlines-plans-move-towards-autonomous-ai-labs/) (secondary)

**22. labmcp-sila2 lets AI agents call SiLA 2 servers, tested only in simulation** (`LAN-20261103-14`, software-orchestration, published 2026-09-26)
- Depends on sila2>=0.12,<0.15 [[1]](https://github.com/K-Dense-AI/lab-instrument-mcps/tree/46545ea7eb818249a524c3340dc80657f448430f/servers/protocols/sila2)
- Verifier: facts verified, science sound. At commit 46545ea (2026-09-26, also the latest commit for this folder on main): labmcp-sila2 0.1.2 pins sila2>=0.12,<0.15. Its README status reads 'simulated: tested against a real in-process SiLA 2 server (sila2 library ...), not yet verified against vendor servers', and it validates parameters against the FDL. First released 2026-09-25.
- Sources: [1] [labmcp-sila2 README](https://github.com/K-Dense-AI/lab-instrument-mcps/tree/46545ea7eb818249a524c3340dc80657f448430f/servers/protocols/sila2) (primary)

**23. Orca lab scheduler 2.0 adds daemon and REST API, relicenses to SSPL** (`LAN-20261104-01`, software-orchestration, published 2026-09-23)
- v2.0.0 replaces 1.x authoring with four decorators; workflows stay plain Python [[1]](https://github.com/Cheshire-Labs/orca/pull/14)
- 'Relicensed from AGPL-3.0 to the Server Side Public License, version 1'; releases up to v1.0.0 stay AGPL-3.0 [[1]](https://github.com/Cheshire-Labs/orca/pull/14)
- Verifier: facts verified, science na. Merged PR #14 (23 Sep 2026) states daemon with REST/SSE, CLI, four decorators, AGPL-3.0 to SSPL v1, and 'Releases up to v1.0.0 stay under AGPL-3.0'. Primary source only (author merged own PR); SSPL not being OSI-approved is analysis, not in the source.
- Sources: [1] [Orca v2.0.0 pull request](https://github.com/Cheshire-Labs/orca/pull/14) (primary)

**24. Court blocks WuXi AppTec's Pentagon 1260H listing; BIOSECURE now law** (`LAN-20261102-24`, business, published 2026-08-07)
- Verifier: facts verified, science na. Several independent law-firm and trade sources confirm: BIOSECURE enacted 18 Dec 2025 as FY2026 NDAA s.851 (PL 119-60), naming no companies; WuXi AppTec added to the 1260H list 8 Jun 2026; Judge Boasberg (D.D.C.) granted a preliminary injunction 7 Aug 2026. The injunction is preliminary and DoD may redesignate; the OMB list is due 18 Dec 2026. Ropes & Gray pages were confirmed through search, not opened.
- Sources: [1] [Ropes & Gray: BIOSECURE enacted](https://www.ropesgray.com/en/insights/alerts/2026/01/biosecure-act-enacted) (secondary) · [2] [Ropes & Gray: court enjoins 1260H designation](https://www.ropesgray.com/en/insights/alerts/2026/08/federal-court-enjoins-dod-designation-of-wuxi-apptec-as-a-chinese-military-company-under-section) (secondary)

**25. OpenAI and Ginkgo: GPT-5-designed experiments cut cell-free protein cost 40%** (`LAN-20261102-13`, self-driving-labs, published 2026-02-05)
- ~36,000 experiments, 6 cycles; sfGFP cost from $698/g to $422/g [[1]](https://openai.com/index/gpt-5-lowers-protein-synthesis-cost/)
- Company preprint, not peer reviewed [[1]](https://openai.com/index/gpt-5-lowers-protein-synthesis-cost/)
- Verifier: facts verified, science sound. openai.com is blocked; snippets of OpenAI's page, Ginkgo's release and R&D World confirm ~36,000 reactions, 6 rounds, $698 to $422/g, human reagent prep, validated designs only, and a company preprint of 5 Feb 2026. The 40% is reaction cost for one protein (sfGFP), and nothing supports the 'largest' superlative.
- Sources: [1] [OpenAI announcement](https://openai.com/index/gpt-5-lowers-protein-synthesis-cost/) (primary)

**26. Labman builds a robotic design-make-test-analyse lab for an unnamed big pharma** (`LAN-20261102-28`, robotics-workcells, published 2025-01-07)
- Verifier: facts partial, science na. Labman's own page and events listing confirm its largest project, announced 7 Jan 2025: an AI-driven robotic DMTA platform of integrated modules with mobile robots for an unnamed global pharma, over two years from January 2025, built in North Yorkshire. Synthesis is confirmed; 'purification' and 'automated assays' were not seen in the snippets. Company-only source (primary for its own news).
- Sources: [1] [Labman news](https://live.labmanautomation.com/news/DMTA-drug-discovery-lab) (primary)

**27. Dispendix I.DOT ships a native SiLA 2 server** (`LAN-20261103-09`, liquid-handling, published 2022-09-14)
- Verifier: facts partial, science sound. The README confirms an on-instrument I.DOT SiLA 2 server that supports only client-initiated connections and mDNS _sila._tcp discovery, with C# client samples. The 2026-02-24 date is the latest commit (net8.0 update); the repo and the native server date from 2022-09-14, so this is not new.
- Sources: [1] [Dispendix I.DOT SiLA 2 samples](https://github.com/Dispendix/dx-idot-sila2-samples) (primary)

**28. PyLabRobot week: STAR/Prep probing offsets, VANTAstar simulation, animated 3D visualizer** (`LAN-20261109-02`, software-orchestration, published 2026-11-09)
- #1592 renames resource_offsets/jet to offsets/jets on aspirate/dispense (old names deprecated); #1595 adds offsets to probe methods [[1]](https://github.com/PyLabRobot/pylabrobot/pull/1592)
- STAR dispense: blow-out mode follows the blow-out air volume (#1593) [[2]](https://github.com/PyLabRobot/pylabrobot/pull/1593)
- v1 VANTAstar: simulation=True and setup against a saved declared configuration (#1585, #1584) [[3]](https://github.com/PyLabRobot/pylabrobot/pull/1585)
- Visualizer3D: an animated move turns a part about its joint (#1591) [[4]](https://github.com/PyLabRobot/pylabrobot/pull/1591)
- Tip-rack definitions are now always built; official_tip_rack_identity removed (#1453, mostly Opentrons racks) [[5]](https://github.com/PyLabRobot/pylabrobot/pull/1453)
- Verifier: facts partial, science sound. PRs #1592 (merged 6 Nov), #1593 (9 Nov), #1585 (7 Nov), #1591 (6 Nov), #1453 (8 Nov) and #1595 (7 Nov) are confirmed merged in the window. Imprecision: #1592 renames resource_offsets to offsets and jet to jets on aspirate/dispense (old names deprecated, commands unchanged), and the probe-method offsets come from #1595, so 'take offsets and jets' overstates it as new capability. The #1453 change mostly concerns Opentrons tip racks. The count of 'eight PRs' was not checked. Software changes in a public repo, so primary evidence is adequate.
- Sources: [1] [PR #1592 offsets and jets](https://github.com/PyLabRobot/pylabrobot/pull/1592) (primary) · [2] [PR #1593 blow-out mode](https://github.com/PyLabRobot/pylabrobot/pull/1593) (primary) · [3] [PR #1585 VANTAstar simulation](https://github.com/PyLabRobot/pylabrobot/pull/1585) (primary) · [4] [PR #1591 Visualizer3D](https://github.com/PyLabRobot/pylabrobot/pull/1591) (primary) · [5] [PR #1453 tip rack definitions](https://github.com/PyLabRobot/pylabrobot/pull/1453) (primary)

**29. Hamilton and Parallel Fluidics partner to automate advanced workflows on liquid handlers** (`LAN-20261109-01`, liquid-handling, published 2026-11-05)
- Hamilton press page lists the partnership, dated 5 Nov 2026 [[1]](https://www.hamiltoncompany.com/press-releases)
- Verifier: facts partial, science na. Hamilton's press-release listing (seen via search snippet, page itself unreachable) shows the headline and 5 Nov 2026 date, so the partnership exists. No release text was retrievable and parallelfluidics.com could not be fetched, so the 'validated on Hamilton, Tecan, Formulatrix, Opentrons' claim is unconfirmed. The summary is appropriately hedged. Parallel Fluidics being Boston-based is confirmed by search.
- Sources: [1] [Hamilton press releases](https://www.hamiltoncompany.com/press-releases) (primary) · [2] [Parallel Fluidics LNP Screening Array](https://www.parallelfluidics.com/lnp-screening-array/starter-kit) (primary)

**30. SiLA Rust 0.1.0 published to crates.io** (`LAN-20261103-11`, standards, published 2026-11-03)
- Interop: Python client vs Rust server 349/349; Rust client vs Python server 104/104 [[1]](https://gitlab.com/SiLA2/sila_rust)
- Verifier: facts verified, science sound. crates.io lists sila2-types, -build, -client and -server 0.1.0, created 2026-11-03 22:00 UTC from gitlab.com/SiLA2/sila_rust, which has a v0.1.0 tag. The README and CHANGELOG report 349/349 server and 104/104 client checks on the SiLA interoperability tester 0.10.3. These results are self-reported from CI, not independently reproduced.
- Sources: [1] [sila_rust repository](https://gitlab.com/SiLA2/sila_rust) (primary)

**31. OPC Foundation merges LADS 1.0.0 packages into its .NET SDK** (`LAN-20261103-12`, standards, published 2026-11-01)
- Verifier: facts verified, science na. The PR page shows 'Add LADS (OPC 30500-1) model, server, client, sample and docs' by marcschier, opened 31 Oct and merged 1 Nov 2026. It adds Opc.Ua.LADS, Opc.Ua.LADS.Server and Opc.Ua.LADS.Client plus a shaking-incubator sample. The OPC reference gives LADS 1.0.0 a publication date of 2023-11-30.
- Sources: [1] [UA-.NETStandard PR #4945](https://github.com/OPCFoundation/UA-.NETStandard/pull/4945) (primary)

**32. SiLA 2 base repository tags release v1.2** (`LAN-20261103-06`, standards, published 2026-02-05)
- Tags v1.0 2019-10-01, v1.1 2022-03-17, v1.2 2026-02-05 [[1]](https://gitlab.com/SiLA2/sila_base)
- Verifier: facts verified, science na. Fresh clone of sila_base shows annotated tags v1.0 'Official Release 1.0' (2019-10-01), v1.1 (tag 2022-03-17 on a 2022-02-14 commit) and v1.2 'Official Release 1.2' (tag 2026-02-05 on a 2026-02-04 commit). A search found no v1.2 specification document; the standards page still offers Parts A/B v1.1.
- Sources: [1] [sila_base repository (tags)](https://gitlab.com/SiLA2/sila_base) (primary)

**33. BioIVT acquires BeCytes Biotechnologies to expand NAMs and ADME** (`LAN-20261102-25`, business, published 2025-10-28)
- Verifier: facts partial, science na. The acquisition, Barcelona base, tissue/cell (hepatocyte) focus and NAMs/ADME framing are confirmed by BioIVT's own Business Wire release, Parc Cientific de Barcelona and Ara. The date is wrong: BioIVT's release is dated 28 Oct 2025 (Business Wire id 20251027), and 4 Nov is a later syndication/coverage date. Terms undisclosed.
- Sources: [1] [Biotech Spain](https://biotech-spain.com/en/articles/bioivt-acquires-becytes-biotechnologies-to-boost-preclinical-research-in-europe/) (secondary)

**P1. BMS automates 96-well Caco-2 permeability, matching 24-well classification for 94%** (`LAN-20261102-16`, dmpk-adme, published 2025-12-26)
- 94% of 50 literature compounds concordant with 24-well [[1]](https://pubmed.ncbi.nlm.nih.gov/41468180/)
- ASSAY Drug Dev Technol, online 26 Dec 2025 [[1]](https://pubmed.ncbi.nlm.nih.gov/41468180/)
- Verifier: facts verified, science sound. Search snippets (PubMed/SAGE pages not openable) confirm Cai X, ..., Shou W (BMS), ASSAY Drug Dev Technol, online 26 Dec 2025, DOI 10.1177/1540658X251408742: 24- to 96-well Caco-2 on an integrated culture+assay platform with cleaning, plate tracking and dynamic scheduling; 94% of 50 literature compounds classified as in 24-well. Peer-reviewed; concordance is categorical (no Papp R2, throughput or hardware in the abstract), so 'matching' means same permeability class only.
- Sources: [1] [PubMed 41468180](https://pubmed.ncbi.nlm.nih.gov/41468180/) (paper)

**P2. WuXi reads flux-dialysis protein binding by acoustic-ejection MS, ~25x faster** (`LAN-20261102-17`, dmpk-adme, published 2025-11-10)
- R² > 0.96 vs LC-MS/MS; ~25-fold faster [[1]](https://pubmed.ncbi.nlm.nih.gov/41386030/)
- Drug Metab Dispos 53(12), Dec 2025 [[1]](https://pubmed.ncbi.nlm.nih.gov/41386030/)
- Verifier: facts verified, science sound. Snippets from PubMed/DMD/ScienceDirect confirm Wen X, Wang J, Li X, Xing L, Chen G, Tao Y, Shen L (WuXi AppTec DMPK), DMD 53(12):100200, Epub 10 Nov 2025 (WuXi paper listing): AEMS fu vs LC-MS/MS R2 > 0.96, vs literature R2 > 0.95, 25-fold faster. Peer-reviewed but small (10 reference compounds, human plasma); the 25x is readout speed (about 3 s/sample, 30 nL), not whole-assay time.
- Sources: [1] [PubMed 41386030](https://pubmed.ncbi.nlm.nih.gov/41386030/) (paper)

**P3. Genentech combines hepatocyte stability and metabolite profiling in one automated assay** (`LAN-20261102-19`, dmpk-adme, published 2024-03-04)
- Three species, ~4.5 h; Drug Metab Dispos 52(5):377–389 [[1]](https://pubmed.ncbi.nlm.nih.gov/38438166/)
- Verifier: facts partial, science sound. Paper confirmed via snippets: Leung C, Liu J, Cunico K, Johnson K, Yan Z, Cai J (Genentech), DMD 52(5):377-389, DOI 10.1124/dmd.123.001618, accepted 29 Feb 2024, online about 4 Mar 2024; automation + HRMS + batch processing, hepatocytes from three species, about 4.5 h workflow (30 min prep + 4 h time course). 'Up to 60 compounds' was not found: the abstract mentions eight control compounds. Full text not reachable.
- Sources: [1] [PubMed 38438166](https://pubmed.ncbi.nlm.nih.gov/38438166/) (paper)

**P4. AstraZeneca's Wave 1: five DMPK assays on three Hamilton STARplus robots, weekly** (`LAN-20261102-18`, dmpk-adme, published 2020-05-14)
- Three Hamilton Microlab STARplus with identical configuration [[1]](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7567642/)
- Verifier: facts verified, science sound. Snippets of PMC7567642 / journal page confirm Wernevik J et al. (AstraZeneca), ASSAY Drug Dev Technol 18(4):157-179, DOI 10.1089/adt.2020.970, ahead of print 14 May 2020: DMPK Wave 1 (HLM and rat hepatocyte CLint, human PPB, dried-DMSO solubility, logD7.4) run weekly on all synthesised compounds on three identically configured Hamilton Microlab STARplus. 'No big pharma has published newer throughput figures' is editorial; AZ's own 2021 ADDT letter on acoustic dispensing/384-well workflows to raise Wave 1 capacity exists and was not checked for figures.
- Sources: [1] [PMC7567642](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7567642/) (paper)

**P5. End-to-end automated platform screens solubility and logD with 20x less material** (`LAN-20261102-29`, dmpk-adme, published 2026-08-27)
- >10x efficiency, 20x less material [[1]](https://link.springer.com/article/10.1186/s41120-026-00192-0)
- Verifier: facts verified, science questionable. Springer snippets confirm AAPS Open 12:59, published 27 Aug 2026, DOI 10.1186/s41120-026-00192-0: a 'closed-loop' platform from sample prep to data reporting for solubility, LogD and ASD screening, >10x efficiency and 20x less material. 'Closed-loop' here means an end-to-end automated workflow, not a design-make-test-learn loop; the baseline for >10x is not stated in the abstract. Authors not confirmed.
- Sources: [1] [AAPS Open](https://link.springer.com/article/10.1186/s41120-026-00192-0) (paper)

**P6. Merck's Juncai Meng presents acoustic-ejection MS uses in discovery at Pittcon 2026** (`LAN-20261102-21`, dmpk-adme, published 2026-02)
- Verifier: facts partial, science questionable. Pittcon listing confirms a talk by Juncai Meng (Merck & Co.), 8 Mar 2026, saying Merck has applied AEMS at the discovery stage, but the verbatim quote 'has been implemented at Merck' was not seen. The Meng et al. review (Analysis & Sensing 6(2) e202500218, 2026) covers ADME profiling among other uses. The talk's named uses are peptide conformation, compound QC and HT solubility, not metabolic stability or PPB, so 'routine pharma ADME work' overreaches (conference abstract + review only).
- Sources: [1] [Pittcon 2026 abstract](https://labscievents.pittcon.org/event/pittcon-2026/planning/UGxhbm5pbmdfNDI4ODM1MQ==) (primary) · [2] [Meng et al., Analysis & Sensing](https://chemistry-europe.onlinelibrary.wiley.com/doi/abs/10.1002/anse.202500218) (paper)

**P7. Mdr1-knockout MDCK cells estimate human intestinal permeability** (`LAN-20261102-30`, dmpk-adme, published 2025-09-07)
- Verifier: facts verified, science sound. Snippets (ACS, PMC12505271, SDU portal) confirm Beran K ... Evers R, Mol Pharm 22(10):6067-6082, DOI 10.1021/acs.molpharmaceut.5c00755, online 7 Sep 2025 (issue 6 Oct), with the 3-7 vs 14-28 day culture statement. Peer-reviewed, but the base is 16 reference compounds (R2 > 0.8) and 6 test APIs, and with P-gp knocked out it holds for passive permeability only, which the summary should say.
- Sources: [1] [Mol Pharm 22(10):6067](https://pubs.acs.org/mpohbp/article/22/10/6067/3749648/) (paper)

**P8. LabSafety Bench: no AI model above 70% on lab hazard identification** (`LAN-20261102-14`, self-driving-labs, published 2026-01-14)
- 19 LLMs/VLMs evaluated; none >70% on hazard identification [[1]](https://www.nature.com/articles/s42256-025-01152-1)
- Nat Mach Intell 8:20–31, online 14 Jan 2026 [[1]](https://www.nature.com/articles/s42256-025-01152-1)
- Verifier: facts partial, science sound. Snippets of the abstract confirm 19 LLMs/VLMs and none above 70% on hazard identification (peer-reviewed), but the paper was published in Nat Mach Intell 8:20-31 on 14 Jan 2026, not in 2025. nature.com and arxiv.org are blocked.
- Sources: [1] [LabSafety Bench, Nat Mach Intell](https://www.nature.com/articles/s42256-025-01152-1) (paper) · [2] [arXiv 2410.14182](https://arxiv.org/abs/2410.14182) (paper)

## Feedback

> **Brief:** _/5 · **Missed:** _ · **Notes:** _ · `LAN-W20261109`

> **Scope:** Add: _ · Remove: _ · `LAN-S20261109`

Rate stories 1-5 (5 = must-know) and tag freely (`must-know`, `useful`, `meh`, `off-topic`, `wrong`, `unsound`, `hype`, `stale`, `dup`, `shallow`, `great`, `more`, `less`). **Missed**: anything this brief should have had. **Scope**: sites, companies or topics to add or remove, e.g. `Add: Opentrons blog, Automata · Remove: Telescope Innovations`.
