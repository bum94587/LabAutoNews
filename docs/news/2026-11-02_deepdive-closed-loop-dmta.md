# Deep dive: Closed-loop / self-driving DMTA in pharma, 2026-11-02
Scope: real deployments versus claims, and where DMPK data enters the loop. Searched with site-restricted and open web search; most primary pages could not be fetched here (network policy), so details rest on search-result text and press coverage and are marked accordingly.

## TL;DR
- Public 2026 "closed-loop" announcements are mostly **plans and partnerships**, not measured results: Danaher's autonomous lab targets 8x faster antibody-reagent discovery, operating at scale only in early 2027 [1].
- Pharma is buying **standardized data at scale** as the foundation: AstraZeneca and Carterra will co-build hardware and software for lab-in-the-loop work, with no terms or outputs disclosed [2].
- **DMPK/ADME mostly enters at the "design" end today** as predictive models (Lilly TuneLab) rather than as automated assays inside a running loop [3].
- Cycle-time claims (hours versus weeks) in circulation come from vendor or unsourced pages; treat as unverified [4][5].

## What is actually deployed or announced
**Danaher / Abcam (7 Oct 2026).** A planned AI design-build-test loop for affinity reagents such as antibodies, hosted at Abcam, with company targets of up to 8x faster discovery and up to 10x annual output. Scale-up is expected in early 2027 [1]. *Analysis:* these are targets, and reagents are not small-molecule ADME, so transfer to DMPK is indirect.

**AstraZeneca / Carterra (8 Oct 2026).** A research collaboration on hardware and software that generates standardized experimental data for AI/ML-guided design; Carterra builds high-throughput SPR [2]. Outlet dates differ (8 vs 14 Oct). No financial terms, timelines or first outputs were found.

**Vendor platforms.** XtalPi describes hundreds of workstations running a 24/7 closed-loop DMTA cycle and claims a 5-8x efficiency gain [4]; this is a vendor claim with no independent evidence found.

**Research prototypes.** A 2025 arXiv paper (Tippy) proposes five specialised agents (Supervisor, Molecule, Lab, Analysis, Report) for DMTA automation and describes itself as production-ready [6]. *Analysis:* an author claim; I could not read the evaluation here.

## Where DMPK data enters the loop
- **Predict first.** Lilly's TuneLab serves ADME/ADMET predictions to biotechs using federated learning so partners need not share raw data (launched Sept 2025; Lilly's data-point counts could not be verified) [3]. This shapes which compounds are made, but is not itself an automated wet-lab loop.
- **Test step.** Automated in-vitro ADME (e.g. 96-well Caco-2) exists as stand-alone platforms; I found no 2026 public example where such assays feed a *closed* loop with no human hand-off. *Speculation:* the slow, multi-day assays (cell-based permeability, hepatocyte clearance) are the likely bottleneck for true closed-loop cycle times.

## What to watch
- Whether Danaher or AstraZeneca/Carterra publish measured cycle times after early 2027 [1][2].
- Any pharma disclosure of ADME assay results feeding automated compound selection without manual review.
- Independent evaluation of agentic DMTA systems such as Tippy [6].

## References
[1] Danaher accelerates Life Sciences research with new AI-powered autonomous lab, HPCwire (Danaher release), 7 Oct 2026, https://www.hpcwire.com/off-the-wire/danaher-accelerates-life-sciences-research-with-new-ai-powered-autonomous-lab/ (secondary)
[2] Carterra advances lab-in-the-loop drug discovery through new scientific collaboration, News-Medical, 8 Oct 2026, https://www.news-medical.net/news/20261008/Carterra-advances-lab-in-the-loop-drug-discovery-through-new-scientific-collaboration.aspx (secondary); SelectScience, https://www.selectscience.net/article/carterra-advances-lab-in-the-loop-drug-discovery-through-collaboration-with-astrazeneca (secondary)
[3] Lilly TuneLab, https://tunelab.lilly.com/ (primary); BioPharmaTrend, https://www.biopharmatrend.com/news/lilly-offers-biotechs-access-to-ai-models-trained-on-1b-in-proprietary-drug-discovery-data-1363/ (secondary)
[4] XtalPi autonomous lab solution, https://en.xtalpi.com/lab_automation/ (vendor, primary for its own claim)
[5] Self-Driving Labs in Pharma: Closed-Loop R&D That Works, IntuitionLabs, https://intuitionlabs.ai/articles/self-driving-labs-pharma-rd (secondary, low confidence)
[6] Accelerating Drug Discovery Through Agentic AI: A Multi-Agent Approach to Laboratory Automation in the DMTA Cycle, arXiv 2507.09023, 2025, https://arxiv.org/abs/2507.09023 (paper, preprint)

> **Rate:** _/5 · **Tags:** _ · `LAN-D20261102`
