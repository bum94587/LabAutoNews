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
2. **Harvest feedback and apply scope changes.** If `/home/user/myday` is not present, call
   add_repo for `bum94587/myday` and clone it there (shallow). Run
   `uv run harvest_ratings.py --from /home/user/myday/projects/labautonews/docs/news --from docs/news`.
   Then, for every `kind: "scope"` record in `data/feedback/ratings.jsonl` whose
   `(id, harvested_at)` is not yet in `data/feedback/scope_log.jsonl`:
   - **Add** a site → a new entry in `config/sources.yaml` (tier `core` if the user says so,
     else `secondary`; find its news/blog section and give it `search.domains` + 2-3 queries,
     and a `fetch:` block if it has a feed). Add a company → the right group in
     `config/watchlist.yaml` (and its newsroom as a source if it has one worth checking).
   - **Remove** → delete the company from the watchlist, or the site from sources.yaml.
   - Append `{"id", "harvested_at", "request": {"add", "remove"}, "applied_at": "D",
     "summary": "one line of what changed", "changes": ["config/... : ..."]}` to
     `data/feedback/scope_log.jsonl`. If a request is ambiguous, apply the most sensible
     reading and say so in `summary` (the brief shows it under "Scope changes applied").
3. Read `config/sources.yaml`, `config/watchlist.yaml`, `config/weights.json` (if present) and
   `docs/tuning.md`: what the user has rated up or down, `steer.more` / `steer.less`, and
   `missed_leads`.
4. List the ids, titles and URLs of all items from the last 30 days (`data/items/`) so that you
   never add the same story twice. A genuinely new development in an old story is a new item
   that says what changed.

## 1. Collect (daily)
0. **Whose brief this is**: a DMPK / ADME scientist in drug discovery (`focus` in
   `config/watchlist.yaml`). DMPK/ADME automation is the primary lens (segment `dmpk-adme`,
   +1 relevance, listed first), but any lab automation relevant to pharma & biotech is in
   scope. Don't narrow too far; materials/physics SDL work stays in at relevance −1.
1. `uv run fetch_sources.py` (Mondays: `uv run fetch_sources.py --weekly`), then
   `uv run fetch_sources.py --new` for the links first seen today.
   Sources that fail are normal when the network policy blocks them. Cover those with search.
2. For **every core source due today** in `config/sources.yaml` (cadence `daily` every run;
   cadence `weekly` (SLAS Discovery, SLAS Technology, HardwareX, PubMed, preprints) on Mondays
   only, looking back 14 days), run its site-restricted searches:
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
6. Sources with a `notes:` field have special handling. Follow it (e.g. PyLabRobot is one
   weekly roll-up item built from `fetch_sources.py --new` PR titles, not one item per PR;
   roll-ups go in the run on the brief day, or in the first run after a release).

Record what you checked in `data/runs/D.json`:
```json
{"date": "D", "sources_checked": [{"id": "slas", "method": "site-search", "queries": ["..."], "candidates": 3, "kept": 1}],
 "fetch_failed": ["hamilton"],
 "rejected": [{"title": "Tecan half-year results", "url": "https://...", "source_id": "tecan", "reason": "financial results, not lab automation"}],
 "notes": "anything odd"}
```
`method` is `feed` (fetch_sources worked), `site-search`, or `feed+site-search`.
`rejected` lists every candidate you looked at and screened out *before* it became an item
(outside the window, not lab automation, duplicate, vendor's non-automation business) with a
short reason. The user reads this list, so be specific and keep each reason to a few words.

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
- **Write for a quick read** (validate.py enforces the limits): `title` ≤ 14 words, a plain
  "who did what"; `summary` ≤ 50 words, at most 2 sentences, facts only; `why_it_matters`
  ≤ 30 words, one sentence. Numbers, caveats and context go in `claims` (shown under Details).
- **Papers** (journal articles, preprints): `type: "research"`, refs of kind `paper` (DOI link
  first, then PubMed/journal page), plus `journal` and `authors` ("Smith et al.") fields.
  The summary is the finding in plain words; `why_it_matters` says what it means for a
  pharma/biotech lab. They render in the brief's "From the journals" section.
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
1. Ratings were harvested in step 0; now run `uv run learn_weights.py`.
2. Write `data/editorial/D.md`, the only free-written part. Keep it short:
   ```
   ## TL;DR
   - at most 4 bullets, each ≤ 20 words, each ending with one source link
   ## Signals to watch (analysis)
   - at most 3 bullets, each ≤ 30 words, linked; label speculation
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
