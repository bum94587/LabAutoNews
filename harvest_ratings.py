"""Collect your ratings and tags from the weekly briefs into data/feedback/ratings.jsonl.

You rate where you read: in the myday viewer, switch on Edit and fill in the line under a
story, e.g.

    > **Rate:** 4/5 · **Tags:** must-know, more · `LAN-20261102-03`
    > **Brief:** 3/5 · **Missed:** https://... Opentrons Flex price cut · **Notes:** too vendor-heavy · `LAN-W20261102`
    > **Scope:** Add: Opentrons blog, Automata · Remove: Telescope Innovations · `LAN-S20261102`

then commit/push myday as usual. This script reads those lines back. A line still showing
`_` is unrated and skipped. Re-rating later just replaces the earlier value (newest wins).
Scope lines become `kind: "scope"` records; the research run applies them to config/ and
logs what it changed in data/feedback/scope_log.jsonl.

    uv run harvest_ratings.py                          # ~/dev/myday copies + this repo's docs/news
    uv run harvest_ratings.py --from /path/to/news     # any folder(s) of briefs
    uv run harvest_ratings.py --dry-run

In the scheduled cloud run, myday is cloned to /home/user/myday and passed with --from.
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path

from labnews.common import (BRIEF_ID_RE, FEEDBACK, ITEM_ID_RE, NEWS_DIR, SCOPE_ID_RE, append_jsonl, now_utc,
                            ratings)

DEFAULT_MYDAY = Path.home() / "dev" / "myday" / "projects" / "labautonews" / "docs" / "news"

RATE_RE = re.compile(r"\*\*(?:Rate|Brief):\*\*\s*([1-5])\s*/\s*5")
FIELD_RE = r"\*\*{name}:\*\*\s*(.*?)\s*(?:·|`|$)"


def field(line: str, name: str) -> str:
    m = re.search(FIELD_RE.format(name=name), line)
    val = (m.group(1) if m else "").strip()
    return "" if val in ("", "_") else val


def field_plain(line: str, name: str) -> str:
    """`Add: x, y · Remove: z` style fields (no bold)."""
    m = re.search(rf"\b{name}:\s*(.*?)\s*(?:·|`|$)", line)
    val = (m.group(1) if m else "").strip()
    return "" if val in ("", "_") else val


def parse(path: Path) -> list[dict]:
    out = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.lstrip().startswith(">"):
            continue
        m_id = ITEM_ID_RE.search(line) or BRIEF_ID_RE.search(line) or SCOPE_ID_RE.search(line)
        if not m_id:
            continue
        rid = m_id.group(0)
        if rid.startswith("LAN-S"):
            rec = {"id": rid, "kind": "scope", "add": field_plain(line, "Add"),
                   "remove": field_plain(line, "Remove")}
            if rec["add"] or rec["remove"]:
                rec["brief"] = path.name
                out.append(rec)
            continue
        m_rate = RATE_RE.search(line)
        tags = [t.strip().lower() for t in field(line, "Tags").split(",") if t.strip()]
        rec = {"id": rid, "kind": "brief" if rid.startswith("LAN-W") else "item",
               "rating": int(m_rate.group(1)) if m_rate else None, "tags": tags}
        if rec["kind"] == "brief":
            rec["missed"] = field(line, "Missed")
            rec["notes"] = field(line, "Notes")
        if rec["rating"] is None and not tags and not rec.get("missed") and not rec.get("notes"):
            continue
        rec["brief"] = path.name
        out.append(rec)
    return out


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--from", dest="dirs", action="append", type=Path,
                    help="folder of briefs to read (repeatable)")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    dirs = args.dirs or [DEFAULT_MYDAY, NEWS_DIR]

    have = ratings()
    new = []
    for d in dirs:
        if not d.exists():
            print(f"skip (not found): {d}")
            continue
        for f in sorted(d.glob("*_lab-automation-weekly.md")):
            for rec in parse(f):
                old = have.get(rec["id"])
                same = old and all(old.get(k) == rec.get(k) for k in ("rating", "tags", "missed", "notes", "add", "remove"))
                if same:
                    continue
                rec["harvested_at"] = now_utc()
                rec["from"] = str(d)
                have[rec["id"]] = rec
                new.append(rec)
                desc = (f"add={rec['add']!r} remove={rec['remove']!r}" if rec["kind"] == "scope"
                        else f"rating={rec['rating']} tags={rec['tags']}" + (f" missed={rec['missed']!r}" if rec.get("missed") else ""))
                print(f"{'would add' if args.dry_run else 'added'}: {rec['id']}  {desc}")
    if not args.dry_run:
        append_jsonl(FEEDBACK, new)
    print(f"{len(new)} new or changed rating(s); {len(have)} rated in total.")


if __name__ == "__main__":
    main()
