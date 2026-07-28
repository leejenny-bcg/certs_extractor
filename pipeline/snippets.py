"""Shared helper for loading Stage 1's extracted-text cache and finding a
short text excerpt around a term on a given page. Used by the UI (for the
benefit-detail drill-down) and by the LLM review stages (classify_benefits.py,
semantic_match_topic_tree.py) to gather real source-text evidence -- lives
in pipeline/ rather than ui/ so pipeline stages don't depend on the UI layer.
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


DEFAULT_MAX_SNIPPETS = 3


def gather_snippets(output_dir, record, max_snippets=DEFAULT_MAX_SNIPPETS, context_chars=80):
    """Real source excerpts for a benefit record, sampled from its
    highest-mention documents/pages via find_snippet() above. Moved here
    (was classify_benefits.py-local) once semantic_match_topic_tree.py
    needed the same "show the model real context, not just the extracted
    name" evidence: a bare name + section header wasn't enough for it to
    tell that "Allogeneic Transplants" was listed alongside "Tandem
    transplants"/"single transplant" under Transplant Services (i.e. a
    bone-marrow/stem-cell modality in context), not general-organ
    allogeneic transplant - it rejected a real match over exactly that gap.

    context_chars defaults to find_snippet()'s own default (80, tuned for
    classify_benefits.py's shorter classification task) but callers that
    need to see sibling list items - not just the immediate phrase - should
    pass a larger value: confirmed the default 80 cuts the "Allogeneic
    Transplants" excerpt above off mid-sentence, right before "Search of
    the National Bone Marrow Donor Program Registry" - the one clause that
    would have told the model this is specifically a bone-marrow benefit.
    """
    snippets = []
    docs = sorted(record["documents"], key=lambda d: -d["mention_count"])
    for doc in docs:
        if len(snippets) >= max_snippets:
            break
        for page_idx in doc["pages"][:2]:
            if len(snippets) >= max_snippets:
                break
            excerpt = find_snippet(output_dir, doc["doc_id"], page_idx, record["canonical_name"],
                                    context_chars=context_chars)
            if excerpt:
                snippets.append({
                    "doc_id": doc["doc_id"],
                    "page": page_idx,
                    "text": excerpt,
                })
    return snippets
