"""Stage 3: extract benefit/procedure name candidates from each cert/rider,
using the Stage 2 section boundaries plus the bullet/font signals validated
by prototyping. Three tiers of candidate, tagged so confidence stays visible:

  Tier 1 - section headers themselves (only from benefit-bearing sections,
           i.e. section_context containing "PAYS FOR" or "COVERAGE FOR" -
           NOT from "WHAT YOU MUST PAY" sections, whose headers are cost
           categories like "Coinsurance Requirements", not benefit names).

  Tier 2a - bullet-hierarchy walk within those same benefit-bearing sections,
            bounded by "We pay for:" / "We do not pay for:" (which also
            tags inclusion covered/excluded). For the Dental profile, a
            bold-font-run at the start of a bullet splits the benefit name
            from its inline description (validated: "Diagnostic and
            preventive services" (bold) "- evaluate existing conditions...").

  Tier 2b - cost-tier bullet walk within "WHAT YOU MUST PAY" sections (all
            cert profiles) AND across the whole document for csr_rider
            profile docs. Handles three shapes found by inspection:
              - "$X for: <bullets>"                    (group header)
              - "N% of the approved amount for: <bullets>" (group header)
              - "$X for <single service>."              (inline, one candidate)
            A bullet that is a group header is not itself a candidate; its
            children are. Parent metadata is the enclosing Stage 2 section
            header (e.g. "Coinsurance Requirements"), not a benefit name.

  Tier 3 - INDEX page terms (two-column pages, fixed via x0-midpoint split),
           mapped back to whichever Stage 2 section's page range contains
           the term's page number.

Every candidate gets a `shape` tag (phrase vs sentence) from a conservative,
visible heuristic - this is explicitly not a solved classifier. Ambiguous
items (e.g. a criterion nested under a benefit, not a new benefit itself)
are tagged, not dropped - resolving that is later/manual work.

Usage:
    python3 extract_candidates.py <extracted_dir> <segments_dir> <output_dir>
"""
import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path

import spacy

from layout import BULLET_CHARS, group_words_into_lines, is_bullet_word, merge_lone_bullet_lines

# parser/ner not needed for POS tagging alone; disabling roughly halves
# per-call latency (see pipeline/normalize.py, same tradeoff for the same
# reason).
_NLP = spacy.load("en_core_web_sm", disable=["parser", "ner"])

BENEFIT_SECTION_RE = re.compile(r"PAYS FOR|COVERAGE FOR")
PAY_SECTION_RE = re.compile(r"WHAT YOU MUST PAY")

WE_PAY_FOR_RE = re.compile(r"^we pay for\b", re.IGNORECASE)
WE_DO_NOT_PAY_FOR_RE = re.compile(r"^we do not pay for\b", re.IGNORECASE)

SEE_SECTION_HELPER_RE = re.compile(r"^see section \d+ beginning on page", re.IGNORECASE)
LOCATIONS_LINE_RE = re.compile(r"^locations:", re.IGNORECASE)
LETTERHEAD_MAX_SIZE = 9.0

# A bullet ending in a bare "to <verb>:" (nothing between the infinitive and
# the colon) is introducing a list of things being identified/determined/
# etc, not naming a benefit itself (e.g. "Medication assessments to
# identify:"). Deliberately narrow - a colon preceded by more than one word
# (e.g. "...limited to those described below:") is often a legitimate
# standalone name that just happens to introduce children too.
BARE_INFINITIVE_COLON_RE = re.compile(r"\bto\s+\w+:$")
# Same "group header for its own children" shape, different ending: a bare
# copula/modal right before the colon (e.g. "The optometrist is:" ->
# provider-licensing criteria; "...biologicals must be:" -> drug-eligibility
# criteria). Also narrow on purpose, same reasoning as above.
GROUP_HEADER_COPULA_RE = re.compile(r"\b(is|are|must be|will be):$", re.IGNORECASE)

COST_TIER_GROUP_HEADER_RE = re.compile(
    r"^(\$[\d,]+(\.\d+)?\s+for:|"
    r"\d{1,3}%\s+of the approved amount for:|"
    r".*following (covered )?services.*:)$",
    re.IGNORECASE,
)
COST_TIER_INLINE_RE = re.compile(r"^\$[\d,]+(\.\d+)?\s+for\s+(?P<service>.+?)\.?$", re.IGNORECASE)
# Deductible/OOP-max bullets are consistently "$X for one member" / "$X for
# the family (...)" - a household-size split, not a named service. Every
# doc in the corpus repeats this exact pair, so it's worth excluding by name
# rather than accepting it as noise.
HOUSEHOLD_SIZE_RE = re.compile(r"^(one member|the family\b.*)$", re.IGNORECASE)

CRITERION_WORDS = {"when", "if", "unless", "because", "must", "will", "does", "should", "shall"}
# A benefit/procedure name is a noun phrase - it doesn't open with a finite
# verb. A leading copula/modal is a strong, cheap signal that this is a
# criterion/condition clause instead (e.g. "Are covered under your
# certificate", "Can be split over a short fill period..."), which
# CRITERION_WORDS' substring-anywhere check misses when the trigger word
# isn't literally "if"/"when"/etc.
LEADING_VERB_WORDS = {"are", "is", "can", "will", "does", "has", "have", "was", "were", "do", "did", "should", "shall", "may", "might", "must"}

# Generic/administrative descriptors that sit at the exact same bullet depth
# as real named benefits in the source (e.g. "Individual psychotherapeutic
# treatment" and "Services provided by the hospital's or facility's staff"
# under the same "We pay for:" list) - no structural signal (font, glyph,
# depth) distinguishes them, only the lexical pattern. Confirmed against 6
# real examples (all caught) and 10 known-good benefit names (0 false
# positives) before adding.
AGENT_CLAUSE_RE = re.compile(
    r"\b(provided|given|required|received|furnished|administered|billed|ordered|prescribed|dispensed|performed|rendered|supervised)\s+(by|from)\b",
    re.IGNORECASE,
)
PAYMENT_FOR_RE = re.compile(r"^payment for\b", re.IGNORECASE)
# "do(es) not meet X" and "have/has not been X" are both exclusion-criterion
# shapes ("Treatment...that do not meet BCBSM requirements", "Services that
# have not been preapproved") - same underlying pattern, different verb.
NOT_MEET_RE = re.compile(r"\bdo(?:es)? not meet\b|\bhas not been\b|\bhave not been\b", re.IGNORECASE)


def contains_finite_verb(text):
    """A real benefit name, however long, is a noun phrase - no verb
    anywhere in it. A genuine description/criterion sentence almost
    always has one. Replaces a pure word-count proxy that mis-tagged
    long-but-verbless phrases as "sentence" - confirmed: "Mental health
    and substance use disorder visits (office, virtual or online visits)"
    (12 words, no verb) was wrongly excluded, and never even reached LLM
    review because of it (the review scope gate skips anything already
    shape-tagged "sentence").

    Deliberately narrower than "any VERB/AUX token": a bare check flags
    legitimate long benefit names that contain an infinitive-of-purpose
    ("Services TO TREAT temporomandibular joint dysfunction...") or a
    participial modifier ("...limited to those described below") - both
    common, neither a real assertion. Content verbs only count in present
    tense (VBZ/VBP - "is", "requires"); past tense (VBD) is excluded
    because spaCy's tagger, with no surrounding sentence, confirmed
    mistagging a participial modifier as VBD ("limited" in the TMJ
    example above, should be VBN). Auxiliaries (is/are/was/were/have/
    has/do/does) count in any tense - "was"/"were" aren't participle-
    homographs the way "limited"/"required"/"described" are, so the same
    ambiguity doesn't apply."""
    for tok in _NLP(text):
        if tok.pos_ == "AUX" and tok.tag_ in ("VBZ", "VBP", "VBD"):
            return True
        if tok.pos_ == "VERB" and tok.tag_ in ("VBZ", "VBP"):
            return True
    return False


def shape_of(text):
    """Conservative phrase-vs-sentence heuristic. Not a solved classifier -
    ambiguous items still get emitted, just tagged lower-confidence."""
    words = text.strip().rstrip(".").split()
    if not words:
        return "sentence"
    lower_words = {w.lower().strip(",:;") for w in words}
    if words[0].lower().strip(",:;") in LEADING_VERB_WORDS:
        return "sentence"
    # Extreme outlier backstop (rare) - a genuinely enormous candidate is
    # almost certainly not a clean benefit name regardless of structure.
    # Between the old threshold and this one, verb presence (not length
    # alone) decides - see contains_finite_verb().
    if len(words) > 25:
        return "sentence"
    if len(words) > 10 and contains_finite_verb(text):
        return "sentence"
    if lower_words & CRITERION_WORDS:
        return "sentence"
    if re.search(r"\b\d{1,3}%\b", text) and len(words) > 4:
        return "sentence"
    if AGENT_CLAUSE_RE.search(text) or PAYMENT_FOR_RE.match(text) or NOT_MEET_RE.search(text):
        return "sentence"
    return "phrase"


def is_letterhead_or_noise(line_words, line_text_str):
    if all(w.get("size", 0) <= LETTERHEAD_MAX_SIZE for w in line_words):
        return True
    if SEE_SECTION_HELPER_RE.match(line_text_str.strip()):
        return True
    # NOT LOCATIONS_LINE_RE here - it used to be filtered out here, which
    # meant its facility-type bullets (which aren't filtered) flowed into
    # walk_benefit_bullets with no record of what block they belonged to.
    # walk_benefit_bullets needs to see this line itself to know to skip the
    # bullet run that follows.
    if re.match(r"^SECTION \d+:", line_text_str.strip()):
        return True
    if "Blue Cross Blue Shield of Michigan" in line_text_str:
        return True
    return False


def bullet_depth_ranker(section_lines):
    """Rank distinct bullet x0 values seen in this section, ascending, so
    depth is relative to what's actually in THIS section/profile rather than
    a hardcoded pixel threshold (x0 conventions differ slightly by family)."""
    x0s = sorted({round(l["x0"], 0) for l in section_lines if l["is_bullet"]})
    return {x0: i for i, x0 in enumerate(x0s)}


def build_section_lines(pages, start_page, end_page, header_text, start_top=None, boundary=None):
    """Flatten a section's pages into a noise-filtered line list, each with
    bullet-ness, x0 (if bullet), first-word font/size, and joined text.

    Two boundary bugs matter here, symmetric to each other: Stage 2's
    end_page is "wherever the next section starts" (often the same page as
    this section's tail), so without an upper bound the next section's
    bullets bleed in; and start_page alone doesn't rule out the *previous*
    section's tail sharing this section's start_page above its own header.
    `start_top` is this section's own header position (lower bound);
    `boundary` is the next section's (page, top) (upper bound), or None for
    the last section in a document.
    """
    lines = []
    for page_idx in range(start_page, min(end_page + 1, len(pages))):
        page = pages[page_idx]
        page_lines = merge_lone_bullet_lines(group_words_into_lines(page["words"]))
        for top, line_words in page_lines:
            if start_top is not None and page_idx == start_page and top < start_top:
                continue
            if boundary is not None and page_idx == boundary[0] and top >= boundary[1]:
                continue
            text = " ".join(w["text"] for w in line_words)
            stripped = text.strip()
            if stripped == header_text.strip():
                continue
            if re.match(rf"^{re.escape(header_text.strip())}\s*\(continued\)$", stripped, re.IGNORECASE):
                continue
            if is_letterhead_or_noise(line_words, stripped):
                continue
            first = line_words[0]
            lines.append(
                {
                    "page": page_idx,
                    "top": top,
                    "text": stripped,
                    "is_bullet": is_bullet_word(first),
                    "x0": first["x0"] if is_bullet_word(first) else None,
                    "words": line_words,
                }
            )
    return lines


def bold_split(line_words):
    """Dental-profile signal: if a bullet's first run of words is bold and
    the rest isn't, the bold run is the benefit name, the rest is inline
    description. Returns (name, has_split)."""
    bold_words = []
    for w in line_words:
        if "Bold" in w.get("fontname", "") and "Italic" not in w.get("fontname", ""):
            bold_words.append(w["text"])
        else:
            break
    if bold_words and len(bold_words) < len(line_words):
        return " ".join(bold_words), True
    return None, False


def strip_leading_bullet(text):
    if text and text[0] in BULLET_CHARS:
        return text[1:].strip()
    return text.strip()


def strip_trailing_colon(text):
    """A candidate's own trailing colon is never part of its name - it's
    either a group header that also happens to read as a standalone benefit
    (e.g. "Chiropractic office visits:", deliberately kept as a candidate
    rather than demoted, see BARE_INFINITIVE_COLON_RE above) or a narrower
    group header GROUP_HEADER_COPULA_RE/BARE_INFINITIVE_COLON_RE didn't
    catch. Either way, strip it for the final candidate text; it never
    changes shape_of()'s classification (checked against both example
    categories before adding)."""
    text = text.rstrip()
    return text[:-1].rstrip() if text.endswith(":") else text


# A candidate ending in a bare page cross-reference (", Page 86" or
# "(Page 86)") is citing where the SAME concept has its own full benefit
# section elsewhere in the certificate - confirmed against the source PDF:
# "Occupational therapy, Page 73" / "Physical therapy, Page 86" / "Speech
# language therapy, Page 121" are nested under "The following when
# provided for rehabilitation:" in Home Health Care Services, and each of
# those three names already has its own full Tier 1 section elsewhere.
# Since every document has different pagination, the literal page number
# differs per document and silently blocks the cross-document merge that
# should otherwise unify these with their real canonical entry. The page
# number is never part of the benefit's name, so stripping it is safe.
TRAILING_PAGE_REF_RE = re.compile(r"[,.]?\s*\(?page\s+\d+\)?\.?\s*$", re.IGNORECASE)

# Same cross-reference, worded as a full clause instead of a bare page
# number - confirmed against the source PDF: "Physical therapy (see Page
# 86 for physical therapy services)" under a Dental/TMJ We-pay-for list,
# citing the same "Physical Therapy" benefit's own dedicated section. The
# "for ..." content is never new information about the benefit (it's
# always a restatement/description of what's at that page), so the whole
# parenthetical is safe to drop, not just the digits inside it. Matched
# structurally ("(see Page N for ...)") rather than against specific
# wording so it generalizes to whatever follows "for".
TRAILING_SEE_PAGE_REF_RE = re.compile(r"\s*\(see page\s+\d+ for [^()]*\)\.?\s*$", re.IGNORECASE)

# A benefit name never legitimately ends in a dangling conjunction - this
# only shows up as leftover debris after stripping a trailing page-ref
# clause from source text that itself has a stray word (confirmed: one
# document's own PDF text literally reads "Physical therapy or (see Page
# 83 for physical therapy services)", an apparent typo in BCBSM's source,
# not our extraction). Deliberately only applied right after a page-ref
# strip, not generally, since a mid-sentence fragment ending in "or"/"and"
# elsewhere isn't the same situation.
DANGLING_CONJUNCTION_RE = re.compile(r"\s+(or|and)\s*$", re.IGNORECASE)


def strip_trailing_page_reference(text):
    without_clause = TRAILING_SEE_PAGE_REF_RE.sub("", text)
    if without_clause != text:
        without_clause = DANGLING_CONJUNCTION_RE.sub("", without_clause).rstrip()
        return without_clause if without_clause else text
    stripped = TRAILING_PAGE_REF_RE.sub("", text).rstrip()
    return stripped if stripped else text


def clean_candidate_text(text):
    return strip_trailing_colon(strip_trailing_page_reference(text))


TERMINAL_PUNCT = (".", "!", "?", ":")


def try_merge_continuation(last_candidate, line_text):
    """A non-bullet line following a bullet is either a genuine multi-line
    wrap of that bullet's text (e.g. "...independent laboratory or" /
    "physician's office" split across a page-width wrap - confirmed in the
    source PDF, not a byproduct of our own line-grouping) or a new,
    unrelated transition sentence. "Prior text lacks terminal punctuation"
    alone isn't a strong enough signal - most of our clean short candidate
    names ("Allergy Testing", "A pre-surgical consultation...") never end in
    punctuation at all, so that check alone kept absorbing whatever sentence
    happened to follow. The reliable signal is the continuation line's own
    first character: a genuine wrap is still mid-sentence, so it starts
    lowercase ("physician's office"); an unrelated new sentence starts
    capitalized ("Your copayment is applied...").

    One exception to the lowercase check: a wrap that splits mid-parenthetical
    (e.g. "...occupational therapy (Page" / "71) when medically necessary" -
    confirmed in the source PDF) continues with whatever the parenthetical's
    content starts with, which can be a digit rather than a lowercase letter.
    An unclosed "(" - more "("s than ")"s so far - is an unambiguous "this is
    not a complete sentence yet" signal on its own, independent of
    capitalization. Returns True if merged.
    """
    if last_candidate is None:
        return False
    if last_candidate["text"].rstrip().endswith(TERMINAL_PUNCT):
        return False
    mid_parenthetical = last_candidate["text"].count("(") > last_candidate["text"].count(")")
    if not line_text or not (line_text[0].islower() or mid_parenthetical):
        return False
    merged_text = clean_candidate_text(f"{last_candidate['text']} {line_text}".strip())
    last_candidate["text"] = merged_text
    last_candidate["shape"] = shape_of(merged_text)
    return True


def is_local_subheader(line):
    """A standalone bold (non-italic), body-size line that isn't a We-pay-
    for/We-do-not-pay-for marker - e.g. "Mandatory Prior Authorization" or
    "Medication Synchronization" nested inside a long multi-topic Tier 1
    section like "Prescription Drugs". These use the exact same font as the
    We-pay-for markers (Arial-BoldMT ~11pt), which is why this check only
    runs after both marker regexes have already failed to match. Without
    treating these as inclusion-reset points, a "we do not pay for" from an
    earlier, unrelated sub-topic keeps applying to every later sub-topic
    that never states its own coverage stance - stale state, not a real
    exclusion.
    """
    first = line["words"][0]
    fontname = first.get("fontname", "")
    return "Bold" in fontname and "Italic" not in fontname and 10.5 <= first.get("size", 0) <= 11.5


def walk_benefit_bullets(lines, header_text, section_context, dental_split, default_inclusion=None):
    """Tier 2a: walk the We-pay-for/We-do-not-pay-for bounded bullet tree.

    PPO Medical/Vision sections always open with an explicit "We pay for:"
    marker, so bullets before it (e.g. a "Locations:" list) are correctly
    ignored by requiring inclusion to be set first. The Dental profile has
    no such per-section marker at all - Class I/II/III just enumerate
    covered items directly, with real exclusions living in a separate
    Section 4 - so it needs `default_inclusion="covered"` or every one of
    its bullets gets silently dropped waiting for a marker that never comes.

    Two things need handling independent of `inclusion` state entirely,
    because relying on marker-matching to happen to be in the right state
    at the right time proved fragile in practice (see the "An office" bug):

    - A "Locations:" bullet run (facility types, not benefits) needs to be
      skipped even when a generic summary sentence earlier in the section
      (e.g. "We pay for professional, hospital and facility services to
      treat the underlying causes of infertility.") happened to already
      match WE_PAY_FOR_RE and set inclusion to "covered" before the real
      list-introducing marker appears.
    - A bullet that's a bare infinitive clause ending in a colon (e.g.
      "Medication assessments to identify:") is a group header for its own
      children, not a benefit itself - narrower than "any colon-ending
      bullet" on purpose, since some colon-ending bullets ARE legitimate
      standalone names (e.g. "Services to treat temporomandibular joint
      dysfunction (TMJ) limited to those described below:").
    """
    candidates = []
    depth_rank = bullet_depth_ranker(lines)
    inclusion = default_inclusion
    stack_text_by_depth = {}
    last_candidate = None
    skipping_locations = False

    for line in lines:
        text = line["text"]

        if LOCATIONS_LINE_RE.match(text.strip()):
            skipping_locations = True
            last_candidate = None
            continue
        if skipping_locations:
            if line["is_bullet"]:
                continue
            skipping_locations = False
            # fall through - this non-bullet line (often the real "We pay
            # for:" marker) still needs normal handling below.

        if WE_PAY_FOR_RE.match(text):
            inclusion = "covered"
            last_candidate = None
            continue
        if WE_DO_NOT_PAY_FOR_RE.match(text):
            inclusion = "excluded"
            last_candidate = None
            continue
        if not line["is_bullet"] and is_local_subheader(line):
            inclusion = default_inclusion
            last_candidate = None
            continue
        if not line["is_bullet"]:
            if inclusion is not None and not try_merge_continuation(last_candidate, text):
                last_candidate = None
            continue
        if inclusion is None:
            continue

        depth = depth_rank.get(round(line["x0"], 0), 0)
        raw = strip_leading_bullet(text)

        if BARE_INFINITIVE_COLON_RE.search(raw) or GROUP_HEADER_COPULA_RE.search(raw):
            # Group header for its children, not a candidate itself - still
            # tracked in stack_text_by_depth so children get the right
            # immediate_parent.
            stack_text_by_depth[depth] = raw
            last_candidate = None
            continue

        candidate_text = raw
        did_split = False
        if dental_split:
            split_name, did_split = bold_split(line["words"][1:])  # skip bullet glyph word
            if did_split:
                candidate_text = split_name
        candidate_text = clean_candidate_text(candidate_text)

        parent = stack_text_by_depth.get(depth - 1) if depth > 0 else None
        stack_text_by_depth[depth] = candidate_text

        new_candidate = {
            "text": candidate_text,
            "tier": 2,
            "subtier": "2a",
            "parent_header": header_text,
            "immediate_parent": parent,
            "nesting_depth": depth,
            "inclusion": inclusion,
            "shape": shape_of(candidate_text),
            "section_context": section_context,
            "source_page": line["page"],
        }
        candidates.append(new_candidate)
        # A bold-split candidate's text is already the clean name with its
        # inline description deliberately discarded - if that description
        # wraps to a second physical line, it belongs to the discarded part,
        # not the name, so it must not become eligible for continuation-merge.
        last_candidate = None if did_split else new_candidate
    return candidates


def walk_cost_tier_bullets(lines, header_text, section_context):
    """Tier 2b: cost-tier ($ or % group headers, or inline $-for-service)."""
    candidates = []
    depth_rank = bullet_depth_ranker(lines)
    group_active_depth = None
    last_candidate = None

    for line in lines:
        if not line["is_bullet"]:
            if not try_merge_continuation(last_candidate, line["text"]):
                last_candidate = None
            continue
        raw = strip_leading_bullet(line["text"])
        depth = depth_rank.get(round(line["x0"], 0), 0)

        inline_match = COST_TIER_INLINE_RE.match(raw)
        if inline_match:
            candidate_text = clean_candidate_text(inline_match.group("service").strip())
            if HOUSEHOLD_SIZE_RE.match(candidate_text):
                group_active_depth = None
                last_candidate = None
                continue
            new_candidate = {
                "text": candidate_text,
                "tier": 2,
                "subtier": "2b",
                "parent_header": header_text,
                "immediate_parent": None,
                "nesting_depth": depth,
                "inclusion": "covered",
                "shape": shape_of(candidate_text),
                "section_context": section_context,
                "source_page": line["page"],
            }
            candidates.append(new_candidate)
            last_candidate = new_candidate
            group_active_depth = None
            continue

        if COST_TIER_GROUP_HEADER_RE.match(raw):
            group_active_depth = depth
            last_candidate = None
            continue

        if group_active_depth is not None and depth > group_active_depth:
            candidate_text = clean_candidate_text(raw)
            new_candidate = {
                "text": candidate_text,
                "tier": 2,
                "subtier": "2b",
                "parent_header": header_text,
                "immediate_parent": None,
                "nesting_depth": depth,
                "inclusion": "covered",
                "shape": shape_of(candidate_text),
                "section_context": section_context,
                "source_page": line["page"],
            }
            candidates.append(new_candidate)
            last_candidate = new_candidate
        elif group_active_depth is not None and depth <= group_active_depth:
            group_active_depth = None
            last_candidate = None

    return candidates


INDEX_ENTRY_RE = re.compile(r"^(?P<term>.+?)\s*\.{2,}\s*(?P<page>\d+)$")
LEADING_PAGE_NUM_RE = re.compile(r"^(\d{1,4})\s+SECTION\s+\d+:", re.MULTILINE)
TRAILING_PAGE_NUM_RE = re.compile(r"SECTION\s+\d+:[^\n]*?(\d{1,4})\s*$", re.MULTILINE)


def compute_printed_page_offset(pages):
    """BCBSM certs footer each page with the document's own printed page
    counter (e.g. "SECTION 3: COVERAGE FOR VISION CARE SERVICES 10"), which
    the INDEX page's dot-leader entries reference - NOT the absolute PDF
    page index. Confirmed by inspection: for one Vision cert, absolute index
    = printed number + 7, constant across 40+ sampled pages (no resets
    mid-document). Printed numbers can appear before OR after the "SECTION
    N:" text depending on left/right page folio position, hence two regexes.
    Returns the most common (absolute_index - printed_number) offset found,
    or 0 if no footer pattern is found anywhere (safe fallback, not a claim
    of correctness for that document).
    """
    offsets = Counter()
    for page_idx, page in enumerate(pages):
        text = page["raw_text"]
        m = LEADING_PAGE_NUM_RE.search(text) or TRAILING_PAGE_NUM_RE.search(text)
        if m:
            offsets[page_idx - int(m.group(1))] += 1
    if not offsets:
        return 0
    return offsets.most_common(1)[0][0]


def extract_index_entries(pages, sections_by_page, page_offset):
    """Tier 3: find INDEX pages, split the two columns by x-midpoint, and
    pull term/page-number pairs, mapped back to the nearest Stage 2 section.
    Raw page numbers are the document's printed counter, converted to an
    absolute page index via `page_offset` before being used for anything."""
    entries = []
    num_pages = len(pages)
    for page_idx, page in enumerate(pages):
        lines_plain = [l.strip().lower() for l in page["raw_text"].split("\n")]
        if "index" not in lines_plain:
            continue
        words = page["words"]
        if not words:
            continue
        mid_x = (min(w["x0"] for w in words) + max(w["x0"] for w in words)) / 2
        left = [w for w in words if w["x0"] < mid_x]
        right = [w for w in words if w["x0"] >= mid_x]
        for col in (left, right):
            for top, line_words in group_words_into_lines(col):
                text = " ".join(w["text"] for w in line_words)
                m = INDEX_ENTRY_RE.match(text.strip())
                if not m:
                    continue
                term = clean_candidate_text(m.group("term").strip())
                printed_page = int(m.group("page"))
                absolute_page = printed_page + page_offset
                in_range = 0 <= absolute_page < num_pages
                parent = sections_by_page.get(absolute_page) if in_range else None
                # An INDEX term whose page doesn't resolve to any
                # benefit-bearing section is landing in Definitions,
                # Appeals, General Conditions, etc. (e.g. "Coinsurance",
                # "Adverse Benefit Decision", "BCBSM") - the back-of-book
                # index covers every topic in the certificate, not just
                # benefits, and this is the clean signal for "not a
                # benefit" that was already being computed but unused.
                shape = shape_of(term) if parent is not None else "sentence"
                entries.append(
                    {
                        "text": term,
                        "tier": 3,
                        "subtier": "3",
                        "parent_header": parent,
                        "immediate_parent": None,
                        "nesting_depth": None,
                        "inclusion": "unknown",
                        "shape": shape,
                        "section_context": None,
                        "source_page": absolute_page if in_range else None,
                    }
                )
    return entries


def page_to_section_lookup(sections):
    lookup = {}
    for s in sections:
        for p in range(s["start_page"], s["end_page"] + 1):
            lookup.setdefault(p, s["header"])
    return lookup


def extract_one(record, segmentation):
    profile = segmentation["profile"]
    if profile == "skip":
        return {"doc_id": record["doc_id"], "profile": profile, "candidates": []}

    candidates = []
    pages = record["pages"]
    sections = segmentation["sections"]

    def next_boundary(i):
        if i + 1 >= len(sections):
            return None
        nxt = sections[i + 1]
        if nxt.get("start_top") is None:
            return None
        return (nxt["start_page"], nxt["start_top"])

    if profile == "csr_rider":
        for i, section in enumerate(sections):
            lines = build_section_lines(
                pages,
                section["start_page"],
                section["end_page"],
                section["header"],
                start_top=section.get("start_top"),
                boundary=next_boundary(i),
            )
            candidates.extend(walk_cost_tier_bullets(lines, section["header"], None))
        return {"doc_id": record["doc_id"], "profile": profile, "candidates": candidates}

    # cert profiles: ppo_medical / vision / dental
    for i, section in enumerate(sections):
        ctx = section["section_context"] or ""
        header = section["header"]
        boundary = next_boundary(i)

        if BENEFIT_SECTION_RE.search(ctx):
            candidates.append(
                {
                    "text": clean_candidate_text(header),
                    "tier": 1,
                    "subtier": "1",
                    "parent_header": None,
                    "immediate_parent": None,
                    "nesting_depth": None,
                    "inclusion": "covered",
                    "shape": "phrase",
                    "section_context": ctx,
                    "source_page": section["start_page"],
                }
            )
            lines = build_section_lines(
                pages, section["start_page"], section["end_page"], header, start_top=section["start_top"], boundary=boundary
            )
            candidates.extend(
                walk_benefit_bullets(lines, header, ctx, dental_split=(profile == "dental"), default_inclusion=("covered" if profile == "dental" else None))
            )

        elif PAY_SECTION_RE.search(ctx):
            lines = build_section_lines(
                pages, section["start_page"], section["end_page"], header, start_top=section["start_top"], boundary=boundary
            )
            candidates.extend(walk_cost_tier_bullets(lines, header, ctx))

    sections_by_page = page_to_section_lookup([s for s in sections if BENEFIT_SECTION_RE.search(s["section_context"] or "")])
    page_offset = compute_printed_page_offset(pages)
    candidates.extend(extract_index_entries(pages, sections_by_page, page_offset))

    return {"doc_id": record["doc_id"], "profile": profile, "candidates": candidates}


def cache_path_for(output_dir, relative_path):
    safe_name = relative_path.replace("/", "__").replace(" ", "_")
    return Path(output_dir) / f"{safe_name}.json"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("extracted_dir", type=Path)
    parser.add_argument("segments_dir", type=Path)
    parser.add_argument("output_dir", type=Path)
    args = parser.parse_args()

    args.output_dir.mkdir(parents=True, exist_ok=True)

    extracted_files = sorted(args.extracted_dir.glob("*.json"))
    print(f"Found {len(extracted_files)} extracted records", file=sys.stderr)

    tier_counts = {}
    for f in extracted_files:
        with open(f) as fh:
            record = json.load(fh)
        seg_path = args.segments_dir / f.name
        with open(seg_path) as fh:
            segmentation = json.load(fh)

        result = extract_one(record, segmentation)
        out_path = cache_path_for(args.output_dir, record["relative_path"])
        with open(out_path, "w") as fh:
            json.dump(result, fh, indent=2)

        for c in result["candidates"]:
            key = f"tier{c['tier']}"
            tier_counts[key] = tier_counts.get(key, 0) + 1

        print(f"{record['relative_path'][:70]:70} -> {len(result['candidates']):4} candidates", file=sys.stderr)

    print("\n--- summary ---", file=sys.stderr)
    for tier, count in sorted(tier_counts.items()):
        print(f"{tier}: {count}", file=sys.stderr)


if __name__ == "__main__":
    main()
