# LabAutoNews

Daily research and a weekly, fully referenced brief on **laboratory automation**: liquid
handling, robotics and workcells, self-driving labs, orchestration software, clinical
automation, standards, and the business around them.

- **Every claim links to its source** so it can be checked again later.
- **An independent verifier agent** checks every item for facts (who, what, when, numbers)
  and for science/engineering soundness before it reaches a brief.
- **You rate stories where you read them** (the myday viewer). The ratings are harvested and
  learned from, so the research gets better at finding what you care about.

Main sources: SLAS, LRIG, ELRIG, Labautomation.io, PyLabRobot, and only the lab-automation
sections of Hamilton, Tecan, Agilent and Beckman Coulter, checked daily; and weekly, the journals
SLAS Discovery, SLAS Technology and HardwareX plus PubMed, with DMPK / ADME automation in drug
discovery as the primary lens (papers in that field are marked 🎯 and listed first). Trade press, wires and preprints are used to
corroborate and widen the net. See [`config/sources.yaml`](config/sources.yaml).

## How it runs

```
every day (scheduled cloud run)            Mondays, additionally
───────────────────────────────            ─────────────────────
sync_state.py   gather state from branches harvest_ratings.py  read your ratings from myday
fetch_sources.py headlines from sources    learn_weights.py    learn what's worth finding
site-restricted web searches               editorial (TL;DR, signals)
data/items/D.jsonl     ← research items    build_brief.py → docs/news/D_lab-automation-weekly.md
verifier agent → data/verify/D.jsonl
validate.py, commit, push                  myday "update" → pull_news.py → viewer
```

## Quickstart

This is a [`uv`](https://docs.astral.sh/uv/)-managed Python 3.12 project.

```bash
uv sync
uv run sync_state.py          # fold in data from the cloud runs' claude/* branches
uv run fetch_sources.py       # headline metadata from the configured sources
uv run validate.py            # schema check of items and verdicts
uv run build_brief.py         # render this week's brief into docs/news/
uv run harvest_ratings.py     # read ratings from ~/dev/myday/projects/labautonews/docs/news
uv run learn_weights.py       # update config/weights.json and docs/tuning.md
```

In Claude Code: `/deep-research daily`, `/deep-research weekly`, or
`/deep-research deepdive "self-driving labs in materials science"`.

## Rating

See [`docs/rating-guide.md`](docs/rating-guide.md). Short version: in a brief, change
`> **Rate:** _/5 · **Tags:** _` to `> **Rate:** 4/5 · **Tags:** must-know, more`. To change what is
watched, fill in the brief's last line, `> **Scope:** Add: … · Remove: …`; each brief's Scope
section lists every site and company with what it produced.

## Layout

| Path | What lives there |
|------|------------------|
| `config/sources.yaml` | Sources, their lab-automation sections, fetch + search settings |
| `config/watchlist.yaml` | Segments, item types, companies, keywords, events |
| `config/weights.json` | Learned from your ratings (generated) |
| `data/items/`, `data/verify/` | One JSONL per day: research items, and the verifier's verdicts |
| `data/runs/` | What each run checked and how (coverage) |
| `data/editorial/` | Weekly TL;DR and signals |
| `data/feedback/ratings.jsonl` | Your harvested ratings and scope requests |
| `data/feedback/scope_log.jsonl` | Scope requests applied to `config/` |
| `data/raw/` | Link registry and fetch log from `fetch_sources.py` |
| `docs/news/` | The weekly briefs (read in myday) |
| `docs/tuning.md` | What the learner found (generated) |
| `dialogs/` | Prompt/answer log of the project's setup and decisions |
| `.claude/skills/deep-research/` | The run playbook |
| `.claude/agents/verifier.md` | The fact and science/engineering checker |
