# Getting at the blocked source sites

The scheduled cloud run sits behind a network allowlist. On 2026-11-14 a probe from the run
reached only `github.com` (through git) and `raw.githubusercontent.com`. Everything else was
refused at the proxy: every source site, the GitHub API, the literature APIs (Crossref,
PubMed, Europe PMC, OpenAlex, arXiv, bioRxiv, Semantic Scholar), and every relay that might
have worked around the block (Google News RSS, Bing News, web.archive.org, r.jina.ai, the
press-release wires' RSS, trade-press RSS). WebFetch fails the same way. A relay is just
another blocked host, so going through one doesn't help.

What does work from inside the run is **WebSearch**. It runs on Anthropic's side, so the
allowlist doesn't apply to it. It returns titles, links, dates and snippets, not full pages.
That is the current fallback, and it is why items rest on search snippets and the verifier
often marks facts `partial`.

There are three ways to do better, in order of preference.

## 1. Allow the domains in the environment (best, a settings change by the user)

In claude.ai/code, open the environment's settings → Network access. Either choose full
access, or add these hosts to a custom allowlist
([docs](https://code.claude.com/docs/en/claude-code-on-the-web)):

- Core sites: `labautomation.io`, `www.slas.org`, `www.lrig.org`, `elrig.org`,
  `www.hamiltoncompany.com`, `www.tecan.com`, `www.agilent.com`, `www.beckman.com`
- Literature APIs: `api.crossref.org`, `eutils.ncbi.nlm.nih.gov`, `pubmed.ncbi.nlm.nih.gov`,
  `export.arxiv.org`, `api.biorxiv.org`, `www.ebi.ac.uk` (Europe PMC)
- News aggregation: `news.google.com` (RSS search feeds, which cover trade press, wires and
  start-up news in one place)
- Verification: `www.nature.com`, `doi.org`, `www.sciencedirect.com`, `www.prnewswire.com`,
  `www.businesswire.com`, `www.globenewswire.com`, `api.github.com`

With these allowed, `fetch_sources.py` reads the feeds directly, and both the researcher and the
verifier can open primary pages instead of relying on snippets.

## 2. The feed-fetch GitHub Action (no settings change; built 2026-11-14)

`.github/workflows/fetch-feeds.yml` runs `fetch_sources.py --all --weekly` every day on
GitHub's runners, which have open internet. It commits only `data/raw/links.jsonl` and
`fetch_log.jsonl` (headline metadata) to the branch `claude/feeds-bot`. On Monday,
`sync_state.py` merges that branch like any other `claude/*` branch, and
`uv run fetch_sources.py --new --days 7` then lists the week's headlines, including Google
News searches for autonomous-lab start-up news and an arXiv self-driving-lab query.

To switch it on:
1. Merge the workflow file to `main`. Scheduled workflows run only from the default branch.
2. Repo Settings → Actions → General: allow Actions to run, and set Workflow permissions to
   "Read and write" so the job can push its branch.
3. Optional: Actions tab → fetch-feeds → "Run workflow" to seed it once.

Limits: it fetches headlines, not article bodies. The run still opens each lead through search,
and the verifier still can't fetch the pages, so option 1 remains the full fix.

## 3. Search only (what runs today)

Site-restricted WebSearch (`allowed_domains` = a source's `search.domains`), extended mode for
core and autonomous-lab queries. LinkedIn stays search-only in every case: it's behind a
login, and its terms forbid scraping.
