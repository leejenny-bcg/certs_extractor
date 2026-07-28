"""Stage 5: compare the corpus-derived benefits_master.json against the
Topic Tree - this is where the tree finally re-enters the pipeline, as a
diff target rather than something extraction was ever anchored to.

Pass A - exact match on aligned key. The corpus side already has
`merge_key` from Stage 4 (lemma + leading-article-stripped). The Topic
Tree side has `normalized_key` (lemma only, from build_benefits.py) - this
script applies the same leading-article strip to it so both sides are on
equal footing before comparing.

Pass B - fuzzy match (RapidFuzz) between whatever's left unmatched on both
sides. Unlike Stage 4 (which restricted fuzzy rescue to true singletons to
keep ~16k raw candidates tractable), both lists here are already small and
deduped (1,986 tree entries, ~1,200 corpus benefits), so a full comparison
is cheap enough to run directly with no subsetting.

Outputs (JSON + CSV, kept as flat records for an eventual Streamlit UI to
load directly without further reshaping):
  - corpus_benefits_not_in_tree  - the original motivating question
  - tree_entries_not_in_corpus   - the inverse gap
  - matched_pairs                - the overlap, tagged exact/fuzzy + score

Usage:
    python3 compare_to_topic_tree.py <benefits_master.json> <topic_tree_benefits.json> <output_dir>
"""
import argparse
import csv
import json
import sys
from pathlib import Path

from merge_candidates import strip_leading_article
from rapidfuzz import fuzz, process

FUZZY_THRESHOLD = 90


def load_corpus(path):
    with open(path) as f:
        records = json.load(f)
    for r in records:
        r["_key"] = r["merge_key"]
    return records


def load_tree(path):
    with open(path) as f:
        data = json.load(f)
    entries = data["benefits"]
    for e in entries:
        e["_key"] = strip_leading_article(e["normalized_key"])
    return entries


def build_tree_index(tree):
    by_key = {}
    for e in tree:
        by_key.setdefault(e["_key"], []).append(e)
    return by_key


def run_comparison(corpus, tree):
    tree_by_key = build_tree_index(tree)
    matched_tree_keys = set()
    matched_pairs = []
    corpus_unmatched = []

    # Pass A: exact key match
    for c in corpus:
        hits = tree_by_key.get(c["_key"])
        if hits:
            for e in hits:
                matched_pairs.append(
                    {
                        "corpus_canonical_name": c["canonical_name"],
                        "corpus_total_mentions": c["total_mentions"],
                        "corpus_tiers_present": c["tiers_present"],
                        "corpus_profiles_present": c["profiles_present"],
                        "tree_benefit_name": e["benefit_name"],
                        "tree_topic_ids": e["topic_ids"],
                        "tree_paths": e["tree_paths"],
                        "match_type": "exact",
                        "score": 100,
                    }
                )
                matched_tree_keys.add(e["_key"])
        else:
            corpus_unmatched.append(c)

    # Pass B: fuzzy match against the fixed pool of still-unmatched tree
    # entries. Deliberately not removing tree entries as they get matched -
    # multiple corpus benefits legitimately mapping to the same coarser tree
    # entry is expected, not a bug to prevent.
    tree_pool = [e for e in tree if e["_key"] not in matched_tree_keys]
    tree_pool_names = [e["benefit_name"] for e in tree_pool]

    still_unmatched_corpus = []
    for c in corpus_unmatched:
        best = (
            process.extractOne(
                c["canonical_name"], tree_pool_names, scorer=fuzz.token_sort_ratio, score_cutoff=FUZZY_THRESHOLD
            )
            if tree_pool_names
            else None
        )
        if best is None:
            still_unmatched_corpus.append(c)
            continue
        _, score, idx = best
        e = tree_pool[idx]
        matched_pairs.append(
            {
                "corpus_canonical_name": c["canonical_name"],
                "corpus_total_mentions": c["total_mentions"],
                "corpus_tiers_present": c["tiers_present"],
                "corpus_profiles_present": c["profiles_present"],
                "tree_benefit_name": e["benefit_name"],
                "tree_topic_ids": e["topic_ids"],
                "tree_paths": e["tree_paths"],
                "match_type": "fuzzy",
                "score": score,
            }
        )
        matched_tree_keys.add(e["_key"])

    tree_unmatched = [e for e in tree if e["_key"] not in matched_tree_keys]

    return matched_pairs, still_unmatched_corpus, tree_unmatched


def write_json(obj, path):
    with open(path, "w") as f:
        json.dump(obj, f, indent=2, default=str)


def write_corpus_csv(records, path):
    with open(path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["canonical_name", "total_mentions", "document_count", "tiers_present", "profiles_present", "parent_headers"])
        for r in records:
            writer.writerow(
                [
                    r["canonical_name"],
                    r["total_mentions"],
                    r["document_count"],
                    ",".join(str(t) for t in r["tiers_present"]),
                    ",".join(r["profiles_present"]),
                    " | ".join(r["parent_headers"][:5]),
                ]
            )


def write_tree_csv(entries, path):
    with open(path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["benefit_name", "topic_ids", "tree_paths"])
        for e in entries:
            writer.writerow([e["benefit_name"], ",".join(str(t) for t in e["topic_ids"]), " | ".join(e["tree_paths"][:2])])


def write_matched_csv(pairs, path):
    with open(path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["corpus_canonical_name", "tree_benefit_name", "match_type", "score", "corpus_total_mentions"])
        for p in pairs:
            writer.writerow([p["corpus_canonical_name"], p["tree_benefit_name"], p["match_type"], p["score"], p["corpus_total_mentions"]])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("corpus_path", type=Path, help="benefits_master.json")
    parser.add_argument("tree_path", type=Path, help="benefits.json (Topic Tree, from build_benefits.py)")
    parser.add_argument("output_dir", type=Path)
    args = parser.parse_args()

    args.output_dir.mkdir(parents=True, exist_ok=True)

    corpus = load_corpus(args.corpus_path)
    tree = load_tree(args.tree_path)
    print(f"Loaded {len(corpus)} corpus benefits, {len(tree)} Topic Tree entries", file=sys.stderr)

    matched_pairs, corpus_unmatched, tree_unmatched = run_comparison(corpus, tree)

    corpus_unmatched.sort(key=lambda r: -r["total_mentions"])
    tree_unmatched.sort(key=lambda e: e["benefit_name"].lower())
    matched_pairs.sort(key=lambda p: -p["corpus_total_mentions"])

    write_json(corpus_unmatched, args.output_dir / "corpus_benefits_not_in_tree.json")
    write_json(tree_unmatched, args.output_dir / "tree_entries_not_in_corpus.json")
    write_json(matched_pairs, args.output_dir / "matched_pairs.json")
    write_corpus_csv(corpus_unmatched, args.output_dir / "corpus_benefits_not_in_tree.csv")
    write_tree_csv(tree_unmatched, args.output_dir / "tree_entries_not_in_corpus.csv")
    write_matched_csv(matched_pairs, args.output_dir / "matched_pairs.csv")

    exact_count = sum(1 for p in matched_pairs if p["match_type"] == "exact")
    fuzzy_count = sum(1 for p in matched_pairs if p["match_type"] == "fuzzy")
    matched_tree_count = len(tree) - len(tree_unmatched)
    matched_corpus_count = len(corpus) - len(corpus_unmatched)

    print("\n--- summary ---", file=sys.stderr)
    print(f"Matched pairs: {len(matched_pairs)} ({exact_count} exact, {fuzzy_count} fuzzy)", file=sys.stderr)
    print(f"Topic Tree: {matched_tree_count}/{len(tree)} matched ({matched_tree_count/len(tree):.1%}), {len(tree_unmatched)} not found in corpus", file=sys.stderr)
    print(f"Corpus: {matched_corpus_count}/{len(corpus)} matched ({matched_corpus_count/len(corpus):.1%}), {len(corpus_unmatched)} not on Topic Tree", file=sys.stderr)


if __name__ == "__main__":
    main()
