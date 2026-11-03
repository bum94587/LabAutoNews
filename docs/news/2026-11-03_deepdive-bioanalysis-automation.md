# Deep dive: Bioanalysis automation: acoustic ejection MS and high-throughput PK, 2026-11-03
Scope: how acoustic ejection mass spectrometry (AEMS) changes the readout side of ADME automation. Searched open web and vendor sites; page fetches were blocked here, so details rest on search-result text and are marked. Vendor claims are labelled as such.

## TL;DR
- AEMS skips the chromatography column: nanolitre droplets are fired straight into the MS, so a plate is read in minutes, not hours [1][2].
- SCIEX claims up to 10x throughput for metabolic stability, and up to 60x (2 s per sample) on Echo MS+; the two notes use different LC-MS baselines. Vendor figures, no independent validation found [1][2].
- Academic validation is mostly outside ADME (covalent screening, reaction analysis) [3][4]; pharma interest is real but evidenced by talk abstracts [5].
- Shifting the bottleneck: when the readout is seconds per sample, incubation, liquid handling and data review set the pace.

## How it works (the "learn a topic" part)
A classic automated ADME run is: liquid handler prepares incubations, quenches, centrifuges, then an LC-MS/MS injects each sample, with a chromatographic gradient of one to several minutes per sample. That gradient is the slowest step.
AEMS replaces it: an acoustic transducer (the same physics as Beckman's Echo liquid handlers) ejects picolitre-to-nanolitre droplets from a well into an open-port interface, a flow of solvent carries them into electrospray MS [5]. No column means no separation, so each sample takes roughly one second to a few seconds [2][5].

## What the evidence says
- **Throughput (vendor):** Up to 10x versus LC-MS/MS on 23 compounds in human and rat microsomes [1]. Echo MS+ with ZenoTOF 7600+ is claimed at 2 s per sample with equivalent half-lives [2]. Treat "up to" figures as best cases.
- **Software closes the loop:** LeadScape Analyze builds MRM methods, runs batches and processes data automatically on the Echo MS [6]. Analysis is the second automation target after sample handling.
- **Independent work:** An SLAS Technology paper used AEMS for covalent BTK inhibitor screening, reactivity and potency [3]. Hu and Blair (Nature 2024) analysed reactions via fragmentation patterns instead of chromatography [4]. Neither is a DMPK assay.
- **Trade-offs (analysis, from general knowledge, not confirmed by fetched sources):** no separation means ion suppression and isobaric interference are harder to see, and sensitivity is generally lower than LC-MS/MS, so AEMS suits early-tier assays (metabolic stability, solubility) more than regulated PK bioanalysis.

## What to watch
- A peer-reviewed head-to-head of AEMS vs LC-MS/MS on a full ADME panel, from a pharma or CRO.
- Whether workcell vendors (Hamilton, Tecan, Beckman) ship integrated incubation-to-Echo-MS workflows.
- MCP/agent layers on MS data systems (reported for Waters), which would let AI agents queue and review runs [7].

## References
[1] SCIEX, "Up to 10x increased throughput for metabolic stability assays", tech note, undated, https://sciex.com/tech-notes/pharma/discovery/10x-increased-throughput-for-metabolic-stability-assays (primary, vendor)
[2] SCIEX, "Accelerating ADME workflows: AEMS for high-throughput metabolic stability studies", tech note, undated, https://sciex.com/tech-notes/pharma/accelerating-adme-workflows-aems-for-high-throughput-metabolic-stability-studies (primary, vendor)
[3] Cheng et al., SLAS Technology, Aug 2025, https://doaj.org/article/07194c6df2a2440497f6c7b117155dcc (paper)
[4] Hu and Blair, Nature 636, Dec 2024, https://doi.org/10.1038/s41586-024-08211-4 (paper)
[5] Pittcon 2026 session, 8 Mar 2026, https://labscievents.pittcon.org/event/pittcon-2026/planning/UGxhbm5pbmdfNDI4ODM1MQ== (secondary, abstract)
[6] SCIEX, "Automating high-throughput ADME assays with LeadScape Analyze", https://sciex.com/tech-notes/pharma/discovery/automating-high-throughput-adme-assays-with-leadscape-analyze-s (primary, vendor)
[7] Drug Discovery News, "Is the autonomous lab finally achievable?", Oct 2026, https://www.drugdiscoverynews.com/is-the-autonomous-lab-finally-achievable-17574 (secondary; page not fetched, claim from search snippet)

> **Rate:** _/5 · **Tags:** _ · `LAN-D20261103`
