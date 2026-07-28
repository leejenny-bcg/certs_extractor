"""QA sweep over Stage 3 output: aggregate stats per profile, and flag
documents/candidates that look wrong rather than just eyeballing a few
examples. Surfaced, not hidden - this doesn't fix anything, just reports.

Usage:
    python3 qa_stage3.py <candidates_dir> <segments_dir>
"""
import argparse
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

LONG_TEXT_THRESHOLD = 150
NUMERIC_ONLY_RE = re.compile(r"^[\d\s.,%$#-]+$")


def load_all(candidates_dir):
    docs = []
    for f in sorted(Path(candidates_dir).glob("*.json")):
        with open(f) as fh:
            docs.append((f.name, json.load(fh)))
    return docs


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("candidates_dir", type=Path)
    parser.add_argument("segments_dir", type=Path)
    args = parser.parse_args()

    docs = load_all(args.candidates_dir)

    per_profile_doc_counts = defaultdict(list)  # profile -> [(fname, count)]
    tier_counts = Counter()
    shape_counts = Counter()
    inclusion_counts = Counter()
    subtier_counts = Counter()

    zero_candidate_nonskip = []
    long_text_flags = []
    numeric_only_flags = []
    duplicate_flags = []
    bad_page_flags = []

    for fname, doc in docs:
        profile = doc["profile"]
        candidates = doc["candidates"]
        per_profile_doc_counts[profile].append((fname, len(candidates)))

        if profile != "skip" and len(candidates) == 0:
            zero_candidate_nonskip.append(fname)

        seen_pairs = Counter()
        num_pages = None
        seg_path = args.segments_dir / fname
        if seg_path.exists():
            with open(seg_path) as fh:
                seg = json.load(fh)
            num_pages = seg.get("num_pages")

        for c in candidates:
            tier_counts[c["tier"]] += 1
            subtier_counts[c.get("subtier")] += 1
            shape_counts[c["shape"]] += 1
            inclusion_counts[c["inclusion"]] += 1

            text = c["text"].strip()
            if len(text) > LONG_TEXT_THRESHOLD:
                long_text_flags.append((fname, text[:100] + "..."))
            if NUMERIC_ONLY_RE.match(text):
                numeric_only_flags.append((fname, text))

            key = (text.lower(), c.get("parent_header"))
            seen_pairs[key] += 1

            if num_pages is not None and c.get("source_page") is not None:
                if not (0 <= c["source_page"] < num_pages):
                    bad_page_flags.append((fname, text[:60], c["source_page"], num_pages))

        for (text, parent), count in seen_pairs.items():
            if count >= 4:
                duplicate_flags.append((fname, parent, text, count))

    print("=== Per-profile document counts ===")
    for profile, entries in sorted(per_profile_doc_counts.items()):
        counts = [c for _, c in entries]
        if not counts:
            continue
        counts_sorted = sorted(counts)
        median = counts_sorted[len(counts_sorted) // 2]
        print(f"\n{profile}: {len(entries)} docs, median={median}, min={min(counts)}, max={max(counts)}")
        for fname, count in sorted(entries, key=lambda x: x[1]):
            flag = ""
            if profile != "skip" and median > 0 and (count < median * 0.3 or count > median * 3):
                flag = "  <-- OUTLIER"
            print(f"  {count:5} {fname[:75]}{flag}")

    print("\n=== Tier / subtier / shape / inclusion totals ===")
    print("tiers:", dict(tier_counts))
    print("subtiers:", dict(subtier_counts))
    print("shapes:", dict(shape_counts))
    print("inclusion:", dict(inclusion_counts))

    print(f"\n=== Zero-candidate non-skip docs: {len(zero_candidate_nonskip)} ===")
    for f in zero_candidate_nonskip:
        print(" ", f)

    print(f"\n=== Long text (>{LONG_TEXT_THRESHOLD} chars) candidates: {len(long_text_flags)} ===")
    for f, t in long_text_flags[:20]:
        print(" ", f[:50], "::", t)

    print(f"\n=== Numeric-only candidates: {len(numeric_only_flags)} ===")
    for f, t in numeric_only_flags[:20]:
        print(" ", f[:50], "::", t)

    print(f"\n=== Repeated (text, parent) pairs >=4x within a doc: {len(duplicate_flags)} ===")
    for f, parent, text, count in duplicate_flags[:30]:
        print(" ", f[:45], "| parent:", parent, "| x", count, "::", text[:60])

    print(f"\n=== Out-of-range source_page: {len(bad_page_flags)} ===")
    for f, t, page, num_pages in bad_page_flags[:20]:
        print(" ", f[:45], "::", t, "page", page, "of", num_pages)


if __name__ == "__main__":
    main()
