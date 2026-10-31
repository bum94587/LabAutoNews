"""Shared paths, file formats and validation for the LabAutoNews scripts.

Data model (all plain text so git can merge it and myday can read it):

- data/items/YYYY-MM-DD.jsonl    one research item per line, written by that day's run
- data/verify/YYYY-MM-DD.jsonl   the verifier agent's verdicts, keyed by item id
- data/runs/YYYY-MM-DD.json      what that day's run checked (sources, methods, queries)
- data/editorial/YYYY-MM-DD.md   TL;DR + "signals to watch" for a weekly brief
- data/feedback/ratings.jsonl    your ratings, tags and scope requests, harvested from the briefs
- data/feedback/scope_log.jsonl  scope requests the runs have applied to config/
- data/raw/links.jsonl           every link the fetcher has ever seen (first_seen date)
- config/weights.json            what learn_weights.py learned from the ratings
"""

from __future__ import annotations

import json
import re
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any, Iterable

import yaml

ROOT = Path(__file__).resolve().parent.parent
CONFIG = ROOT / "config"
DATA = ROOT / "data"
ITEMS_DIR = DATA / "items"
VERIFY_DIR = DATA / "verify"
RUNS_DIR = DATA / "runs"
EDITORIAL_DIR = DATA / "editorial"
FEEDBACK = DATA / "feedback" / "ratings.jsonl"
SCOPE_LOG = DATA / "feedback" / "scope_log.jsonl"
RAW_DIR = DATA / "raw"
LINKS = RAW_DIR / "links.jsonl"
FETCH_LOG = RAW_DIR / "fetch_log.jsonl"
NEWS_DIR = ROOT / "docs" / "news"
WEIGHTS = CONFIG / "weights.json"

ITEM_ID_RE = re.compile(r"LAN-\d{8}-\d{2,3}")
BRIEF_ID_RE = re.compile(r"LAN-W\d{8}")
SCOPE_ID_RE = re.compile(r"LAN-S\d{8}")

# Quick-read limits (words). validate.py fails an item that goes over.
MAX_WORDS = {"title": 14, "summary": 50, "why_it_matters": 30}

FACTS = ["verified", "partial", "unverified", "contradicted"]
SCIENCE = ["sound", "questionable", "unsupported", "na"]
STATUS = ["include", "hold", "drop"]
FOUND_VIA = ["feed", "site-search", "web-search", "followup", "missed-lead"]
REF_KINDS = ["primary", "secondary", "paper", "data"]


def now_utc() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def today() -> str:
    return date.today().isoformat()


def load_yaml(name: str) -> dict:
    return yaml.safe_load((CONFIG / name).read_text(encoding="utf-8"))


def sources() -> list[dict]:
    return load_yaml("sources.yaml")["sources"]


def watchlist() -> dict:
    return load_yaml("watchlist.yaml")


def read_jsonl(path: Path) -> list[dict]:
    if not path.exists():
        return []
    out = []
    for n, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        line = line.strip()
        if not line:
            continue
        try:
            out.append(json.loads(line))
        except json.JSONDecodeError as e:
            raise SystemExit(f"{path}:{n}: bad JSON ({e})")
    return out


def write_jsonl(path: Path, rows: Iterable[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows), encoding="utf-8")


def append_jsonl(path: Path, rows: Iterable[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")


def all_items() -> list[dict]:
    rows: list[dict] = []
    for p in sorted(ITEMS_DIR.glob("*.jsonl")):
        rows.extend(read_jsonl(p))
    return rows


def all_verdicts() -> dict[str, dict]:
    """Item id -> newest verdict (by `at`)."""
    out: dict[str, dict] = {}
    for p in sorted(VERIFY_DIR.glob("*.jsonl")):
        for v in read_jsonl(p):
            old = out.get(v["id"])
            if old is None or v.get("at", "") >= old.get("at", ""):
                out[v["id"]] = v
    return out


def ratings() -> dict[str, dict]:
    """Rated id (item or brief) -> newest rating."""
    out: dict[str, dict] = {}
    for r in read_jsonl(FEEDBACK):
        old = out.get(r["id"])
        if old is None or r.get("harvested_at", "") >= old.get("harvested_at", ""):
            out[r["id"]] = r
    return out


def domain(url: str) -> str:
    m = re.match(r"https?://([^/]+)", url or "")
    host = m.group(1).lower() if m else ""
    return host.removeprefix("www.")


# --------------------------------------------------------------------------- validation

def validate_item(it: dict, segments: set[str], types: set[str], source_ids: set[str]) -> list[str]:
    errs = []
    need = ["id", "found", "published", "title", "summary", "segment", "type", "source_id",
            "found_via", "refs", "relevance", "status"]
    for k in need:
        if k not in it:
            errs.append(f"missing '{k}'")
    if errs:
        return errs
    if not ITEM_ID_RE.fullmatch(it["id"]):
        errs.append(f"id '{it['id']}' must look like LAN-YYYYMMDD-NN")
    for k in ("found", "published"):
        if it[k] and not re.fullmatch(r"\d{4}-\d{2}(-\d{2})?", str(it[k])):
            errs.append(f"{k} '{it[k]}' must be YYYY-MM-DD (or YYYY-MM if only the month is known)")
    if it["segment"] not in segments:
        errs.append(f"segment '{it['segment']}' not in config/watchlist.yaml")
    if it["type"] not in types:
        errs.append(f"type '{it['type']}' not in watchlist item_types")
    if it["source_id"] not in source_ids | {"web"}:
        errs.append(f"source_id '{it['source_id']}' not in config/sources.yaml (or 'web')")
    if it["found_via"] not in FOUND_VIA:
        errs.append(f"found_via '{it['found_via']}' not in {FOUND_VIA}")
    if it["status"] not in STATUS:
        errs.append(f"status '{it['status']}' not in {STATUS}")
    if not isinstance(it["relevance"], int) or not 1 <= it["relevance"] <= 5:
        errs.append("relevance must be an integer 1-5")
    for field, limit in MAX_WORDS.items():
        n = len(str(it.get(field, "")).split())
        if n > limit and it.get("status") == "include":
            errs.append(f"{field} is {n} words; keep it to {limit} (details go in claims)")
    refs = it["refs"]
    if not refs:
        errs.append("needs at least one ref - no source, no claim")
    for i, r in enumerate(refs):
        if not str(r.get("url", "")).startswith("http"):
            errs.append(f"refs[{i}] has no http url")
        if r.get("kind") not in REF_KINDS:
            errs.append(f"refs[{i}].kind must be one of {REF_KINDS}")
    for i, c in enumerate(it.get("claims", [])):
        if not isinstance(c.get("ref"), int) or not 0 <= c["ref"] < len(refs):
            errs.append(f"claims[{i}].ref must index into refs")
    return errs


def validate_verdict(v: dict) -> list[str]:
    errs = []
    for k in ("id", "facts", "science", "notes", "checked", "at"):
        if k not in v:
            errs.append(f"missing '{k}'")
    if errs:
        return errs
    if v["facts"] not in FACTS:
        errs.append(f"facts '{v['facts']}' not in {FACTS}")
    if v["science"] not in SCIENCE:
        errs.append(f"science '{v['science']}' not in {SCIENCE}")
    if not v["checked"]:
        errs.append("checked must list the URLs the verifier actually opened or searched")
    return errs


# --------------------------------------------------------------------------- scoring

def feature_values(it: dict, verdict: dict | None = None) -> list[tuple[str, str]]:
    """The item properties the learner keeps statistics on."""
    feats = [
        ("source_id", it.get("source_id", "")),
        ("segment", it.get("segment", "")),
        ("type", it.get("type", "")),
        ("found_via", it.get("found_via", "")),
    ]
    refs = it.get("refs") or []
    if refs:
        feats.append(("domain", domain(refs[0].get("url", ""))))
        feats.append(("has_primary", str(any(r.get("kind") == "primary" for r in refs)).lower()))
    for c in it.get("companies", []):
        feats.append(("company", c))
    if verdict:
        feats.append(("facts", verdict.get("facts", "")))
        feats.append(("science", verdict.get("science", "")))
    return [(k, v) for k, v in feats if v]


def predicted_score(it: dict, verdict: dict | None, weights: dict | None) -> float:
    """The researcher's 1-5 relevance, nudged by what the ratings taught us.

    Each learned feature contributes its (shrunk) deviation from the overall mean rating;
    the sum is damped so one strong feature cannot swamp the rest.
    """
    base = float(it.get("relevance", 3))
    if not weights or not weights.get("features"):
        return base
    adj = 0.0
    for k, v in feature_values(it, verdict):
        f = weights["features"].get(k, {}).get(v)
        if f:
            adj += f["effect"]
    return base + max(-1.5, min(1.5, adj * 0.5))


def load_weights() -> dict | None:
    if WEIGHTS.exists():
        return json.loads(WEIGHTS.read_text(encoding="utf-8"))
    return None


def dump_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
