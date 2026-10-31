---
name: deep-research
description: Run the LabAutoNews research pass - the daily run (gather + verify items), and on Mondays the weekly brief - or a one-off topic deep dive. Use for "run the daily research", "build the weekly brief", or any lab-automation news/deep-dive request in this repo.
argument-hint: "daily | weekly | deepdive \"<topic>\""
---

# LabAutoNews research run

Arguments: `$ARGUMENTS` (default `daily`). Dates are America/Los_Angeles. `D` = today.
`daily` on a Monday also does the `weekly` steps.

## 0. Orient (every run)
1. `uv sync`, then `uv run sync_state.py`: pulls the items, verdicts and ratings that earlier
   runs left on other branches. Without this step you will duplicate work.
2. Read `config/sources.yaml`, `config/watchlist.yaml`, `config/weights.json` (if present) and
   `docs/tuning.md`: what the user has rated up or down, `steer.more` / `steer.less`, and
   `missed_leads`.
3. List the ids, titles and URLs of all items from the last 30 days (`data/items/`) so that you
   never add the same story twice. A genuinely new development in an old story is a new item
   that says what changed.

## 1. Collect (daily)
1. `uv run fetch_sources.py`, then `uv run fetch_sources.py --new` for the links first seen today.
   Sources that fail are normal when the network policy blocks them. Cover those with search.
2. For **every core source** in `config/sources.yaml`, run its site-restricted searches:
   WebSearch with `allowed_domains` = `search.domains` and each of `search.queries`, adding the
   current month/year. Vendors: keep only lab-automation sections (respect `include` /
   `exclude`). Agilent's chromatography or Beckman's centrifuge news is not lab automation.
3. Secondary sources: run when core sources are thin, to corroborate, and for
   funding/research/self-driving-lab news. Spend more effort where `weights.json` effects are
   positive and less where they are negative, but always check every core source.
4. Follow up every `missed_leads` entry from `docs/tuning.md` that has no item yet
   (`found_via: "missed-lead"`).
5. For each candidate, open the primary source. Keep it only if it was **published within the
   last 7 days** (a daily run looks back 7 days to catch late indexing; the 30-day dedupe stops
   repeats) and it is about lab automation.

Record what you checked in `data/runs/D.json`:
```json
{"date": "D", "sources_checked": [{"id": "slas", "method": "site-search", "queries": ["..."], "candidates": 3, "kept": 1}],
 "fetch_failed": ["hamilton"], "notes": "anything odd"}
```
`method` is `feed` (fetch_sources worked), `site-search`, or `feed+site-search`.

## 2. Write items (daily)
Append to `data/items/D.jsonl`, one JSON object per line. Ids are `LAN-<D as YYYYMMDD>-NN`,
continuing from the highest NN already in the file.

```json
{"id": "LAN-20261102-01", "found": "2026-11-02", "published": "2026-10-30",
 "title": "Plain, specific headline (who did what)",
 "summary": "2-4 sentences of fact only, each fact traceable to a ref.",
 "claims": [{"text": "Series B of $40M led by X", "ref": 0}],
 "why_it_matters": "1-2 sentences of analysis for a lab-automation practitioner. Mark speculation.",
 "segment": "liquid-handling", "type": "partnership", "companies": ["Hamilton", "Cerillo"],
 "source_id": "hamilton", "found_via": "site-search", "query": "the exact query that found it",
 "refs": [{"url": "https://...", "title": "Hamilton press release", "kind": "primary", "accessed": "2026-11-02"},
          {"url": "https://...", "title": "SelectScience", "kind": "secondary", "accessed": "2026-11-02"}],
 "relevance": 4, "status": "include"}
```
- `segment` and `type` come from `config/watchlist.yaml`. `source_id` is a sources.yaml id, or `web`.
- `relevance` is your honest 1-5 guess of how much the user will care (5 = must-know). It is
  compared against the user's ratings to calibrate you, so don't inflate it.
- `status`: `include`, `hold` (worth tracking but not brief-worthy) or `drop` (with a
  `drop_reason`). Dropped items stay in the file so dedupe and learning can see them.
- **Every fact needs a ref. No link, no claim.** Primary sources first (press release, paper,
  organiser page). Put numbers in `claims`, each pointing to its ref.
- Then run `uv run validate.py D` and fix every problem.

## 3. Verify (every run, never skipped)
Spawn the **verifier** agent (`.claude/agents/verifier.md`) with the prompt:
"Verify data/items/D.jsonl (window: last 7 days, today is D)". It works in its own context and
writes `data/verify/D.jsonl`. When it returns:
- apply any `corrections` it gave to the items (edit the item, keep the id)
- set `status: "drop"` with a `drop_reason` on anything `contradicted`
- run `uv run validate.py D` again

## 4. Weekly brief (Mondays, or `weekly`)
1. Harvest ratings: if `/home/user/myday` is not present, call add_repo for `bum94587/myday`
   and clone it there (shallow). Then
   `uv run harvest_ratings.py --from /home/user/myday/projects/labautonews/docs/news --from docs/news`,
   then `uv run learn_weights.py`.
2. Write `data/editorial/D.md`, the only free-written part:
   ```
   ## TL;DR
   - 3-5 bullets, each ending with the story's source link(s)
   ## Signals to watch (analysis)
   - patterns across this week's (and earlier) items, each linked; label speculation
   ```
3. `uv run build_brief.py --end D`. This renders `docs/news/D_lab-automation-weekly.md`. Read it
   once from top to bottom. If something is wrong, fix the item or verdict data and rebuild
   (never hand-edit the rendered brief).

## 5. Commit and push (every run)
`git add data docs config && git commit -m "research: daily D"` (or `"report: weekly D"`), then
push the session branch. myday's `tools/pull_news.py` finds briefs on any `claude/*` branch.
Do not commit to myday.

## Deep dive (`deepdive "<topic>"`)
Same rules on sources and verification, no date window (lead with the last 12 months).
Write items as above with `segment` set appropriately. Write the analysis to
`docs/news/D_deepdive-<slug>.md` with numbered references to every source, run the verifier
on the items, and include its badges/notes for each claim-bearing section.
