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


# Mirrors classify_benefits.py's APPLY_CONFIDENCE_LEVELS - kept as a
# separate constant rather than importing the pipeline module, which pulls
# in the Anthropic SDK for no reason here. Keep the two in sync by hand.
_CONFIDENT_LEVELS = ("high", "medium")


def is_high_confidence(record):
    """A benefit is high-confidence if any of its mentions came from a
    certificate's own section header (Tier 1) or a benefit-section bullet
    (Tier 2a/2b) - i.e. not exclusively index terms or sentence-shaped
    criteria, which are more likely to be noise than a real benefit name.
    This is the single place to extend the "hide low-quality entries"
    checkbox with more exclusion criteria later (e.g. revenue-code-style
    names) without touching the UI filtering logic itself.

    llm_review can push a record either direction, not just toward
    exclusion: shape_of() is a heuristic, not a solved classifier, and can
    wrongly tag a real benefit "sentence" (confirmed: "Mental health and
    substance use disorder visits (office, virtual or online visits)" - no
    verb, just long - and "LTACH services if the member's primary
    diagnosis is a mental health or substance use disorder condition" -
    both real, both excluded, neither ever reviewed under the old scope
    gate). Now that classify_benefits.py reviews every non-Tier-1 record
    regardless of shape, a high/medium-confidence "benefit" verdict
    rescues a record from that shape-based exclusion - the mirror image of
    the flag path above. Low-confidence "benefit" verdicts don't rescue,
    same precision-first reasoning as the flag path: surfacing a
    borderline exclusion (still visible in the "Low-Quality / Excluded"
    tab either way) is a smaller error than confidently asserting
    something is clean when the model itself wasn't sure.
    """
    llm_review = record.get("llm_review")
    if llm_review:
        if llm_review.get("applied"):
            return False
        if llm_review["classification"] == "benefit" and llm_review["confidence"] in _CONFIDENT_LEVELS:
            return True
    if 1 in record["tiers_present"]:
        return True
    phrase_count = record["shape_breakdown"].get("phrase", 0)
    sentence_count = record["shape_breakdown"].get("sentence", 0)
    return phrase_count >= sentence_count


def is_top_level_header(record):
    """A Tier 1 record is the certificate's own section header - e.g.
    "Surgery", "Hospital Services", dental's "Class II - Basic Services".
    Deliberately a plain, deterministic tiers_present check rather than an
    LLM judgment call: classify_benefits.py briefly tried having Claude
    decide which Tier-1 headers are "real" benefits vs. administrative
    category labels, but that was inconsistent (two near-duplicate "Class
    I" records differing only by dash character got opposite verdicts) and
    over-eager (flagged legitimate primary navigation categories like
    "Surgery"). Whether to show these broad categories is now a user
    choice (the Benefit Explorer's "include top-level navigation
    categories" toggle), not an automated one.
    """
    return 1 in record["tiers_present"]


def exclusion_reason(record):
    """Human-readable reason a record fails is_high_confidence(), for the
    Benefit Explorer's "Low-Quality / Excluded" tab - the whole point of
    that tab is letting a human judge whether the exclusion is correct, so
    the reason has to be visible, not just the fact of exclusion. Returns
    None if the record isn't excluded.
    """
    if is_high_confidence(record):
        return None
    llm_review = record.get("llm_review")
    if llm_review and llm_review.get("applied"):
        return f"{llm_review['classification']}: {llm_review['reasoning']}"
    return "Mostly sentence-shaped mentions (index terms or criteria/description text), not a clean benefit name"


def get_extracted_doc(doc_id):
    """Lazily load a single Stage 1 extracted-text cache file for a document.
    Returns None if the cache is missing - output/extracted/ (~115MB) is
    excluded from the deploy repo, so a fresh clone won't have it. The
    snippet/full-page-text features degrade to "not available" rather than
    crashing the page. Thin wrapper over pipeline/snippets.py so pipeline
    stages (e.g. classify_benefits.py) can share the same cache/logic
    without depending on the UI layer.
    """
    return _get_extracted_doc(OUTPUT_DIR, doc_id)


def find_snippet(doc_id, page_idx, term, context_chars=80):
    """See pipeline/snippets.py:find_snippet for the full docstring."""
    return _find_snippet(OUTPUT_DIR, doc_id, page_idx, term, context_chars=context_chars)
