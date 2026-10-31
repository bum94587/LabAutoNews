"""Gather research state from every branch before a run starts.

Each scheduled cloud run pushes to its own `claude/...` branch, so yesterday's items are not
on the branch today's run starts from. This fetches `origin/main` and every `origin/claude/*`
branch and folds their data into the working tree:

- union files (JSONL, one record per line) are merged by key, so nothing is lost and
  re-running is harmless: data/items/*.jsonl, data/verify/*.jsonl, data/feedback/ratings.jsonl, scope_log.jsonl,
  data/raw/links.jsonl, data/raw/fetch_log.jsonl
- write-once files are copied in when missing locally: data/runs/*.json,
  data/editorial/*.md, docs/news/*.md
- latest-wins files take the newest commit's copy: config/weights.json, docs/tuning.md

Only files change; nothing is checked out, merged or committed.

    uv run sync_state.py            # fetch and merge
    uv run sync_state.py --no-fetch # use refs already fetched
"""

from __future__ import annotations

import argparse
import fnmatch
import json
import subprocess
import sys

from labnews.common import ROOT

UNION = {  # glob -> function giving a record's key
    "data/items/*.jsonl": lambda r: r["id"],
    "data/verify/*.jsonl": lambda r: (r["id"], r.get("at", "")),
    "data/feedback/ratings.jsonl": lambda r: (r["id"], r.get("harvested_at", "")),
    "data/feedback/scope_log.jsonl": lambda r: (r["id"], r.get("harvested_at", "")),
    "data/raw/links.jsonl": lambda r: r["url"],
    "data/raw/fetch_log.jsonl": lambda r: (r["source_id"], r["at"]),
}
COPY_IF_MISSING = ["data/runs/*.json", "data/editorial/*.md", "docs/news/*.md", "docs/news/assets/*"]
LATEST = ["config/weights.json", "docs/tuning.md"]


def git(*args: str, ok_fail: bool = False) -> str:
    done = subprocess.run(["git", "-C", str(ROOT), *args], capture_output=True, text=True, timeout=300)
    if done.returncode and not ok_fail:
        sys.exit(f"git {' '.join(args)} failed:\n{done.stderr.strip()}")
    return done.stdout if done.returncode == 0 else ""


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--no-fetch", action="store_true")
    args = ap.parse_args()
    if not args.no_fetch:
        git("fetch", "--prune", "origin", "+refs/heads/main:refs/remotes/origin/main",
            "+refs/heads/claude/*:refs/remotes/origin/claude/*", ok_fail=True)

    refs = git("for-each-ref", "--format=%(refname:short)", "refs/remotes/origin/main",
               "refs/remotes/origin/claude").split()
    current = git("rev-parse", "--abbrev-ref", "HEAD").strip()
    refs = [r for r in refs if r != f"origin/{current}"]
    patterns = list(UNION) + COPY_IF_MISSING + LATEST
    changed: list[str] = []
    newest: dict[str, tuple[int, str]] = {}

    for ref in refs:
        files = git("ls-tree", "-r", "--name-only", ref, "--", "data", "docs", "config", ok_fail=True).split("\n")
        for path in filter(None, files):
            pat = next((p for p in patterns if fnmatch.fnmatch(path, p)), None)
            if not pat:
                continue
            local = ROOT / path
            if pat in UNION:
                theirs = git("show", f"{ref}:{path}", ok_fail=True)
                key = UNION[pat]
                mine = local.read_text(encoding="utf-8") if local.exists() else ""
                have = {}
                for line in mine.splitlines():
                    if line.strip():
                        have[key(json.loads(line))] = line
                added = 0
                for line in theirs.splitlines():
                    if line.strip():
                        k = key(json.loads(line))
                        if k not in have:
                            have[k] = line
                            added += 1
                if added:
                    local.parent.mkdir(parents=True, exist_ok=True)
                    local.write_text("".join(v + "\n" for v in have.values()), encoding="utf-8")
                    changed.append(f"+{added} line(s) {path}  (from {ref})")
            elif pat in COPY_IF_MISSING:
                if not local.exists():
                    data = subprocess.run(["git", "-C", str(ROOT), "show", f"{ref}:{path}"],
                                          capture_output=True, timeout=120).stdout
                    local.parent.mkdir(parents=True, exist_ok=True)
                    local.write_bytes(data)
                    changed.append(f"copied {path}  (from {ref})")
            else:
                stamp = int(git("log", "-1", "--format=%ct", ref, "--", path, ok_fail=True).strip() or 0)
                if stamp > newest.get(path, (0, ""))[0]:
                    newest[path] = (stamp, ref)

    for path, (stamp, ref) in newest.items():
        local = ROOT / path
        mine = int(git("log", "-1", "--format=%ct", "HEAD", "--", path, ok_fail=True).strip() or 0)
        if stamp > mine:
            local.write_text(git("show", f"{ref}:{path}"), encoding="utf-8")
            changed.append(f"updated {path}  (newer on {ref})")

    print("\n".join(changed) if changed else "Already up to date with every branch.")
    print(f"{len(refs)} branch(es) scanned.")


if __name__ == "__main__":
    main()
