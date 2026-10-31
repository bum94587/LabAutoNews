"""Fetch the latest headlines from the sources in config/sources.yaml.

For each source with a `fetch:` block, read its listing (Discourse JSON, RSS, or an HTML page
of links), keep only lab-automation-relevant links for vendors (`include` / `exclude`), and
record every link not seen before in `data/raw/links.jsonl` with today's date as first_seen.
The research run then opens the new links as candidates.

Metadata only (titles, links, dates, short feed summaries); never article bodies.
Every source is fetched inside its own try/except, so one blocked or broken site never kills
the run; the outcome per source goes to `data/raw/fetch_log.jsonl`. A blocked site is not an
error: the research run covers it with site-restricted web search instead (see the skill).

    uv run fetch_sources.py              # fetch all core sources
    uv run fetch_sources.py --all        # also secondary sources that have a fetch block
    uv run fetch_sources.py --only slas  # one source
    uv run fetch_sources.py --new        # just print links first seen today (no fetching)
"""

from __future__ import annotations

import argparse
import re
from urllib.parse import urljoin

import feedparser
import requests
from bs4 import BeautifulSoup

from labnews.common import FETCH_LOG, LINKS, append_jsonl, now_utc, read_jsonl, sources, today

HEADERS = {
    "User-Agent": "Mozilla/5.0 (LabAutoNews research; headline metadata only)",
    "Accept": "text/html,application/json,application/rss+xml;q=0.9,*/*;q=0.5",
}
TIMEOUT = 25


def get(url: str) -> requests.Response:
    r = requests.get(url, headers=HEADERS, timeout=TIMEOUT)
    r.raise_for_status()
    return r


def fetch_discourse(cfg: dict) -> list[dict]:
    data = get(cfg["url"]).json()
    base = cfg["url"].split("/latest")[0]
    out = []
    for t in data.get("topic_list", {}).get("topics", []):
        out.append({
            "title": t.get("title", ""),
            "url": f"{base}/t/{t.get('slug')}/{t.get('id')}",
            "published": (t.get("created_at") or "")[:10],
            "summary": f"{t.get('posts_count', 0)} posts, {t.get('views', 0)} views, last activity {(t.get('last_posted_at') or '')[:10]}",
        })
    return out


def fetch_rss(cfg: dict) -> list[dict]:
    feed = feedparser.parse(get(cfg["url"]).content)
    out = []
    for e in feed.entries:
        pub = ""
        if getattr(e, "published_parsed", None):
            pub = "%04d-%02d-%02d" % e.published_parsed[:3]
        out.append({"title": e.get("title", ""), "url": e.get("link", ""), "published": pub,
                    "summary": re.sub(r"<[^>]+>", "", e.get("summary", ""))[:300]})
    return out


def fetch_html_links(cfg: dict) -> list[dict]:
    soup = BeautifulSoup(get(cfg["url"]).text, "html.parser")
    pat = re.compile(cfg.get("link_pattern", "."))
    seen, out = set(), []
    for a in soup.find_all("a", href=True):
        url = urljoin(cfg["url"], a["href"]).split("#")[0]
        text = " ".join(a.get_text(" ").split())
        if not text or len(text) < 8 or url in seen or not pat.search(url):
            continue
        seen.add(url)
        # dates are often near the link; take the first YYYY-MM-DD / "Month D, YYYY" in the parent
        ctx = " ".join(a.parent.get_text(" ").split()) if a.parent else ""
        m = re.search(r"\b(20\d\d-\d\d-\d\d)\b", ctx)
        out.append({"title": text[:200], "url": url, "published": m.group(1) if m else "", "summary": ""})
    return out


FETCHERS = {"discourse": fetch_discourse, "rss": fetch_rss, "html-links": fetch_html_links}


def relevant(src: dict, row: dict) -> bool:
    text = f"{row['title']} {row['summary']} {row['url']}".lower()
    inc, exc = src.get("include"), src.get("exclude") or []
    if any(x.lower() in text for x in exc):
        return False
    return True if not inc else any(x.lower() in text for x in inc)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--all", action="store_true", help="include secondary sources")
    ap.add_argument("--only", help="fetch a single source id")
    ap.add_argument("--new", action="store_true", help="only list links first seen today")
    args = ap.parse_args()

    known = {r["url"]: r for r in read_jsonl(LINKS)}
    if args.new:
        for r in known.values():
            if r["first_seen"] == today():
                print(f"[{r['source_id']}] {r['published'] or '????-??-??'}  {r['title']}\n    {r['url']}")
        return

    log, new_rows = [], []
    for src in sources():
        if "fetch" not in src or (args.only and src["id"] != args.only):
            continue
        if not args.all and not args.only and src.get("tier") != "core":
            continue
        cfg = src["fetch"]
        entry = {"at": now_utc(), "source_id": src["id"], "url": cfg["url"]}
        try:
            rows = FETCHERS[cfg["type"]](cfg)
            kept = [r for r in rows if relevant(src, r)]
            fresh = [r for r in kept if r["url"] not in known]
            for r in fresh:
                rec = {"first_seen": today(), "source_id": src["id"], **r}
                known[r["url"]] = rec
                new_rows.append(rec)
            entry.update(status="ok", listed=len(rows), relevant=len(kept), new=len(fresh))
            print(f"ok      {src['id']:<18} {len(rows):>3} listed, {len(kept):>3} relevant, {len(fresh):>3} new")
        except Exception as e:  # noqa: BLE001 - a dead source must never stop the run
            msg = f"{type(e).__name__}: {e}"[:200]
            entry.update(status="failed", error=msg)
            print(f"FAILED  {src['id']:<18} {msg}")
        log.append(entry)

    append_jsonl(LINKS, new_rows)
    append_jsonl(FETCH_LOG, log)
    failed = [e["source_id"] for e in log if e["status"] != "ok"]
    print(f"\n{len(new_rows)} new link(s) recorded in {LINKS.relative_to(LINKS.parents[2])}.")
    if failed:
        print("Not fetched (cover these with site-restricted WebSearch): " + ", ".join(failed))


if __name__ == "__main__":
    main()
