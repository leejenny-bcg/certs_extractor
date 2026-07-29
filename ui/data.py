"""Framework-agnostic data loading for the certs_extraction Streamlit UI.
No Streamlit dependency, so it's reusable by future pages/tools the same
way certs_riders/ui/data.py is.
"""
import json
import re
import sys
from functools import lru_cache
from pathlib import Path

UI_DIR = Path(__file__).resolve().parent
ROOT_DIR = UI_DIR.parent
OUTPUT_DIR = ROOT_DIR / "output"
PIPELINE_DIR = ROOT_DIR / "pipeline"

sys.path.insert(0, str(PIPELINE_DIR))
from snippets import get_extracted_doc as _get_extracted_doc  # noqa: E402
from snippets import find_snippet as _find_snippet  # noqa: E402
from confidence import is_high_confidence, is_top_level_header, exclusion_reason  # noqa: E402,F401

CODE_PREFIX_RE = re.compile(r"^\d{3,5}\s*-\s*")


@lru_cache(maxsize=1)
def load_benefits_master():
    with open(OUTPUT_DIR / "benefits_master.json") as f:
        return json.load(f)


@lru_cache(maxsize=1)
def load_corpus_not_in_tree():
    with open(OUTPUT_DIR / "corpus_benefits_not_in_tree.json") as f:
        return json.load(f)


@lru_cache(maxsize=1)
def load_tree_not_in_corpus():
    with open(OUTPUT_DIR / "tree_entries_not_in_corpus.json") as f:
        return json.load(f)


@lru_cache(maxsize=1)
def load_matched_pairs():
    with open(OUTPUT_DIR / "matched_pairs.json") as f:
        return json.load(f)


@lru_cache(maxsize=1)
def load_topic_tree():
    with open(OUTPUT_DIR / "benefits.json") as f:
        return json.load(f)["benefits"]


@lru_cache(maxsize=1)
def benefits_by_name():
    return {b["canonical_name"]: b for b in load_benefits_master()}


def has_revenue_code_prefix(benefit_name):
    return bool(CODE_PREFIX_RE.match(benefit_name))


def get_extracted_doc(doc_id):
    """Lazily load a single document's Stage 1.5 text-only cache file
    (output/extracted_text/, not Stage 1's full output/extracted/ - see
    pipeline/snippets.py). Returns None if the cache is missing (e.g. a
    fresh clone before running Stages 1/1.5). The snippet/full-page-text
    features degrade to "not available" rather than crashing the page.
    Thin wrapper over pipeline/snippets.py so pipeline stages (e.g.
    classify_benefits.py) can share the same cache/logic without
    depending on the UI layer.
    """
    return _get_extracted_doc(OUTPUT_DIR, doc_id)


def find_snippet(doc_id, page_idx, term, context_chars=80):
    """See pipeline/snippets.py:find_snippet for the full docstring."""
    return _find_snippet(OUTPUT_DIR, doc_id, page_idx, term, context_chars=context_chars)
