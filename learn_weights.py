"""Learn from your ratings what kind of item is worth finding, and write it down.

Joins data/feedback/ratings.jsonl to the items and verdicts, then for every item property
(source, segment, type, how it was found, first-ref domain, companies, verifier verdicts)
computes a shrunk mean rating: a property seen only once or twice stays close to the overall
mean, so one rating can't swing the research. The result:

- config/weights.json - read by the research run (where to spend effort) and by
  build_brief.py (story order: the researcher's 1-5 relevance nudged by these effects)
- docs/tuning.md      - the same thing for humans: what's working, what isn't, plus how
  well the researcher's own relevance guesses and the verifier match your judgement

It is deliberately simple (an additive, empirical-Bayes model) until there are enough
ratings (~150+) for something better; the data it needs is the same either way.

    uv run learn_weights.py
"""

from __future__ import annotations

from collections import defaultdict
from statistics import mean

from labnews.common import (ROOT, WEIGHTS, all_items, all_verdicts, dump_json, feature_values, now_utc,
                            ratings)

PRIOR = 3.0      # pseudo-ratings pulling each property toward the overall mean
MIN_N = 2        # properties with fewer ratings are reported but not used


def spearman(xs: list[float], ys: list[float]) -> float | None:
    if len(xs) < 5:
        return None

    def ranks(v: list[float]) -> list[float]:
        order = sorted(range(len(v)), key=lambda i: v[i])
        r = [0.0] * len(v)
        i = 0
        while i < len(order):
            j = i
            while j + 1 < len(order) and v[order[j + 1]] == v[order[i]]:
                j += 1
            for k in range(i, j + 1):
                r[order[k]] = (i + j) / 2
            i = j + 1
        return r

    rx, ry = ranks(xs), ranks(ys)
    mx, my = mean(rx), mean(ry)
    num = sum((a - mx) * (b - my) for a, b in zip(rx, ry))
    den = (sum((a - mx) ** 2 for a in rx) * sum((b - my) ** 2 for b in ry)) ** 0.5
    return round(num / den, 3) if den else None


def main() -> None:
    items = {it["id"]: it for it in all_items()}
    verdicts = all_verdicts()
    rated = [(items[r["id"]], verdicts.get(r["id"]), r) for r in ratings().values()
             if r["kind"] == "item" and r.get("rating") and r["id"] in items]
    briefs = [r for r in ratings().values() if r["kind"] == "brief"]

    if not rated:
        dump_json(WEIGHTS, {"generated": now_utc(), "n_ratings": 0, "global_mean": None, "features": {}, "tags": {}})
        (ROOT / "docs" / "tuning.md").write_text(
            "# Tuning\n\nNo ratings yet. Rate stories in the weekly brief (myday viewer → Edit) and "
            "run `uv run harvest_ratings.py && uv run learn_weights.py`.\n", encoding="utf-8")
        print("No ratings yet; wrote empty weights.")
        return

    g = mean(r["rating"] for _, _, r in rated)
    stats: dict[str, dict[str, list[int]]] = defaultdict(lambda: defaultdict(list))
    tag_stats: dict[str, dict[str, int]] = defaultdict(lambda: defaultdict(int))
    for it, v, r in rated:
        for k, val in feature_values(it, v):
            stats[k][val].append(r["rating"])
        for t in r.get("tags", []):
            for k, val in feature_values(it, v):
                tag_stats[f"{k}={val}"][t] += 1

    features: dict[str, dict[str, dict]] = {}
    for k, vals in stats.items():
        for val, rs in vals.items():
            shrunk = (sum(rs) + PRIOR * g) / (len(rs) + PRIOR)
            entry = {"n": len(rs), "mean": round(mean(rs), 2), "shrunk": round(shrunk, 2),
                     "effect": round(shrunk - g, 3) if len(rs) >= MIN_N else 0.0}
            features.setdefault(k, {})[val] = entry

    rel = spearman([it["relevance"] for it, _, _ in rated], [r["rating"] for _, _, r in rated])
    wrong_but_verified = [it["id"] for it, v, r in rated
                          if "wrong" in r.get("tags", []) and v and v["facts"] == "verified"]
    unsound_but_sound = [it["id"] for it, v, r in rated
                         if "unsound" in r.get("tags", []) and v and v["science"] == "sound"]
    steer = {t: [f"{k}={val}" for k, vals in features.items() for val in vals
                 if tag_stats[f"{k}={val}"].get(t, 0) >= 2] for t in ("more", "less", "off-topic", "hype")}

    weights = {"generated": now_utc(), "n_ratings": len(rated), "global_mean": round(g, 3),
               "features": features, "tags": {k: dict(v) for k, v in tag_stats.items()},
               "steer": steer, "relevance_spearman": rel,
               "verifier_misses": {"wrong_but_verified": wrong_but_verified,
                                   "unsound_but_sound": unsound_but_sound},
               "missed_leads": [b["missed"] for b in briefs if b.get("missed")]}
    dump_json(WEIGHTS, weights)

    md = [f"# Tuning (from {len(rated)} rated stories, {len(briefs)} brief ratings)", "",
          f"Generated {weights['generated']} by `learn_weights.py`. Overall mean rating {g:.2f}/5. "
          f"Effects are shrunk toward that mean (prior {PRIOR:g}); a property needs {MIN_N}+ ratings to count.", ""]
    for k in sorted(features):
        rows = sorted(features[k].items(), key=lambda kv: -kv[1]["shrunk"])
        md += [f"## {k}", "", "| value | n | mean | shrunk | effect |", "|---|---:|---:|---:|---:|"]
        md += [f"| {val} | {e['n']} | {e['mean']} | {e['shrunk']} | {e['effect']:+.2f} |" for val, e in rows]
        md.append("")
    md += ["## Calibration", "",
           f"- Researcher's relevance guess vs your rating (Spearman): {rel if rel is not None else 'needs 5+ ratings'}",
           f"- Tagged `wrong` although the verifier said facts verified: {', '.join(wrong_but_verified) or 'none'}",
           f"- Tagged `unsound` although the verifier said sound: {', '.join(unsound_but_sound) or 'none'}", "",
           "## Steering", ""]
    md += [f"- `{t}`: {', '.join(v) or '—'}" for t, v in steer.items()]
    if weights["missed_leads"]:
        md += ["", "## Missed (from your brief ratings)", ""] + [f"- {m}" for m in weights["missed_leads"]]
    (ROOT / "docs" / "tuning.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print(f"Learned from {len(rated)} ratings (mean {g:.2f}); wrote config/weights.json and docs/tuning.md.")


if __name__ == "__main__":
    main()
