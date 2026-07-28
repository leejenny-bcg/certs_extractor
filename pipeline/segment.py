"""Stage 2: segment each cert/rider into header-bounded sections, using the
per-profile structural signals validated by prototyping:

- ppo_medical / vision / dental certs: benefit headers render in
  TimesNewRomanPS-BoldItalicMT ~14pt (confirmed identical across all three
  cert families). Repeat headers after a page break instead render as
  "<Title> (continued)" in Arial-BoldMT ~11pt - a different, weaker signal,
  so it's only trusted when the title matches a header already seen on an
  earlier page in the same document (excluding the "We pay for:" / "We do
  not pay for:" bold markers, which use the same font but are not headers).
- csr_rider (the 9 Med Rx CSR riders): there is no benefit-name header at
  all. The only standalone headings are a closed, empirically-observed
  vocabulary (Deductible/Copayment/Coinsurance Requirements) that bound the
  "$X for: <services>" bullets Stage 3 will parse.
- skip: no segmentation - these riders were confirmed (by reading full text)
  to introduce no new benefit names.

Each page also gets tagged with its enclosing "SECTION N: TITLE" context,
read off the certificate's own running footer (e.g. "SECTION 3: WHAT BCBSM
PAYS FOR 21") - this is BCBSM's own page-level section marker, not something
we're inferring, so it's a cheap and reliable way to know which top-level
section (benefits vs. exclusions vs. definitions) each header falls under.

Usage:
    python3 segment.py <extracted_dir> <output_dir>
"""
import argparse
import json
import re
import sys
from pathlib import Path

from family_profiles import classify
from layout import group_words_into_lines

HEADER_FONT_HINT = "TimesNewRomanPS-BoldItalicMT"
HEADER_SIZE_RANGE = (12.5, 15.5)
CONTINUED_FONT_HINT = "Arial-BoldMT"
CONTINUED_SIZE_RANGE = (10.5, 11.5)
CONTINUED_SUFFIX_RE = re.compile(r"^(.*?)\s*\(continued\)$", re.IGNORECASE)
NOT_A_HEADER_PREFIXES = ("we pay for", "we do not pay for")

FOOTER_SECTION_RE = re.compile(r"SECTION (\d+): ([A-Z0-9 ,'\"/()-]{3,80})")

# Empirically observed (not guessed) across all 9 CSR riders - see prototyping.
CSR_HEADING_VOCAB = {"Deductible Requirements", "Copayment Requirements", "Coinsurance Requirements"}


def line_text(line_words):
    return " ".join(w["text"] for w in line_words)


def detect_section_context(raw_text):
    """Last 'SECTION N: TITLE' footer match on the page, title with trailing
    page-number digits stripped."""
    matches = FOOTER_SECTION_RE.findall(raw_text)
    if not matches:
        return None
    num, title = matches[-1]
    title = re.sub(r"\s*\d+\s*$", "", title).strip()
    return f"SECTION {num}: {title}"


def find_headers_in_cert(pages):
    """Returns a list of header dicts: {text, page, top, section_context,
    continued_from_page (bool)}, in document order."""
    headers = []
    seen_header_texts = set()

    for page_idx, page in enumerate(pages):
        section_context = detect_section_context(page["raw_text"])
        lines = group_words_into_lines(page["words"])
        for top, line_words in lines:
            if not line_words:
                continue
            first = line_words[0]
            text = line_text(line_words)

            is_primary = (
                HEADER_FONT_HINT in first.get("fontname", "")
                and HEADER_SIZE_RANGE[0] <= first.get("size", 0) <= HEADER_SIZE_RANGE[1]
            )
            if is_primary:
                headers.append(
                    {
                        "text": text,
                        "page": page_idx,
                        "top": top,
                        "section_context": section_context,
                        "continued": False,
                    }
                )
                seen_header_texts.add(text.strip().lower())
                continue

            is_bold_continued_candidate = (
                CONTINUED_FONT_HINT in first.get("fontname", "")
                and CONTINUED_SIZE_RANGE[0] <= first.get("size", 0) <= CONTINUED_SIZE_RANGE[1]
            )
            if is_bold_continued_candidate:
                m = CONTINUED_SUFFIX_RE.match(text)
                if m:
                    base = m.group(1).strip()
                    base_lower = base.lower()
                    if base_lower in NOT_A_HEADER_PREFIXES or any(
                        base_lower.startswith(p) for p in NOT_A_HEADER_PREFIXES
                    ):
                        continue
                    if base_lower in seen_header_texts:
                        headers.append(
                            {
                                "text": base,
                                "page": page_idx,
                                "top": top,
                                "section_context": section_context,
                                "continued": True,
                            }
                        )

    return headers


def headers_to_sections(headers, num_pages):
    """Turn a flat header list into sections, merging "continued" headers
    into the section they continue rather than starting a new one."""
    sections = []
    for h in headers:
        if h["continued"] and sections and sections[-1]["header"].strip().lower() == h["text"].strip().lower():
            sections[-1]["end_page"] = h["page"]
            continue
        sections.append(
            {
                "header": h["text"],
                "section_context": h["section_context"],
                "start_page": h["page"],
                "start_top": h["top"],
                "end_page": h["page"],
            }
        )

    # each section's true end_page is wherever the *next distinct* section starts
    for i in range(len(sections) - 1):
        sections[i]["end_page"] = max(sections[i]["end_page"], sections[i + 1]["start_page"])
    if sections:
        sections[-1]["end_page"] = max(sections[-1]["end_page"], num_pages - 1)
    return sections


def find_csr_rider_sections(pages):
    sections = []
    for page_idx, page in enumerate(pages):
        for top, line_words in group_words_into_lines(page["words"]):
            text = line_text(line_words).strip()
            if text in CSR_HEADING_VOCAB:
                sections.append(
                    {"header": text, "section_context": None, "start_page": page_idx, "start_top": top, "end_page": page_idx}
                )
    for i in range(len(sections) - 1):
        sections[i]["end_page"] = max(sections[i]["end_page"], sections[i + 1]["start_page"])
    if sections:
        sections[-1]["end_page"] = max(sections[-1]["end_page"], len(pages) - 1)
    return sections


def segment_one(record):
    profile = classify(record)
    if profile in ("ppo_medical", "vision", "dental"):
        headers = find_headers_in_cert(record["pages"])
        sections = headers_to_sections(headers, record["num_pages"])
    elif profile == "csr_rider":
        sections = find_csr_rider_sections(record["pages"])
    else:
        sections = []

    return {
        "doc_id": record["doc_id"],
        "relative_path": record["relative_path"],
        "profile": profile,
        "num_pages": record["num_pages"],
        "num_sections": len(sections),
        "sections": sections,
    }


def cache_path_for(output_dir, relative_path):
    safe_name = relative_path.replace("/", "__").replace(" ", "_")
    return Path(output_dir) / f"{safe_name}.json"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("extracted_dir", type=Path)
    parser.add_argument("output_dir", type=Path)
    args = parser.parse_args()

    args.output_dir.mkdir(parents=True, exist_ok=True)

    extracted_files = sorted(args.extracted_dir.glob("*.json"))
    print(f"Found {len(extracted_files)} extracted records", file=sys.stderr)

    profile_counts = {}
    section_counts = {}
    for f in extracted_files:
        with open(f) as fh:
            record = json.load(fh)
        result = segment_one(record)
        out_path = cache_path_for(args.output_dir, record["relative_path"])
        with open(out_path, "w") as fh:
            json.dump(result, fh, indent=2)

        profile_counts[result["profile"]] = profile_counts.get(result["profile"], 0) + 1
        section_counts[result["profile"]] = section_counts.get(result["profile"], 0) + result["num_sections"]
        print(f"{record['relative_path'][:70]:70} -> {result['profile']:12} {result['num_sections']:3} sections", file=sys.stderr)

    print("\n--- summary ---", file=sys.stderr)
    for profile, count in sorted(profile_counts.items()):
        print(f"{profile:12} {count:3} docs, {section_counts[profile]:4} total sections", file=sys.stderr)


if __name__ == "__main__":
    main()
