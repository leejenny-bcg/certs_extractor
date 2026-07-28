"""Stage 5: compare the corpus-derived benefits_master.json against the
Topic Tree - this is where the tree finally re-enters the pipeline, as a
diff target rather than something extraction was ever anchored to.

Pass A - exact match on aligned key. The corpus side already has
`merge_key` from Stage 4 (lemma + leading-article-stripped). The Topic
Tree side has `normalized_key` (lemma only, from build_benefits.py) - this
script applies the same leading-article strip to it so both sides are on
equal footing before comparing.

Pass B - fuzzy match (RapidFuzz) between whatever's left unmatched on both
sides, on the same normalized `_key` Pass A uses (not raw display text -
confirmed this recovers real matches Pass A's exact comparison already
benefited from lemmatization for but Pass B previously didn't). Unlike
Stage 4 (which restricted fuzzy rescue to true singletons to keep ~16k raw
candidates tractable), both lists here are already small and deduped
(1,986 tree entries, ~1,200 corpus benefits), so a full comparison is
cheap enough to run directly with no subsetting.

Pass C - compound splitting. A corpus name joining two genuinely separate
items with literal "and/or" (e.g. "High-dose chemotherapy and/or total
body irradiation") scores low as a whole against either item's own tree
entry, because the other item's words dilute the ratio - confirmed:
"High-dose chemotherapy and/or total body irradiation" only reaches 66
against "High dose chemotherapy" even on normalized keys. Splitting on
" and/or " and fuzzy-matching each half separately (same normalized-key
approach, same threshold) recovers these without the false-positive risk
of splitting on plain "and"/"or"/commas generally - checked against the
corpus first: those split on a fixed idiom ("Room and board"), an
enumeration with ambiguous grouping ("Broken or Lost Lenses or Frames"),
or leave a content-free fragment ("Routine eye exams or services" ->
"services"). "and/or" is a much less ambiguous authorial signal for
"these are separate alternatives" and only 5 corpus names in the whole
unmatched population contain it, all cleanly splittable. Tagged as its
own match_type with the matched half recorded, not folded into "fuzzy",
so a compound-derived match stays distinguishable from a direct one.

Pass D - generic-suffix stripping. Both sides of this comparison use
"Service(s)" as a near-content-free tail word ("Ambulance Services" /
"Ambulance", "Dental Services" / "Dental") - checked directly against the
42 unmatched corpus names ending in "Service(s)": stripping it and
re-matching on normalized keys recovers 7 clean matches (Ambulance,
Dental, Home Health Care, Long-Term Acute Care Hospital, Diagnostic
Radiology, Skilled Nursing Facility, Urgent Care), all >=90 and all
correct, with zero false positives among the ones that stayed below
threshold. Deliberately scoped to "Service(s)" only, not generalized to
other plausible suffixes ("Care", "Program", "Treatment", "Devices",
"Therapy", "Testing", "Examination", "Equipment") - tested each the same
way first and none produced a single clean match; "Supplies" produced
exactly one hit and it was wrong ("Medical Supplies" -> "Medical" at 100,
matching on an overly generic shared word rather than real equivalence).
"Service(s)" is uniquely safe in this corpus, not representative of
suffixes generally, so the list stays a list of one.

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
import re
import sys
from pathlib import Path

from merge_candidates import merge_key, strip_leading_article
from rapidfuzz import fuzz, process

FUZZY_THRESHOLD = 90

COMPOUND_SPLIT_RE = re.compile(r"\s+and/or\s+", re.IGNORECASE)


def split_compound_parts(text):
    """Split a corpus name on literal "and/or" into its separate items, each
    cleaned of leading/trailing punctuation left over from the split (e.g.
    a trailing comma from "X, Y, and/or Z"). Returns [] if there's nothing
    to split - deliberately narrow, see the Pass C docstring above for why
    plain "and"/"or"/commas aren't included."""
    if not COMPOUND_SPLIT_RE.search(text):
        return []
    parts = COMPOUND_SPLIT_RE.split(text)
    return [p.strip(" ,.;") for p in parts if p.strip(" ,.;")]


GENERIC_SUFFIX_RE = re.compile(r"\s+services?$", re.IGNORECASE)


# Found by running this against the real corpus: "Other Services" strips
# to "Other", which then matches the tree's "2109 - Other" at 100 - both
# sides are generic catch-all placeholders, not a real equivalence. This
# pipeline has independently flagged "Other Services"/"Other Dental
# Services" as generic_administrative (not real benefit names) elsewhere,
# so excluding the bare word is evidenced, not speculative. Narrower than a
# word-count guard, which would also reject genuinely good single-word
# remainders like "Ambulance" or "Dental".
GENERIC_REMAINDER_WORDS = {"other", "others"}


def strip_generic_suffix(text):
    """Strip a trailing "Service(s)" - see the Pass D docstring above for
    why this is scoped to that one word specifically. Returns None if there
    is nothing to strip, or if what's left is itself too generic to be a
    meaningful match target (see GENERIC_REMAINDER_WORDS)."""
    stripped = GENERIC_SUFFIX_RE.sub("", text).strip()
    if not stripped or stripped == text:
        return None
    if stripped.lower() in GENERIC_REMAINDER_WORDS:
        return None
    return stripped


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
    #
    # Fuzzy-matches on _key (lemma-normalized + leading-article-stripped),
    # not the raw benefit_name/canonical_name display text - confirmed this
    # recovers real matches Pass A's exact-key comparison already benefits
    # from but Pass B previously didn't: "Bone Marrow Transplants" <->
    # "Bone marrow transplantation" scores 80 on raw text (misses the 90
    # threshold) but 90 on normalized keys (crosses it); "Electroencephalogram
    # (EEG)" <-> "EEG (Electroencephalogram)" goes from 81 to 100. Output
    # fields still use the original display names - only the comparison
    # basis changed.
    tree_pool = [e for e in tree if e["_key"] not in matched_tree_keys]
    tree_pool_keys = [e["_key"] for e in tree_pool]

    still_unmatched_corpus = []
    for c in corpus_unmatched:
        best = (
            process.extractOne(
                c["_key"], tree_pool_keys, scorer=fuzz.token_sort_ratio, score_cutoff=FUZZY_THRESHOLD
            )
            if tree_pool_keys
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

    # Pass C: compound splitting (see module docstring). Only attempted for
    # names Pass B's whole-string comparison already failed on.
    still_unmatched_after_c = []
    for c in still_unmatched_corpus:
        parts = split_compound_parts(c["canonical_name"])
        match = None
        matched_part = None
        for part in parts:
            tree_pool = [e for e in tree if e["_key"] not in matched_tree_keys]
            tree_pool_keys = [e["_key"] for e in tree_pool]
            if not tree_pool_keys:
                break
            best = process.extractOne(
                merge_key(part), tree_pool_keys, scorer=fuzz.token_sort_ratio, score_cutoff=FUZZY_THRESHOLD
            )
            if best is not None:
                _, score, idx = best
                match = (score, tree_pool[idx])
                matched_part = part
                break
        if match is None:
            still_unmatched_after_c.append(c)
            continue
        score, e = match
        matched_pairs.append(
            {
                "corpus_canonical_name": c["canonical_name"],
                "corpus_total_mentions": c["total_mentions"],
                "corpus_tiers_present": c["tiers_present"],
                "corpus_profiles_present": c["profiles_present"],
                "tree_benefit_name": e["benefit_name"],
                "tree_topic_ids": e["topic_ids"],
                "tree_paths": e["tree_paths"],
                "match_type": "fuzzy_compound",
                "score": score,
                "corpus_matched_part": matched_part,
            }
        )
        matched_tree_keys.add(e["_key"])

    # Pass D: generic-suffix stripping (see module docstring). Only
    # attempted for names Pass C also failed on.
    still_unmatched_corpus = []
    for c in still_unmatched_after_c:
        stripped = strip_generic_suffix(c["canonical_name"])
        if stripped is None:
            still_unmatched_corpus.append(c)
            continue
        tree_pool = [e for e in tree if e["_key"] not in matched_tree_keys]
        tree_pool_keys = [e["_key"] for e in tree_pool]
        best = (
            process.extractOne(
                merge_key(stripped), tree_pool_keys, scorer=fuzz.token_sort_ratio, score_cutoff=FUZZY_THRESHOLD
            )
            if tree_pool_keys
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
                "match_type": "fuzzy_suffix_stripped",
                "score": score,
                "corpus_matched_part": stripped,
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
        writer.writerow(["corpus_canonical_name", "tree_benefit_name", "match_type", "score",
                          "corpus_total_mentions", "corpus_matched_part"])
        for p in pairs:
            writer.writerow([p["corpus_canonical_name"], p["tree_benefit_name"], p["match_type"], p["score"],
                              p["corpus_total_mentions"], p.get("corpus_matched_part", "")])


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
    compound_count = sum(1 for p in matched_pairs if p["match_type"] == "fuzzy_compound")
    suffix_count = sum(1 for p in matched_pairs if p["match_type"] == "fuzzy_suffix_stripped")
    matched_tree_count = len(tree) - len(tree_unmatched)
    matched_corpus_count = len(corpus) - len(corpus_unmatched)

    print("\n--- summary ---", file=sys.stderr)
    print(f"Matched pairs: {len(matched_pairs)} ({exact_count} exact, {fuzzy_count} fuzzy, "
          f"{compound_count} fuzzy_compound, {suffix_count} fuzzy_suffix_stripped)", file=sys.stderr)
    print(f"Topic Tree: {matched_tree_count}/{len(tree)} matched ({matched_tree_count/len(tree):.1%}), {len(tree_unmatched)} not found in corpus", file=sys.stderr)
    print(f"Corpus: {matched_corpus_count}/{len(corpus)} matched ({matched_corpus_count/len(corpus):.1%}), {len(corpus_unmatched)} not on Topic Tree", file=sys.stderr)


if __name__ == "__main__":
    main()
