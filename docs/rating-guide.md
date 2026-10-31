# Rating the briefs

Every story in a weekly brief ends with a line like

> **Rate:** _/5 · **Tags:** _ · `LAN-20261102-03`

In the myday viewer, switch on **Edit**, replace the `_`s, save, and commit/push myday as usual:

> **Rate:** 4/5 · **Tags:** must-know, more · `LAN-20261102-03`

Leave the id alone. Rate as many or as few stories as you like; unrated ones are just skipped.
The Monday run harvests the ratings from myday (`harvest_ratings.py`) and re-learns
(`learn_weights.py`). Changing a rating later replaces the old one.

## The scale

| Rating | Meaning |
|---:|---|
| 5 | Must-know: would be annoyed to miss it |
| 4 | Useful, glad it was there |
| 3 | Fine, but wouldn't miss it |
| 2 | Marginal: barely relevant or too thin |
| 1 | Shouldn't be here |

## Tags (comma-separated, free text, these are the ones the learner looks for)

| Tag | Use when |
|---|---|
| `must-know`, `useful`, `meh`, `off-topic` | how relevant it is |
| `wrong` | a fact is wrong (also checks the verifier: a `wrong` that the verifier passed is logged as a miss) |
| `unsound` | the science/engineering claim doesn't hold up |
| `hype` | marketing dressed as news |
| `stale` | old news re-reported |
| `dup` | already covered |
| `shallow` | right topic, not enough substance |
| `great` | analysis or find you especially liked |
| `more` / `less` | steer: want more / less like this (source, segment, company, type) |

## The whole brief

At the bottom:

> **Brief:** 3/5 · **Missed:** Opentrons Flex price cut https://... · **Notes:** too vendor-heavy · `LAN-W20261102`

**Missed** is the most valuable field: anything you saw elsewhere that the brief should have
had. The next run follows each one up, and the gap tells the learner where coverage is weak.

## Changing the scope (sites, companies)

Near the bottom of every brief, the **Scope** section lists every site with what it produced
this week (candidates found, stories shown) and every watched company with its story count,
plus companies that were in the news but aren't on the watchlist. To change what is watched,
fill in the last line:

> **Scope:** Add: Opentrons blog, Automata · Remove: Telescope Innovations · `LAN-S20261102`

Free text. Name a site, a company, or a topic. The next run harvests it, edits
`config/sources.yaml` / `config/watchlist.yaml`, logs the change in
`data/feedback/scope_log.jsonl`, and the following brief lists it under "Scope changes applied".
Say "core" if a new site should be checked on every run (otherwise it's secondary).

## What happens with it

`learn_weights.py` computes, for every source, segment, item type, search method, domain,
company and verifier verdict, how your ratings compare with your average (shrunk toward the
average until there are enough ratings). The research run spends more effort where that's
positive, and `build_brief.py` orders stories by the researcher's relevance guess nudged by
these effects. `docs/tuning.md` shows the current state, plus calibration: how well the
researcher's guesses track your ratings, and where the verifier missed something you tagged
`wrong` or `unsound`.
