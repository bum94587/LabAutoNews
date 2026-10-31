---
name: deep-research
description: Run a lab-automation research pass (daily scan, weekly digest, or a topic deep dive) and write a cited report into reports/. Use when asked for lab automation news, a weekly report, or a deep dive on a lab-automation topic.
argument-hint: "daily | weekly | deepdive \"<topic>\""
---

# Lab automation deep research

Arguments: `$ARGUMENTS` (default `weekly`).

## 1. Set the window
- `daily`: last 24-36 h. `weekly`: last 7 days. `deepdive`: no hard window,
  but lead with the last 12 months.
- Read `data/watchlist.yaml` and the last 2 reports in `reports/` so you know
  what is already covered. Load `data/seen.jsonl` for URL dedupe.

## 2. Search wide, in parallel
Run several web searches per segment in the watchlist, plus searches for each
tracked company name + "announces" / "raises" / "launches" / "acquires".
Also check: new preprints (self-driving lab, autonomous experimentation,
laboratory robotics), funding rounds, M&A, product launches, partnerships,
layoffs/shutdowns, regulatory or standards news.

## 3. Go deep on what matters
For each candidate item, open the primary source and confirm: who, what,
when (publication date), numbers (round size, valuation, throughput claims).
Drop anything outside the window or that you cannot verify.

## 4. Write the report
Path: `reports/YYYY/YYYY-MM-DD-<type>.md`. Structure:

```
# Lab Automation <Weekly|Daily|Deep Dive>: <date or topic>

## TL;DR            (3-5 bullets, the things a busy reader must know)
## Top stories      (each: headline, date, 2-4 sentence summary, why it matters, source links)
## Funding & deals  (table: company | round/deal | amount | investors/acquirer | date | link)
## Products & tech
## Research         (papers/preprints with one-line takeaway)
## Signals to watch (trends forming across items; label as analysis)
## Sources          (every URL cited)
```

## 5. Update state and commit
- Append one JSON line per covered item to `data/seen.jsonl`:
  `{"date":"YYYY-MM-DD","url":"...","title":"...","report":"<report path>"}`
- Add any newly important company to `data/watchlist.yaml`.
- `git add reports data && git commit -m "report: <type> <date>"` and push.
