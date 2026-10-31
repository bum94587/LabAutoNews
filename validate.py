"""Check every items / verify file against the schema before committing.

    uv run validate.py          # all files
    uv run validate.py 2026-11-02   # just that day's items and verdicts

Exits non-zero on any problem, so a run can't commit an item without a source link, an
unknown segment, a malformed id, or a verdict that doesn't say what it checked.
"""

from __future__ import annotations

import sys

from labnews.common import (ITEMS_DIR, VERIFY_DIR, read_jsonl, sources, validate_item,
                            validate_verdict, watchlist)


def main() -> None:
    day = sys.argv[1] if len(sys.argv) > 1 else "*"
    wl = watchlist()
    segments, types = set(wl["segments"]), set(wl["item_types"])
    source_ids = {s["id"] for s in sources()}
    problems, ids, n_items, n_verdicts = [], set(), 0, 0

    for p in sorted(ITEMS_DIR.glob(f"{day}.jsonl")):
        for it in read_jsonl(p):
            n_items += 1
            if it.get("id") in ids:
                problems.append(f"{p.name}: duplicate id {it['id']}")
            ids.add(it.get("id"))
            problems += [f"{p.name} {it.get('id', '?')}: {e}" for e in validate_item(it, segments, types, source_ids)]

    all_ids = ids if day == "*" else {it["id"] for q in ITEMS_DIR.glob("*.jsonl") for it in read_jsonl(q)}
    for p in sorted(VERIFY_DIR.glob(f"{day}.jsonl")):
        for v in read_jsonl(p):
            n_verdicts += 1
            problems += [f"{p.name} {v.get('id', '?')}: {e}" for e in validate_verdict(v)]
            if v.get("id") not in all_ids:
                problems.append(f"{p.name}: verdict for unknown item {v.get('id')}")

    for line in problems:
        print(line)
    print(f"{n_items} item(s), {n_verdicts} verdict(s), {len(problems)} problem(s).")
    sys.exit(1 if problems else 0)


if __name__ == "__main__":
    main()
