"""Stage 4: merge Stage 3's per-document candidates into a single
cross-document benefit list, with confidence kept visible rather than
silently blended (same philosophy as the original certs_riders pipeline's
exact/fuzzy tiering).

Pass A - exact-after-normalization: lowercase, lemmatize, strip punctuation
(normalize.py, shared with Stage 1/3), PLUS strip a leading indefinite
article ("a"/"an"/"the"). The article-stripping matters concretely here:
CSR-rider-derived candidates are pulled from bulleted sentence fragments
like "- A retail health clinic visit", while the same concept elsewhere
reads "Retail health clinic visits" - without stripping the leading article
these fail to merge on lemma alone.

Pass B - fuzzy rescue: only run on clusters that are singletons (mentioned
exactly once in the whole corpus) AND shape "phrase" - brute-forcing fuzzy
matching across all ~16k raw candidates would be both slow and noisy;
restricting it to the singleton tail is what makes it tractable, mirroring
the original pipeline's "only fuzzy-match the gap list" reasoning.

Usage:
    python3 merge_candidates.py <candidates_dir> <output_dir>
"""
import argparse
import csv
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

from normalize import normalized_key
from rapidfuzz import fuzz

LEADING_ARTICLES = ("a ", "an ", "the ")
FUZZY_THRESHOLD = 90


def strip_leading_article(key):
    for article in LEADING_ARTICLES:
        if key.startswith(article):
            return key[len(article):]
    return key


def merge_key(text):
    return strip_leading_article(normalized_key(text))


def load_all(candidates_dir):
    rows = []  # (doc_id, profile, candidate)
    for f in sorted(Path(candidates_dir).glob("*.json")):
        with open(f) as fh:
            doc = json.load(fh)
        for c in doc["candidates"]:
            rows.append((doc["doc_id"], doc["profile"], c))
    return rows


def pick_canonical_name(variant_counter):
    def score(item):
        text, count = item
        return (count, len(text) < 60, -len(text))
    return max(variant_counter.items(), key=score)[0]


def build_clusters(rows):
    clusters = defaultdict(lambda: {
        "variant_texts": Counter(),
        "tiers_present": set(),
        "profiles_present": set(),
        "parent_headers": set(),
        "inclusion_breakdown": Counter(),
        "shape_breakdown": Counter(),
        "documents": defaultdict(lambda: {"mention_count": 0, "pages": set()}),
        "match_type": "exact",
    })

    for doc_id, profile, c in rows:
        key = merge_key(c["text"])
        if not key:
            continue
        cluster = clusters[key]
        cluster["variant_texts"][c["text"].strip()] += 1
        cluster["tiers_present"].add(c["tier"])
        cluster["profiles_present"].add(profile)
        if c.get("parent_header"):
            cluster["parent_headers"].add(c["parent_header"])
        cluster["inclusion_breakdown"][c["inclusion"]] += 1
        cluster["shape_breakdown"][c["shape"]] += 1
        doc_entry = cluster["documents"][doc_id]
        doc_entry["mention_count"] += 1
        if c.get("source_page") is not None:
            doc_entry["pages"].add(c["source_page"])

    return clusters


def total_mentions(cluster):
    return sum(cluster["variant_texts"].values())


def fuzzy_rescue(clusters):
    """Merge singleton phrase-shaped clusters into a larger cluster if a
    high-similarity match exists, so isolated wording variants don't sit
    forever as their own one-off entries. Tags absorbed keys as 'fuzzy'."""
    all_keys = list(clusters.keys())
    non_singleton_keys = [k for k in all_keys if total_mentions(clusters[k]) > 1]
    singleton_keys = [
        k for k in all_keys
        if total_mentions(clusters[k]) == 1 and clusters[k]["shape_breakdown"].get("phrase", 0) == 1
    ]

    rescued = 0
    for skey in singleton_keys:
        cluster = clusters[skey]
        candidate_text = next(iter(cluster["variant_texts"]))
        best_key, best_score = None, 0
        for okey in non_singleton_keys:
            other_text = pick_canonical_name(clusters[okey]["variant_texts"])
            score = fuzz.token_sort_ratio(candidate_text, other_text)
            if score > best_score:
                best_score, best_key = score, okey
        if best_key is not None and best_score >= FUZZY_THRESHOLD:
            target = clusters[best_key]
            target["variant_texts"].update(cluster["variant_texts"])
            target["tiers_present"] |= cluster["tiers_present"]
            target["profiles_present"] |= cluster["profiles_present"]
            target["parent_headers"] |= cluster["parent_headers"]
            target["inclusion_breakdown"] += cluster["inclusion_breakdown"]
            target["shape_breakdown"] += cluster["shape_breakdown"]
            for doc_id, entry in cluster["documents"].items():
                target_entry = target["documents"][doc_id]
                target_entry["mention_count"] += entry["mention_count"]
                target_entry["pages"] |= entry["pages"]
            target["match_type"] = "fuzzy" if target["match_type"] == "exact" else target["match_type"]
            del clusters[skey]
            rescued += 1

    return rescued


def finalize(clusters):
    records = []
    for key, cluster in clusters.items():
        documents = [
            {"doc_id": doc_id, "mention_count": e["mention_count"], "pages": sorted(e["pages"])}
            for doc_id, e in cluster["documents"].items()
        ]
        documents.sort(key=lambda d: -d["mention_count"])
        records.append(
            {
                "canonical_name": pick_canonical_name(cluster["variant_texts"]),
                "merge_key": key,
                "match_type": cluster["match_type"],
                "variant_texts": dict(cluster["variant_texts"]),
                "tiers_present": sorted(cluster["tiers_present"]),
                "profiles_present": sorted(cluster["profiles_present"]),
                "parent_headers": sorted(cluster["parent_headers"]),
                "inclusion_breakdown": dict(cluster["inclusion_breakdown"]),
                "shape_breakdown": dict(cluster["shape_breakdown"]),
                "total_mentions": total_mentions(cluster),
                "document_count": len(documents),
                "documents": documents,
            }
        )
    records.sort(key=lambda r: -r["total_mentions"])
    return records


def write_csv(records, path):
    with open(path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(
            ["canonical_name", "match_type", "tiers_present", "total_mentions", "document_count",
             "profiles_present", "covered", "excluded", "unknown", "phrase_count", "sentence_count", "parent_headers"]
        )
        for r in records:
            writer.writerow(
                [
                    r["canonical_name"],
                    r["match_type"],
                    ",".join(str(t) for t in r["tiers_present"]),
                    r["total_mentions"],
                    r["document_count"],
                    ",".join(r["profiles_present"]),
                    r["inclusion_breakdown"].get("covered", 0),
                    r["inclusion_breakdown"].get("excluded", 0),
                    r["inclusion_breakdown"].get("unknown", 0),
                    r["shape_breakdown"].get("phrase", 0),
                    r["shape_breakdown"].get("sentence", 0),
                    " | ".join(r["parent_headers"][:5]),
                ]
            )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("candidates_dir", type=Path)
    parser.add_argument("output_dir", type=Path)
    parser.add_argument("--skip-fuzzy", action="store_true", help="Skip Pass B fuzzy rescue (Pass A only)")
    args = parser.parse_args()

    args.output_dir.mkdir(parents=True, exist_ok=True)

    rows = load_all(args.candidates_dir)
    print(f"Loaded {len(rows)} raw candidates", file=sys.stderr)

    clusters = build_clusters(rows)
    print(f"Pass A (exact-after-lemma): {len(clusters)} clusters", file=sys.stderr)

    if not args.skip_fuzzy:
        rescued = fuzzy_rescue(clusters)
        print(f"Pass B (fuzzy rescue): absorbed {rescued} singleton clusters -> {len(clusters)} clusters remain", file=sys.stderr)

    records = finalize(clusters)

    with open(args.output_dir / "benefits_master.json", "w") as f:
        json.dump(records, f, indent=2)
    write_csv(records, args.output_dir / "benefit_summary.csv")

    print(f"\nWrote {len(records)} canonical benefit records", file=sys.stderr)
    print(f"  exact-match clusters: {sum(1 for r in records if r['match_type'] == 'exact')}", file=sys.stderr)
    print(f"  fuzzy-rescued clusters: {sum(1 for r in records if r['match_type'] == 'fuzzy')}", file=sys.stderr)
    print(f"  singleton clusters remaining (1 mention, never merged): {sum(1 for r in records if r['total_mentions'] == 1)}", file=sys.stderr)


if __name__ == "__main__":
    main()
