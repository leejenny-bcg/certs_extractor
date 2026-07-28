"""Shared "is this benefit record trustworthy" logic - lives here (not
ui/data.py) so pipeline stages that need it (e.g. semantic_match_topic_tree.py,
which should only review high-confidence records) don't depend on the UI
layer, same reasoning as snippets.py's move out of ui/data.py.
"""

# Mirrors classify_benefits.py's APPLY_CONFIDENCE_LEVELS - kept as a
# separate constant rather than importing that module, which pulls in the
# Anthropic SDK for no reason here. Keep the two in sync by hand.
CONFIDENT_LEVELS = ("high", "medium")


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
        if llm_review["classification"] == "benefit" and llm_review["confidence"] in CONFIDENT_LEVELS:
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
