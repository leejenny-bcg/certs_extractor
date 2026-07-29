"""Derives a small, deploy-safe text-only cache from Stage 1's full
extracted-text cache, for the UI's snippet preview (and Stage 4.5/5.5's
gather_snippets()) to read instead of output/extracted/ directly.

Stage 1's output/extracted/ is 120MB, but measured directly: only 7.8MB of
that is raw_text. The other 112MB is per-word font/position data (needed
by Stage 2/3 to detect bullet hierarchy and header boundaries) and an
unused lemma_text field - neither of which any snippet-lookup code path
has ever read. Committing the full cache to git for the deployed UI's
sake (tried first) broke Streamlit Community Cloud's build - confirmed by
isolating the commit on a test branch - almost certainly a clone/build
size or time limit on its free tier.

This script strips both fields per page, keeping every page of every
document (not just ones a benefit happens to reference) so the UI's
"pick any page to preview" and "full page text" fallback behave
identically to reading output/extracted/ directly - just ~8-10MB instead
of 120MB.

output/extracted/ itself is untouched and stays local-only (gitignored) -
Stage 2 (segment.py) and Stage 3 (extract_candidates.py) still read it
directly via their own CLI args and still need the word-level data this
script throws away.

Usage:
    python3 build_text_cache.py <extracted_dir> <output_dir>
"""
import argparse
import json
import sys
from pathlib import Path


def slim_record(record):
    return {
        "doc_id": record["doc_id"],
        "num_pages": record["num_pages"],
        "pages": [{"raw_text": p["raw_text"]} for p in record["pages"]],
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("extracted_dir", type=Path, help="output/extracted (Stage 1's full cache)")
    parser.add_argument("output_dir", type=Path)
    args = parser.parse_args()

    text_cache_dir = args.output_dir / "extracted_text"
    text_cache_dir.mkdir(parents=True, exist_ok=True)

    files = sorted(args.extracted_dir.glob("*.json"))
    for path in files:
        with open(path) as f:
            record = json.load(f)
        with open(text_cache_dir / path.name, "w") as f:
            json.dump(slim_record(record), f)

    print(f"Wrote {len(files)} slimmed document(s) to {text_cache_dir}", file=sys.stderr)


if __name__ == "__main__":
    main()
