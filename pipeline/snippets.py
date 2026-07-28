"""Shared helper for loading Stage 1's extracted-text cache and finding a
short text excerpt around a term on a given page. Used by the UI (for the
benefit-detail drill-down) and by classify_benefits.py (to gather evidence
for the LLM classification pass) -- lives in pipeline/ rather than ui/ so
pipeline stages don't depend on the UI layer.
"""
import json
import re
from functools import lru_cache

from extract_text import cache_path_for

_WORD_RE = re.compile(r"[A-Za-z0-9]+")


@lru_cache(maxsize=None)
def get_extracted_doc(output_dir, doc_id):
    """Lazily load a single Stage 1 extracted-text cache file for a document.
    Returns None if the cache is missing - output/extracted/ (~115MB) is
    excluded from the deploy repo, so a fresh clone won't have it. Callers
    should degrade to "not available" rather than crashing.
    """
    cache_file = cache_path_for(output_dir, doc_id)
    if not cache_file.exists():
        return None
    with open(cache_file) as f:
        return json.load(f)


def find_snippet(output_dir, doc_id, page_idx, term, context_chars=80):
    """Best-effort: search the page's raw text for `term` (flexible
    whitespace, case-insensitive) and return a short surrounding excerpt.
    `page_idx` is the absolute, 0-indexed page number used throughout this
    pipeline (Stage 1's `pages` list, and every `source_page`/`pages` field
    downstream) - NOT a 1-indexed printed page number. Returns None if no
    direct textual match is found (e.g. the hit came via lemma/fuzzy
    matching, so the surface form differs from `term`).
    """
    doc = get_extracted_doc(output_dir, doc_id)
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
