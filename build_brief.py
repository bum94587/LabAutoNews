"""Render the weekly brief from the week's items, verdicts and editorial.

    uv run build_brief.py                    # week ending today (7 days)
    uv run build_brief.py --end 2026-11-02   # week ending that date
    uv run build_brief.py --days 14          # wider window (e.g. the first brief)

Writes `docs/news/YYYY-MM-DD_lab-automation-weekly.md`, which myday's `tools/pull_news.py`
copies into the viewer. The brief is rendered (not hand-written) so that every item carries
its id, its verifier badges, numbered source links, and a rating line you can fill in from
the myday viewer's Edit mode:

    > **Rate:** _/5 · **Tags:** _ · `LAN-20261102-03`

Items the verifier marked `contradicted`, and items with status `drop`, are left out of the
stories but listed in the verification log at the bottom, so nothing disappears silently.
"""

from __future__ import annotations

import argparse
from datetime import date, timedelta

import json

from labnews.common import (BRIEF_ID_RE, EDITORIAL_DIR, ITEM_ID_RE, NEWS_DIR, RUNS_DIR, all_items, all_verdicts, load_weights,
                            predicted_score, sources, watchlist)

FACT_BADGE = {"verified": "✅ facts verified", "partial": "🟡 facts partly verified",
              "unverified": "⚪ facts not verified", "contradicted": "❌ facts contradicted"}
SCI_BADGE = {"sound": "🔬 science/engineering sound", "questionable": "⚠️ science/engineering questionable",
             "unsupported": "❌ claims unsupported", "na": ""}
TOP_N = 5


def in_window(d: str, start: date, end: date) -> bool:
    try:
        return start <= date.fromisoformat(d[:10]) <= end
    except ValueError:
        return False


def badges(v: dict | None) -> str:
    if not v:
        return "⏳ not yet verified"
    parts = [FACT_BADGE.get(v["facts"], ""), SCI_BADGE.get(v["science"], "")]
    return " · ".join(p for p in parts if p)


def render_item(it: dict, v: dict | None, segs: dict, n: int | None = None) -> str:
    refs = it["refs"]
    cites = " ".join(f"[{i + 1}]" for i in range(len(refs)))
    meta = " · ".join(filter(None, [
        it["type"].capitalize(), segs.get(it["segment"], it["segment"]),
        ", ".join(it.get("companies", [])), f"published {it['published'] or 'date unknown'}"]))
    head = f"### {f'{n}. ' if n else ''}{it['title']}"
    lines = [head, f"*{meta}*  ", badges(v), "", f"{it['summary']} {cites}"]
    if it.get("claims"):
        lines.append("")
        lines += [f"- {c['text']} [{c['ref'] + 1}]" for c in it["claims"]]
    if it.get("why_it_matters"):
        lines += ["", f"**Why it matters (analysis):** {it['why_it_matters']}"]
    if v and v.get("notes"):
        lines += ["", f"**Verifier:** {v['notes']}"]
    src = " · ".join(f"[{i + 1}] [{r.get('title') or r['url']}]({r['url']}) ({r['kind']})" for i, r in enumerate(refs))
    lines += ["", f"Sources: {src}", "", f"> **Rate:** _/5 · **Tags:** _ · `{it['id']}`", ""]
    return "\n".join(lines)


def coverage(start: date, end: date) -> list[str]:
    names = {s["id"]: s["name"] for s in sources()}
    seen: dict[str, set[str]] = {}
    for p in sorted(RUNS_DIR.glob("*.json")):
        if not in_window(p.stem, start, end):
            continue
        run = json.loads(p.read_text(encoding="utf-8"))
        for c in run.get("sources_checked", []):
            seen.setdefault(c["id"], set()).add(c.get("method", "?"))
    core = [s["id"] for s in sources() if s.get("tier") == "core"]
    out = []
    for sid in core + [k for k in seen if k not in core]:
        how = ", ".join(sorted(seen.get(sid, []))) or "**not checked this week**"
        out.append(f"- {names.get(sid, sid)}: {how}")
    return out


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--end", default=date.today().isoformat())
    ap.add_argument("--days", type=int, default=7)
    args = ap.parse_args()
    end = date.fromisoformat(args.end)
    start = end - timedelta(days=args.days - 1)

    segs = watchlist()["segments"]
    verdicts, weights = all_verdicts(), load_weights()
    week = [it for it in all_items() if in_window(it["found"], start, end)]
    shown, held = [], []
    for it in week:
        v = verdicts.get(it["id"])
        if it["status"] == "drop" or (v and v["facts"] == "contradicted"):
            held.append((it, v))
        elif it["status"] == "include":
            shown.append((predicted_score(it, v, weights), it, v))
        else:
            held.append((it, v))
    shown.sort(key=lambda t: t[1]["published"] or "", reverse=True)  # newest first within a score
    shown.sort(key=lambda t: -t[0])

    brief_id = f"LAN-W{end.strftime('%Y%m%d')}"
    out = [f"# Lab automation weekly, {end.strftime('%-d %b %Y')}", "",
           f"Week of {start.isoformat()} to {end.isoformat()}. {len(shown)} stories from "
           f"{len(week)} items found by the daily research runs. Every story links to its sources; "
           "badges show what the independent verifier agent could confirm. Fill in the "
           "**Rate** lines in the myday viewer (Edit) so the next runs learn what you want.", ""]

    ed = EDITORIAL_DIR / f"{end.isoformat()}.md"
    if ed.exists():
        out += [ed.read_text(encoding="utf-8").strip(), ""]

    out += ["## Top stories", ""]
    for n, (_, it, v) in enumerate(shown[:TOP_N], 1):
        out.append(render_item(it, v, segs, n))

    rest = shown[TOP_N:]
    if rest:
        out += ["## More this week", ""]
        for seg_slug, seg_name in segs.items():
            group = [(it, v) for _, it, v in rest if it["segment"] == seg_slug]
            if group:
                out += [f"#### {seg_name}", ""]
                out += [render_item(it, v, segs) for it, v in group]

    out += ["## Verification log", ""]
    counts: dict[str, int] = {}
    for _, it, v in shown:
        key = v["facts"] if v else "not yet verified"
        counts[key] = counts.get(key, 0) + 1
    out.append("Shown: " + (", ".join(f"{k} {n}" for k, n in sorted(counts.items())) or "none") + ".")
    if held:
        out += ["", "Left out:"]
        for it, v in held:
            why = (v or {}).get("notes") or it.get("drop_reason") or it["status"]
            out.append(f"- {it['title']} (`{it['id']}`, {it['status']}"
                       f"{', ' + v['facts'] if v else ''}): {why} — [{it['refs'][0].get('title') or 'source'}]({it['refs'][0]['url']})")
    out += ["", "## Coverage", ""] + coverage(start, end)
    out += ["", "## Your feedback on this brief", "",
            f"> **Brief:** _/5 · **Missed:** _ · **Notes:** _ · `{brief_id}`", "",
            "Rate 1-5 (5 = must-know). Tags are free text, comma-separated; the usual ones are "
            "`must-know`, `useful`, `meh`, `off-topic`, `wrong`, `unsound`, `hype`, `stale`, `dup`, "
            "`shallow`, `great`, `more`, `less`. **Missed** = anything you saw elsewhere that this "
            "brief should have had (a link or a few words); the next run follows it up.", ""]

    NEWS_DIR.mkdir(parents=True, exist_ok=True)
    path = NEWS_DIR / f"{end.isoformat()}_lab-automation-weekly.md"
    text = "\n".join(out)
    if path.exists():  # a rebuild keeps any rating lines already filled in
        filled = {m.group(0): line for line in path.read_text(encoding="utf-8").splitlines()
                  if line.startswith("> ") and "_/5" not in line
                  and (m := ITEM_ID_RE.search(line) or BRIEF_ID_RE.search(line))}
        text = "\n".join(next((filled[i] for i in filled if line.startswith("> ") and f"`{i}`" in line), line)
                         for line in text.split("\n"))
    path.write_text(text, encoding="utf-8")
    print(f"Wrote {path.relative_to(NEWS_DIR.parents[1])}: {len(shown)} stories, {len(held)} left out.")


if __name__ == "__main__":
    main()
