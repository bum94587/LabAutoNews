"""Render the weekly brief from the week's items, verdicts, runs and editorial.

    uv run build_brief.py                    # week ending today (7 days)
    uv run build_brief.py --end 2026-11-02   # week ending that date
    uv run build_brief.py --days 14          # wider window (e.g. the first brief)

Writes `docs/news/YYYY-MM-DD_lab-automation-weekly.md` (or `-daily.md` with `--kind daily`), which myday's `tools/pull_news.py`
copies into the viewer. Layout, quick read first:

1. TL;DR (editorial), then one short block per story: badge, headline, 1-2 sentences, a
   one-line "why", up to three source links, and a rating line
2. Signals to watch (editorial)
3. Filtered out: items left out and candidates screened out during research, with reasons
4. Scope: every site with what it produced, every watched company with its story count,
   and companies seen that aren't on the watchlist yet
5. Details: key numbers, the verifier's note and every source, per story
6. Feedback lines: Brief (rating / Missed / Notes) and Scope (Add / Remove)

Items the verifier marked `contradicted`, and items with status `drop` or `hold`, are not
stories but are listed under Filtered out, so nothing disappears silently. A rebuild keeps
any feedback line that was already filled in.
"""

from __future__ import annotations

import argparse
import json
import re
from datetime import date, timedelta

from labnews.common import (EDITORIAL_DIR, NEWS_DIR, RUNS_DIR, SCOPE_LOG, all_items, all_verdicts,
                            load_weights, predicted_score, read_jsonl, sources, watchlist)

FACT = {"verified": "✅", "partial": "🟡", "unverified": "⚪", "contradicted": "❌"}
SCI = {"questionable": "⚠️", "unsupported": "⛔"}
LEGEND = ("🎯 your field (DMPK/ADME) · ✅ verified · 🟡 partly verified · ⚪ unverified · ⏳ not yet checked · "
          "⚠️ technical claim questionable · ⛔ technical claim unsupported")
FOCUS_SEGMENT = "dmpk-adme"


def is_paper(it: dict) -> bool:
    return it["type"] == "research" and any(r["kind"] == "paper" for r in it["refs"])


def focus_mark(it: dict) -> str:
    return "🎯 " if it["segment"] == FOCUS_SEGMENT else ""
MAX_INLINE_SOURCES = 3
FEEDBACK_RE = re.compile(r"`(LAN-[A-Z]?\d{8}(?:-\d{2,3})?)`\s*$")


def in_window(d: str, start: date, end: date) -> bool:
    try:
        return start <= date.fromisoformat(d[:10]) <= end
    except ValueError:
        return False


def badge(v: dict | None) -> str:
    if not v:
        return "⏳"
    return FACT.get(v["facts"], "") + SCI.get(v["science"], "")


def short_date(d: str) -> str:
    try:
        return date.fromisoformat(d).strftime("%-d %b")
    except (ValueError, TypeError):
        return d or "date unknown"


def link(r: dict) -> str:
    return f"[{r.get('title') or r['url']}]({r['url']})"


def render_story(n: str, it: dict, v: dict | None) -> str:
    meta = " · ".join(filter(None, [badge(v), it["type"], ", ".join(it.get("companies", [])[:3]),
                                    short_date(it["published"])]))
    srcs = " · ".join(link(r) for r in it["refs"][:MAX_INLINE_SOURCES])
    more = len(it["refs"]) - MAX_INLINE_SOURCES
    if more > 0:
        srcs += f" · [+{more} in Details](#details)"
    body = it["summary"]
    if it.get("why_it_matters"):
        body += f" **Why:** {it['why_it_matters']}"
    return "\n".join([f"### {n}. {focus_mark(it)}{it['title']}", meta, "", body, "", f"Sources: {srcs}", "",
                      f"> **Rate:** _/5 · **Tags:** _ · `{it['id']}`", ""])


def render_paper(n: str, it: dict, v: dict | None) -> str:
    meta = " · ".join(filter(None, [f"*{it['journal']}*" if it.get("journal") else "", it.get("authors", ""),
                                    short_date(it["published"]), badge(v)]))
    body = it["summary"] + (f" **Why:** {it['why_it_matters']}" if it.get("why_it_matters") else "")
    srcs = " · ".join(link(r) for r in it["refs"][:MAX_INLINE_SOURCES])
    return "\n".join([f"### {n}. {focus_mark(it)}{it['title']}", meta, "", body, "", srcs, "",
                      f"> **Rate:** _/5 · **Tags:** _ · `{it['id']}`", ""])


def render_details(n: str, it: dict, v: dict | None) -> str:
    lines = [f"**{n}. {it['title']}** (`{it['id']}`, {it['segment']}, published {it['published']})"]
    for c in it.get("claims", []):
        lines.append(f"- {c['text']} [[{c['ref'] + 1}]]({it['refs'][c['ref']]['url']})")
    if v:
        lines.append(f"- Verifier: facts {v['facts']}, science {v['science']}. {v.get('notes', '')}")
    else:
        lines.append("- Verifier: not yet checked")
    lines.append("- Sources: " + " · ".join(f"[{i + 1}] {link(r)} ({r['kind']})" for i, r in enumerate(it["refs"])))
    return "\n".join(lines) + "\n"


def first_sentence(text: str, max_words: int = 25) -> str:
    sent = re.split(r"(?<=[.!?])\s", text.strip(), maxsplit=1)[0]
    words = sent.split()
    return " ".join(words[:max_words]) + ("…" if len(words) > max_words else "")


GROUP_LABELS = {"core_vendors": "Core vendors", "incumbents": "Incumbents", "open_source": "Open source",
                "growth": "Growth", "ai_native": "AI-native"}


def runs_in(start: date, end: date) -> list[dict]:
    return [json.loads(p.read_text(encoding="utf-8")) for p in sorted(RUNS_DIR.glob("*.json"))
            if in_window(p.stem, start, end)]


def scope_section(runs: list[dict], week: list[dict], shown: list[dict]) -> list[str]:
    stats: dict[str, dict] = {}
    for run in runs:
        for c in run.get("sources_checked", []):
            s = stats.setdefault(c["id"], {"methods": set(), "candidates": 0})
            s["methods"].add(c.get("method", "?"))
            s["candidates"] += int(c.get("candidates", 0) or 0)
    stories = {}
    for it in shown:
        stories[it["source_id"]] = stories.get(it["source_id"], 0) + 1
    out = ["## Scope: sites and companies", "",
           "What each site and company produced in this window. To add or remove one, fill in the "
           "**Scope** line at the very bottom; the next run applies it to `config/`.", "",
           "| Site | Tier | Cadence | Checked via | Candidates | Stories |", "|---|---|---|---|---:|---:|"]
    for s in sources():
        st = stats.get(s["id"])
        how = ", ".join(sorted(st["methods"])) if st else "**not checked**"
        home = s.get("home")
        name = f"[{s['name']}]({home})" if home else s["name"]
        out.append(f"| {name} | {s.get('tier', '')} | {s.get('cadence', 'daily')} | {how} | "
                   f"{st['candidates'] if st else 0} | {stories.get(s['id'], 0)} |")
    if stories.get("web"):
        out.append(f"| Open web search (not a listed site) | — | daily | web-search | — | {stories['web']} |")

    wl = watchlist()["companies"]
    count: dict[str, int] = {}
    for it in shown:
        for c in it.get("companies", []):
            count[c] = count.get(c, 0) + 1
    watched = {c.lower() for group in wl.values() for c in group}
    site_names = " ".join(f"{s['id']} {s['name']}" for s in sources()).lower()
    out += ["", "**Companies watched** (stories this window):", ""]
    for group, names in wl.items():
        out.append(f"- {GROUP_LABELS.get(group, group.replace('_', ' ').capitalize())}: " + " · ".join(f"{c} {count.get(c, 0)}" for c in names))
    seen_new = sorted({c for it in week if it["status"] != "drop" for c in it.get("companies", [])
                       if c.lower() not in watched and c.lower() not in site_names})
    if seen_new:
        out += ["", "**In the news, not on the watchlist** (add?): " + " · ".join(seen_new)]
    return out


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--end", default=date.today().isoformat())
    ap.add_argument("--days", type=int, default=None, help="window length (default 7 weekly, 1 daily)")
    ap.add_argument("--kind", choices=["weekly", "daily"], default="weekly",
                    help="daily = that day's items only, no editorial (deep mode)")
    args = ap.parse_args()
    if args.days is None:
        args.days = 1 if args.kind == "daily" else 7
    end = date.fromisoformat(args.end)
    start = end - timedelta(days=args.days - 1)

    verdicts, weights = all_verdicts(), load_weights()
    week = [it for it in all_items() if in_window(it["found"], start, end)]
    shown, held = [], []
    for it in week:
        v = verdicts.get(it["id"])
        if it["status"] == "include" and not (v and v["facts"] == "contradicted"):
            shown.append((predicted_score(it, v, weights), it, v))
        else:
            held.append((it, v))
    shown.sort(key=lambda t: t[1]["published"] or "", reverse=True)  # newest first within a score
    shown.sort(key=lambda t: -t[0])
    runs = runs_in(start, end)

    ed_text = ""
    ed = EDITORIAL_DIR / f"{end.isoformat()}.md"
    if ed.exists() and args.kind == "weekly":
        ed_text = ed.read_text(encoding="utf-8").strip()
    top, _, signals = ed_text.partition("## Signals")

    tag = end.strftime('%-d %b %Y') if start == end else f"{start.strftime('%-d %b')} – {end.strftime('%-d %b %Y')}"
    out = [f"# Lab automation {args.kind}, {end.strftime('%-d %b %Y')}", "",
           f"{tag} · {sum(not is_paper(t[1]) for t in shown)} stories · {sum(is_paper(t[1]) for t in shown)} papers · "
           f"{len(held)} filtered out · {LEGEND}", ""]
    if top.strip():
        out += [top.strip(), ""]

    news = [t for t in shown if not is_paper(t[1])]
    papers = [t for t in shown if is_paper(t[1])]
    news.sort(key=lambda t: t[1]["segment"] != FOCUS_SEGMENT)    # stable: your field first, then score
    papers.sort(key=lambda t: t[1]["segment"] != FOCUS_SEGMENT)
    numbered = [(str(n), it, v) for n, (_, it, v) in enumerate(news, 1)] + \
               [(f"P{n}", it, v) for n, (_, it, v) in enumerate(papers, 1)]

    out += ["## Stories", ""]
    for n, it, v in numbered:
        if not n.startswith("P"):
            out.append(render_story(n, it, v))
    if not news:
        out += ["No news stories this week.", ""]

    if papers:
        out += ["## From the journals", "",
                "SLAS Discovery, SLAS Technology, HardwareX, PubMed and preprints; your field first.", ""]
        out += [render_paper(n, it, v) for n, it, v in numbered if n.startswith("P")]

    if signals.strip():
        out += ["## Signals" + signals.rstrip(), ""]

    out += ["## Filtered out", ""]
    if held:
        out += ["Found but not shown as stories:", ""]
        for it, v in held:
            why = it.get("drop_reason") or first_sentence((v or {}).get("notes", "")) or it["status"]
            state = it["status"] + (f", facts {v['facts']}" if v else "")
            out.append(f"- **{it['title']}** ({state}): {why} [{it['refs'][0].get('title') or 'source'}]({it['refs'][0]['url']})")
        out.append("")
    rejected = [r for run in runs for r in run.get("rejected", [])]
    if rejected:
        out += ["Screened out during research:", ""]
        for r in rejected:
            src = f" [{r.get('source_id', '')}]" if r.get("source_id") else ""
            target = f"[{r['title']}]({r['url']})" if r.get("url") else r["title"]
            out.append(f"- {target}{src}: {r.get('reason', '')}")
        out.append("")
    if not held and not rejected:
        out += ["Nothing was filtered out.", ""]

    applied = [s for s in read_jsonl(SCOPE_LOG) if in_window(s.get("applied_at", ""), start, end)]
    if applied:
        out += ["## Scope changes applied", ""] + [f"- {s['summary']}" for s in applied] + [""]

    out += scope_section(runs, week, [it for _, it, _ in shown]) + [""]

    out += ['## Details <a id="details"></a>', ""]
    for n, it, v in numbered:
        out.append(render_details(n, it, v))

    out += ["## Feedback", "",
            f"> **Brief:** _/5 · **Missed:** _ · **Notes:** _ · `LAN-{'W' if args.kind == 'weekly' else 'B'}{end.strftime('%Y%m%d')}`", "",
            f"> **Scope:** Add: _ · Remove: _ · `LAN-S{end.strftime('%Y%m%d')}`", "",
            "Rate stories 1-5 (5 = must-know) and tag freely (`must-know`, `useful`, `meh`, `off-topic`, "
            "`wrong`, `unsound`, `hype`, `stale`, `dup`, `shallow`, `great`, `more`, `less`). **Missed**: "
            "anything this brief should have had. **Scope**: sites, companies or topics to add or remove, "
            "e.g. `Add: Opentrons blog, Automata · Remove: Telescope Innovations`.", ""]

    NEWS_DIR.mkdir(parents=True, exist_ok=True)
    path = NEWS_DIR / f"{end.isoformat()}_lab-automation-{args.kind}.md"
    text = "\n".join(out)
    if path.exists():  # a rebuild keeps any feedback line that differs from its blank template
        old = {m.group(1): line for line in path.read_text(encoding="utf-8").splitlines()
               if line.startswith("> ") and (m := FEEDBACK_RE.search(line))}
        new_lines = []
        for line in text.split("\n"):
            m = FEEDBACK_RE.search(line) if line.startswith("> ") else None
            new_lines.append(old.get(m.group(1), line) if m else line)
        text = "\n".join(new_lines)
    path.write_text(text, encoding="utf-8")
    print(f"Wrote {path.relative_to(NEWS_DIR.parents[1])}: {len(shown)} stories+papers, {len(held)} left out, "
          f"{len(rejected)} screened out.")


if __name__ == "__main__":
    main()
