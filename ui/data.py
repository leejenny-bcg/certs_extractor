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
from extract_text import cache_path_for  # noqa: E402

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


def is_high_confidence(record):
    """A benefit is high-confidence if any of its mentions are Tier 1
    (a certificate's own section header) or Tier 2a/2b bullet phrases -
    i.e. not exclusively Tier 3 index terms or sentence-shaped criteria.
    Mirrors the confidence tiering used throughout the extraction pipeline
    (surfaced as a filter here, never silently dropped from the data).
    """
    if 1 in record["tiers_present"]:
        return True
    phrase_count = record["shape_breakdown"].get("phrase", 0)
    sentence_count = record["shape_breakdown"].get("sentence", 0)
    return phrase_count >= sentence_count


@lru_cache(maxsize=None)
def get_extracted_doc(doc_id):
    """Lazily load a single Stage 1 extracted-text cache file for a document.
    Returns None if the cache is missing - output/extracted/ (~115MB) is
    excluded from the deploy repo, so a fresh clone won't have it. The
    snippet/full-page-text features degrade to "not available" rather than
    crashing the page.
    """
    cache_file = cache_path_for(OUTPUT_DIR, doc_id)
    if not cache_file.exists():
        return None
    with open(cache_file) as f:
        return json.load(f)


_WORD_RE = re.compile(r"[A-Za-z0-9]+")


def find_snippet(doc_id, page_idx, term, context_chars=80):
    """Best-effort: search the page's raw text for `term` (flexible
    whitespace, case-insensitive) and return a short surrounding excerpt.
    `page_idx` is the absolute, 0-indexed page number used throughout this
    pipeline (Stage 1's `pages` list, and every `source_page`/`pages` field
    downstream) - NOT a 1-indexed printed page number. Returns None if no
    direct textual match is found (e.g. the hit came via lemma/fuzzy
    matching, so the surface form differs from `term`).
    """
    doc = get_extracted_doc(doc_id)
    if doc is None or page_idx < 0 or page_idx >= len(doc["pages"]):
        return None
    raw_text = doc["pages"][page_idx]["raw_text"]

    words = _WORD_RE.findall(term)
    if not words:
        return None
    pattern = r"\s+".join(re.escape(w) for w in words)
    m = re.search(pattern, raw_text, re.IGNORECASE)
    if not m:
        return None

    start = max(0, m.start() - context_chars)
    end = min(len(raw_text), m.end() + context_chars)
    prefix = "..." if start > 0 else ""
    suffix = "..." if end < len(raw_text) else ""
    before = raw_text[start:m.start()]
    match_text = raw_text[m.start():m.end()]
    after = raw_text[m.end():end]
    return f"{prefix}{before}**{match_text}**{after}{suffix}"
