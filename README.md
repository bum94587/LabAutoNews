# LabAutoNews

Recurring deep research on **laboratory automation**: robotics, liquid handling,
self-driving labs / AI scientists, lab orchestration software, cloud labs, and
the companies, funding, papers and standards behind them.

Research runs are done by Claude Code (see [`CLAUDE.md`](CLAUDE.md) and the
`/deep-research` skill in `.claude/skills/deep-research/`). Every run writes a
dated, fully cited report and updates the running knowledge base so the next
run can skip what is already known.

## Layout

| Path | What lives there |
|------|------------------|
| `reports/YYYY/YYYY-MM-DD-<type>.md` | One report per run (`weekly`, `daily`, `deepdive-<topic>`) |
| `data/watchlist.yaml` | Companies, sources, topics and keywords to track |
| `data/seen.jsonl` | One line per story already covered (URL + date + headline) for dedupe |
| `.claude/skills/deep-research/SKILL.md` | The research playbook a run follows |

## Running a report manually

In a Claude Code session in this repo:

```
/deep-research weekly
/deep-research deepdive "self-driving labs in materials science"
```
