"""Fetch the latest headlines from the sources in config/sources.yaml.

For each source with a `fetch:` block (one, or a list), read its listing (Discourse JSON, RSS,
an HTML page of links, a public git repo's recent merged PRs and release tags, a journal's new
articles via Crossref, or PubMed queries), keep only lab-automation-relevant links for vendors (`include` / `exclude`), and
record every link not seen before in `data/raw/links.jsonl` with today's date as first_seen.
The research run then opens the new links as candidates.

Metadata only (titles, links, dates, short feed summaries); never article bodies.
Every source is fetched inside its own try/except, so one blocked or broken site never kills
the run; the outcome per source goes to `data/raw/fetch_log.jsonl`. A blocked site is not an
error: the research run covers it with site-restricted web search instead (see the skill).

    uv run fetch_sources.py              # fetch all daily core sources
    uv run fetch_sources.py --weekly     # also the weekly ones (journals, PubMed): Mondays
    uv run fetch_sources.py --all        # also secondary sources that have a fetch block
    uv run fetch_sources.py --only slas  # one source
    uv run fetch_sources.py --new        # just print links first seen today (no fetching)
"""

from __future__ import annotations

import argparse
import re
import subprocess
import tempfile
from datetime import date, timedelta
from urllib.parse import urljoin, urlparse

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
    u = urlparse(cfg["url"])
    base = f"{u.scheme}://{u.netloc}"
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


def fetch_git_log(cfg: dict) -> list[dict]:
    """Merged PRs and release tags of a public git repo over the last `days` (default 14).

    Uses git itself (a shallow, blob-less clone into a temp dir), which works where the
    GitHub web/API endpoints are blocked. Only commits that reference a PR `(#123)` are kept.
    """
    repo = cfg["url"].removesuffix(".git")
    since = (date.today() - timedelta(days=int(cfg.get("days", 14)))).isoformat()
    with tempfile.TemporaryDirectory() as tmp:
        subprocess.run(["git", "clone", "-q", "--bare", "--filter=blob:none", f"--shallow-since={since}",
                        repo, tmp], check=True, capture_output=True, timeout=180)
        log = subprocess.run(["git", "-C", tmp, "log", f"--since={since}", "--format=%H%x09%ad%x09%s",
                              "--date=short"], check=True, capture_output=True, text=True).stdout
        tags = subprocess.run(["git", "-C", tmp, "for-each-ref", "refs/tags", "--format=%(refname:short)%09%(creatordate:short)"],
                              check=True, capture_output=True, text=True).stdout
    out = []
    for line in filter(None, log.splitlines()):
        sha, day, subject = line.split("\t", 2)
        m = re.search(r"\(#(\d+)\)\s*$", subject)
        if not m:
            continue
        out.append({"title": subject, "url": f"{repo}/pull/{m.group(1)}", "published": day,
                    "summary": f"merged PR, commit {sha[:7]}"})
    for line in filter(None, tags.splitlines()):
        tag, day = line.split("\t")
        if day >= since:
            out.append({"title": f"Release {tag}", "url": f"{repo}/releases/tag/{tag}", "published": day,
                        "summary": "release tag"})
    return out


def fetch_crossref_journal(cfg: dict) -> list[dict]:
    """Articles a journal published online in the last `days` (default 14), via Crossref by ISSN."""
    since = (date.today() - timedelta(days=int(cfg.get("days", 14)))).isoformat()
    url = (f"https://api.crossref.org/journals/{cfg['issn']}/works?rows=100&sort=published&order=desc"
           f"&filter=from-online-pub-date:{since}&select=DOI,title,published-online,published,abstract,author")
    items = get(url).json().get("message", {}).get("items", [])
    out = []
    for w in items:
        parts = (w.get("published-online") or w.get("published") or {}).get("date-parts", [[]])[0]
        pub = "-".join(f"{p:02d}" if i else str(p) for i, p in enumerate(parts))
        authors = w.get("author") or []
        first = authors[0].get("family", "") if authors else ""
        out.append({"title": " ".join((w.get("title") or [""])[0].split()), "url": f"https://doi.org/{w['DOI']}",
                    "published": pub, "summary": (f"{first} et al. " if first else "") +
                    re.sub(r"<[^>]+>", "", w.get("abstract", ""))[:280]})
    return out


def fetch_pubmed(cfg: dict) -> list[dict]:
    """PubMed records added in the last `days` (default 14) for each query, via NCBI E-utilities."""
    base = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
    days = int(cfg.get("days", 14))
    ids: list[str] = []
    for q in cfg["queries"]:
        r = requests.get(f"{base}/esearch.fcgi", headers=HEADERS, timeout=TIMEOUT, params={
            "db": "pubmed", "term": q, "datetype": "edat", "reldate": days, "retmax": 100,
            "retmode": "json", "tool": "LabAutoNews"})
        r.raise_for_status()
        ids += [i for i in r.json()["esearchresult"]["idlist"] if i not in ids]
    if not ids:
        return []
    r = requests.get(f"{base}/esummary.fcgi", headers=HEADERS, timeout=TIMEOUT, params={
        "db": "pubmed", "id": ",".join(ids[:200]), "retmode": "json", "tool": "LabAutoNews"})
    r.raise_for_status()
    res = r.json()["result"]
    out = []
    for pmid in res.get("uids", []):
        d = res[pmid]
        first = (d.get("authors") or [{}])[0].get("name", "")
        out.append({"title": d.get("title", ""), "url": f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/",
                    "published": d.get("sortpubdate", "")[:10].replace("/", "-"),
                    "summary": f"{first} et al., {d.get('source', '')} {d.get('elocationid', '')}".strip()})
    return out


FETCHERS = {"discourse": fetch_discourse, "rss": fetch_rss, "html-links": fetch_html_links,
            "git-log": fetch_git_log, "crossref-journal": fetch_crossref_journal, "pubmed": fetch_pubmed}


def relevant(src: dict, row: dict) -> bool:
    text = f"{row['title']} {row['summary']} {row['url']}".lower()
    inc, exc = src.get("include"), src.get("exclude") or []
    if any(x.lower() in text for x in exc):
        return False
    return True if not inc else any(x.lower() in text for x in inc)


def fetch_one(src: dict, cfg: dict, known: dict, new_rows: list) -> dict:
    entry = {"at": now_utc(), "source_id": src["id"], "url": cfg.get("url") or cfg.get("issn") or cfg["type"]}
    try:
        rows = FETCHERS[cfg["type"]](cfg)
        kept = [r for r in rows if relevant(src, r)]
        fresh = [r for r in kept if r["url"] not in known]
        for r in fresh:
            rec = {"first_seen": today(), "source_id": src["id"], **r}
            known[r["url"]] = rec
            new_rows.append(rec)
        entry.update(status="ok", listed=len(rows), relevant=len(kept), new=len(fresh))
        print(f"ok      {src['id']:<18} {len(rows):>3} listed, {len(kept):>3} relevant, {len(fresh):>3} new  ({cfg['type']})")
    except Exception as e:  # noqa: BLE001 - a dead source must never stop the run
        msg = f"{type(e).__name__}: {e}"[:200]
        entry.update(status="failed", error=msg)
        print(f"FAILED  {src['id']:<18} {msg}")
    return entry


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--all", action="store_true", help="include secondary sources")
    ap.add_argument("--only", help="fetch a single source id")
    ap.add_argument("--weekly", action="store_true",
                    help="also fetch sources with cadence: weekly (journals, PubMed); the Monday run uses this")
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
        if src.get("cadence") == "weekly" and not (args.weekly or args.only):
            continue
        for cfg in (src["fetch"] if isinstance(src["fetch"], list) else [src["fetch"]]):
            log.append(fetch_one(src, cfg, known, new_rows))

    append_jsonl(LINKS, new_rows)
    append_jsonl(FETCH_LOG, log)
    failed = [e["source_id"] for e in log if e["status"] != "ok"]
    print(f"\n{len(new_rows)} new link(s) recorded in {LINKS.relative_to(LINKS.parents[2])}.")
    if failed:
        print("Not fetched (cover these with site-restricted WebSearch): " + ", ".join(failed))


if __name__ == "__main__":
    main()
