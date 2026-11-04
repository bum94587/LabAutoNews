# Deep dive: Automated in vitro ADME screening platforms in 2026: who runs what, throughput, recent papers, 1 Nov 2026

Scope: pharma in-house platforms, CROs, vendor systems and 2025–2026 papers on automated metabolic stability, CYP, permeability, protein binding and solubility. Written 3 Nov as a make-up for the 1 Nov slot. PubMed, publisher and vendor sites were blocked here, so most details rest on search-result text and are marked; CRO and vendor numbers are their own claims.

Verifier (independent agent, 3 Nov): 6 items verified, 11 partly verified, 1 contradicted and removed; corrections applied. Badges: ✅ verified · 🟡 partly verified · 🔬 science sound · ⚠️ claim questionable or self-reported.

## TL;DR

- **The best public picture of an in-house ADME factory is still AstraZeneca's "Wave 1"**: five assays on three identical Hamilton STARplus robots, run weekly on every new compound; the paper is from 2020, and we found no newer published compounds-per-week figure from a big pharma [1]. ✅
- **The newest platform paper is BMS's automated 96-well Caco-2 assay** (online 26 Dec 2025): 94% correct classification of 50 reference compounds versus the old 24-well format, explicitly built to feed "predict-first" design [2]. ✅🔬
- **The readout is where things are moving**: WuXi showed acoustic-ejection MS (AEMS) reading out flux-dialysis protein binding about 25 times faster than LC-MS/MS, with R² > 0.96, on 10 reference compounds [3] ✅🔬; see our [AEMS deep dive](2026-11-03_deepdive-bioanalysis-automation.md).
- **Automated assays are being re-valued as AI training data**: federated ADMET models (Lilly TuneLab, the Apheris ADMET Network) and open, single-platform datasets (OpenADMET/Octant) are the 2025–26 storyline [4][5][6]. ✅

## Who runs it in-house

**AstraZeneca.** Wave 1 measures human liver microsome and rat hepatocyte intrinsic clearance (CLint), human plasma protein binding (PPB), solubility from dried DMSO and logD7.4. It runs on all compounds synthesised across AZ, and three Hamilton Microlab STARplus robots with identical decks do the pooling, cherry-picking, timepoint sampling and quenching [1]. The paper replaced bespoke assays that ran "tens of compounds per week to several hundreds" [1]. *Snippet-level; check the full text before quoting throughput.*

**Bristol Myers Squibb.** Cai et al. describe moving Caco-2 permeability from 24- to 96-well plates on an integrated platform that also handles the cell culture, with plate tracking, cleaning protocols and dynamic scheduling. The platform classified 94% of 50 literature compounds the same way as the 24-well format [2]. The abstract claims efficiency and turnaround gains but gives no compounds-per-week number and does not name the hardware [2].

**Genentech/Roche.** A 2024 *Drug Metabolism and Disposition* paper (Leung et al.) combines hepatocyte stability with metabolite profiling using automation and high-resolution MS, covering three species in about 4.5 hours [7]. 🟡🔬 At its Pharma Day on 28 September 2026 Roche said it has started building "autonomous AI labs", without claiming one is running [8]. 🟡

**Merck/MSD.** A Pittcon 2026 talk by Merck's Juncai Meng covered applying AEMS in discovery, for quality control, peptide conformation and solubility; metabolic stability was not among the uses we could confirm [9]. 🟡⚠️

**The gap.** Targeted searches found nothing from 2024–2026 describing in-house ADME automation at Pfizer, GSK, Bayer, Takeda, Boehringer Ingelheim, Janssen or AbbVie. That is a limit of what search could reach, not evidence that they have none.

## The CRO layer

CROs publish the most specific numbers, all self-reported and mostly undated (🟡⚠️):

| CRO | Claim | Source |
|---|---|---|
| Charles River | Up to 500 compounds/week for primary HT-ADME assays (microsomal stability, Caco-2, MDCK-MDR1, PPB, blood/plasma ratio); Hamilton liquid handlers and ≤5-day turnaround per an older CRL article | [11] |
| Cyprotex (Evotec) | <72 h on key assays for high-capacity contracts; "thousands of compounds a week" for regular clients | [12] |
| WuXi AppTec | 300k+ in vitro studies a year (all DMPK) | [13] |
| Pharmaron | Discovery ADME "in as little as 5 days" | [15] |

Two business notes. BioIVT announced its purchase of BeCytes Biotechnologies (Barcelona, tissue and cells) on 28 October 2025 [16]. 🟡 For US sponsors, WuXi's status has been volatile: the BIOSECURE Act was enacted on 18 December 2025 without naming WuXi, WuXi AppTec was added to the Pentagon's 1260H list on 8 June 2026, and a federal court blocked that designation on 7 August 2026 [17]. ✅ *Analysis:* outsourcing decisions for ADME screening now carry a policy-risk line item.

## Vendors: the plumbing is mature, the readout is moving

- **No ADME-specific liquid-handling launches in 2025–26** turned up from Hamilton, Tecan, Beckman, Agilent, Thermo, Pion or Sotax; their ADME workflow pages are long-standing (Tecan, for example, claims up to 600 PAMPA assays a day) [18].
- **SCIEX Echo MS+** (launched February 2024, with a ZenoTOF 8600 option added in February 2026) is the main new ADME-relevant readout hardware; SCIEX's Echo MS tech note claims about 10x throughput for metabolic stability, a vendor figure that has not been peer reviewed [19]. 🟡⚠️
- **Evotec's own poster** on Echo MS for HT-ADME notes the trade-off: 2.5 nL droplets and the potential for 1 s cycle times, but lower sensitivity than LC-MS/MS and interference from having no chromatographic separation [20]. Evotec also sells AEMS-based services, and the poster is not peer reviewed. 🟡🔬
- **Labman** is building a robotic design-make-test-analyse lab with mobile robots for an unnamed global pharma, over two years from January 2025 (company announcement) [21]. 🟡

## Recent papers (2025–2026)

| Paper | What is new | Ref |
|---|---|---|
| Cai et al. (BMS), *ASSAY Drug Dev Technol*, online 26 Dec 2025 | Automated 96-well Caco-2; 94% of 50 compounds in the same permeability class as 24-well | [2] ✅🔬 |
| Wen et al. (WuXi), *Drug Metab Dispos* 53(12), online 10 Nov 2025 | Flux-dialysis PPB read by AEMS; R² > 0.96 vs LC-MS/MS on 10 compounds; readout ~25x faster | [3] ✅🔬 |
| *AAPS Open* 12:59, 27 Aug 2026 | End-to-end automated solubility, logD and amorphous-dispersion screening; >10x efficiency (no stated baseline), 20x less material | [22] ✅⚠️ |
| Beran et al., *Mol Pharm* 22(10), online 7 Sep 2025 | Mdr1-knockout MDCK cells estimate human jejunal permeability (16 reference compounds, passive permeability); 3–7 days of culture vs 14–28 for Caco-2 | [23] ✅🔬 |
| Meng et al., *Analysis & Sensing*, Feb 2026 | Review of AEMS across discovery, including ADME profiling | [24] 🟡 |
| ISSX 2025 poster P9 | Automated hepatocyte and microsomal stability, 96- vs 24-well "strong concordance" (abstract only; Tecan Fluent 780 for microsomes) | [25] ✅⚠️ |

**Not found:** a 2025–26 methods paper on automated CYP inhibition, automated PAMPA or automated kinetic solubility, and a peer-reviewed pharma paper using AEMS for metabolic stability. The search tools could not reach PubMed directly, so these may exist.

## Where the data goes next

- **Federated models:** Lilly's TuneLab (launched 9 September 2025) offers ADMET models trained on Lilly data and fine-tuned on partners' data without sharing it; we covered it on 2 Nov (`LAN-20261102-04`) [4]. The Apheris ADMET Network (25 February 2026) has founding members, including Lundbeck, Orion, Recursion and Servier, pooling about 80% of their relevant ADMET data into a federated model [5]. ✅
- **Open data:** OpenADMET and Octant released CYP3A4/CYP2J2 reactivity and CYP3A4 inhibition data under CC BY 4.0; the reactivity readout ran on a SCIEX Echo MS+ with a ZenoTOF 7600 (released 2 March 2026) [6]. ✅🔬
- *Analysis:* when the "test" step feeds a model, consistency matters more than raw capacity. AZ harmonised across sites, BMS benchmarked 96-well against 24-well, and OpenADMET stresses single-platform data for the same reason [1][2][6].

## What to watch

- **Whether AEMS crosses from protein binding into published metabolic-stability workflows in pharma**, with sensitivity data against LC-MS/MS [3][20].
- **Throughput disclosure:** any 2026–27 paper giving current compounds-per-week and turnaround for an in-house ADME platform, the number this field rarely publishes [1][2].
- **Policy and outsourcing:** the OMB "biotechnology companies of concern" list due around December 2026 under BIOSECURE [17].

## References

1. Wernevik J. et al., "A Fully Integrated Assay Panel for Early Drug Metabolism and Pharmacokinetics Profiling", *ASSAY Drug Dev Technol* (2020): [https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7567642/](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7567642/), [https://doi.org/10.1089/adt.2020.970](https://doi.org/10.1089/adt.2020.970) (paper)
2. Cai X. et al. (BMS), "Building a State-of-the-Art Automation Platform to Support High-Throughput 96-Well Caco-2 Permeability Assay", *ASSAY Drug Dev Technol*, online 26 Dec 2025: [https://pubmed.ncbi.nlm.nih.gov/41468180/](https://pubmed.ncbi.nlm.nih.gov/41468180/) (paper)
3. Wen X. et al. (WuXi AppTec), "Application of acoustic ejection mass spectrometry for plasma protein binding assay using flux dialysis", *Drug Metab Dispos* 53(12), Dec 2025: [https://pubmed.ncbi.nlm.nih.gov/41386030/](https://pubmed.ncbi.nlm.nih.gov/41386030/) (paper)
4. Lilly, "Lilly launches TuneLab platform…", 9 Sep 2025: [https://investor.lilly.com/news-releases/news-release-details/lilly-launches-tunelab-platform-give-biotechnology-companies](https://investor.lilly.com/news-releases/news-release-details/lilly-launches-tunelab-platform-give-biotechnology-companies) (primary)
5. Apheris, "Apheris launches ADMET Network", 25 Feb 2026: [https://www.apheris.com/resources/apheris-launches-admet-network](https://www.apheris.com/resources/apheris-launches-admet-network); GEN coverage: [https://www.genengnews.com/topics/artificial-intelligence/admet-predictions-get-ai-boost-federated-data-network-unites-pharma/](https://www.genengnews.com/topics/artificial-intelligence/admet-predictions-get-ai-boost-federated-data-network-unites-pharma/) (primary / secondary)
6. OpenADMET, Octant CYP data release: [https://github.com/OpenADMET/Octant_CYP_blog_post](https://github.com/OpenADMET/Octant_CYP_blog_post) (primary)
7. Genentech, integrated hepatocyte stability and metabolite profiling assay, *Drug Metab Dispos* (2024): [https://pubmed.ncbi.nlm.nih.gov/38438166/](https://pubmed.ncbi.nlm.nih.gov/38438166/) (paper)
8. Roche Pharma Day, 28 Sep 2026, coverage: [https://www.globalbankingandfinance.com/roche-outlines-plans-move-towards-autonomous-ai-labs/](https://www.globalbankingandfinance.com/roche-outlines-plans-move-towards-autonomous-ai-labs/) (secondary)
9. Pittcon 2026 session abstract, "Application of Acoustic Ejection Mass Spectrometry to Accelerate Small Molecules Discovery Process": [https://labscievents.pittcon.org/event/pittcon-2026/planning/UGxhbm5pbmdfNDI4ODM1MQ==](https://labscievents.pittcon.org/event/pittcon-2026/planning/UGxhbm5pbmdfNDI4ODM1MQ==) (primary)
10. *(Removed after verification: the cited ACS Omega paper is not the Novartis solubility study the draft described.)*
11. Charles River, High-Throughput ADME: [https://www.criver.com/products-services/lab-sciences/dmpk/high-throughput-adme-ht-adme](https://www.criver.com/products-services/lab-sciences/dmpk/high-throughput-adme-ht-adme) (primary)
12. Cyprotex/Evotec, working with Cyprotex: [https://www.evotec.com/solutions/drug-discovery-preclinical-development/cyprotex-adme-tox-solutions/about-cyprotex/working-with-cyprotex](https://www.evotec.com/solutions/drug-discovery-preclinical-development/cyprotex-adme-tox-solutions/about-cyprotex/working-with-cyprotex) (primary)
13. WuXi AppTec DMPK, about: [https://dmpkservice.wuxiapptec.com/about-wuxi-apptec-dmpk.html](https://dmpkservice.wuxiapptec.com/about-wuxi-apptec-dmpk.html) (primary)
14. *(Removed after verification: the Medicilon throughput figure could not be confirmed.)*
15. Pharmaron, global DMPK solutions: [https://www.pharmaron.com/knowledge-center/global-dmpk-solutions/](https://www.pharmaron.com/knowledge-center/global-dmpk-solutions/) (primary)
16. BioIVT acquires BeCytes Biotechnologies (announced 28 Oct 2025): [https://biotech-spain.com/en/articles/bioivt-acquires-becytes-biotechnologies-to-boost-preclinical-research-in-europe/](https://biotech-spain.com/en/articles/bioivt-acquires-becytes-biotechnologies-to-boost-preclinical-research-in-europe/) (secondary)
17. Ropes & Gray, "BIOSECURE Act enacted" (Jan 2026): [https://www.ropesgray.com/en/insights/alerts/2026/01/biosecure-act-enacted](https://www.ropesgray.com/en/insights/alerts/2026/01/biosecure-act-enacted); court enjoins WuXi 1260H designation (Aug 2026): [https://www.ropesgray.com/en/insights/alerts/2026/08/federal-court-enjoins-dod-designation-of-wuxi-apptec-as-a-chinese-military-company-under-section](https://www.ropesgray.com/en/insights/alerts/2026/08/federal-court-enjoins-dod-designation-of-wuxi-apptec-as-a-chinese-military-company-under-section) (secondary)
18. Tecan ADME-Tox applications: [https://lifesciences.tecan.com/applications_and_solutions/drug_discovery/adme-tox](https://lifesciences.tecan.com/applications_and_solutions/drug_discovery/adme-tox) (primary)
19. SCIEX, Echo MS system press release (Feb 2024): [https://sciex.com/about-us/press-releases/2024/sciex-expands-high-throughput-screening-solutions-with-echo-ms-system](https://sciex.com/about-us/press-releases/2024/sciex-expands-high-throughput-screening-solutions-with-echo-ms-system); tech note: [https://sciex.com/tech-notes/pharma/discovery/10x-increased-throughput-for-metabolic-stability-assays](https://sciex.com/tech-notes/pharma/discovery/10x-increased-throughput-for-metabolic-stability-assays) (primary)
20. Evotec, Echo MS in high-throughput ADME: [https://www.evotec.com/sciencepool/echo-ms-in-high-throughput-adme](https://www.evotec.com/sciencepool/echo-ms-in-high-throughput-adme) (primary)
21. Labman, robotic DMTA lab: [https://live.labmanautomation.com/news/DMTA-drug-discovery-lab](https://live.labmanautomation.com/news/DMTA-drug-discovery-lab) (primary)
22. "Develop an algorithmic analytics-enabled end-to-end high-throughput platform for solubility, LogD, and ASD formulation screening", *AAPS Open* (2026): [https://link.springer.com/article/10.1186/s41120-026-00192-0](https://link.springer.com/article/10.1186/s41120-026-00192-0) (paper)
23. "Canine Mdr1 Knockout MDCK Cells Reliably Estimate Human Small Intestinal Permeability (Peff) and Fraction Absorbed (fa)", *Mol Pharm* 22(10):6067 (2025): [https://pubs.acs.org/mpohbp/article/22/10/6067/3749648/](https://pubs.acs.org/mpohbp/article/22/10/6067/3749648/) (paper)
24. Meng et al., "Application of Acoustic Ejection Mass Spectrometry to Accelerate Drug Discovery", *Analysis & Sensing* (Feb 2026): [https://chemistry-europe.onlinelibrary.wiley.com/doi/abs/10.1002/anse.202500218](https://chemistry-europe.onlinelibrary.wiley.com/doi/abs/10.1002/anse.202500218) (paper)
25. 14th ISSX meeting abstracts (2025), poster P9: [https://cdn.ymaws.com/www.issx.org/resource/resmgr/meetings_-_general/2025/ISSX_2025_Complete_Abstract_.pdf](https://cdn.ymaws.com/www.issx.org/resource/resmgr/meetings_-_general/2025/ISSX_2025_Complete_Abstract_.pdf) (paper)

> **Rate:** _/5 · **Tags:** _ · `LAN-D20261101`
