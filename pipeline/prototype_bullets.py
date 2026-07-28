"""Prototype: check whether bullet-glyph + indentation + bold-font conventions
for benefit lists hold consistently across the different cert/rider templates
(PPO medical, Vision, Dental, Riders) before building the real Stage 3 parser.

Usage:
    python3 prototype_bullets.py <pdf_path> [--pages 24,25,26] [--max-pages 400]
"""
import argparse
from collections import defaultdict

import pdfplumber

from layout import BULLET_CHARS, group_words_into_lines


def describe_line(line_words):
    first = line_words[0]
    text = " ".join(w["text"] for w in line_words)
    is_bullet = first["text"] in BULLET_CHARS
    bullet_char = first["text"] if is_bullet else None
    bold = any("Bold" in w.get("fontname", "") for w in line_words[:3])
    x0 = round(first["x0"], 1)
    return {
        "x0": x0,
        "bullet_char": bullet_char,
        "bold_start": bold,
        "text": text,
    }


def analyze_pdf(path, page_indices=None, max_pages=None):
    print(f"\n{'=' * 90}\n{path}\n{'=' * 90}")
    with pdfplumber.open(path) as pdf:
        pages = pdf.pages
        if page_indices is not None:
            targets = [i for i in page_indices if i < len(pages)]
        else:
            targets = range(len(pages) if max_pages is None else min(max_pages, len(pages)))

        bullet_x0_by_char = defaultdict(set)
        bold_boundary_lines = []
        sample_lines_printed = 0

        for i in targets:
            page = pages[i]
            words = page.extract_words(extra_attrs=["fontname"])
            if not words:
                continue
            lines = group_words_into_lines(words)
            for _, line_words in lines:
                d = describe_line(line_words)
                if d["bullet_char"]:
                    bullet_x0_by_char[d["bullet_char"]].add(d["x0"])
                if d["bold_start"] and (
                    "pay for" in d["text"].lower() or "exclusion" in d["text"].lower()
                    or "not covered" in d["text"].lower()
                ):
                    bold_boundary_lines.append((i, d["text"][:60]))
                if page_indices is not None and sample_lines_printed < 400:
                    marker = f"[{d['bullet_char']}]" if d["bullet_char"] else "   "
                    bold_flag = "BOLD" if d["bold_start"] else "    "
                    print(f"p{i:>3} x0={d['x0']:>6} {marker} {bold_flag} {d['text'][:80]}")
                    sample_lines_printed += 1

        print("\n-- bullet char -> observed x0 positions --")
        for ch, x0s in bullet_x0_by_char.items():
            print(f"  {ch!r}: {sorted(x0s)}")

        print("-- bold boundary-marker candidate lines --")
        for pg, txt in bold_boundary_lines[:20]:
            print(f"  p{pg}: {txt}")
        if not bullet_x0_by_char:
            print("  NO BULLET CHARACTERS FOUND in scanned pages")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("pdf_path")
    ap.add_argument("--pages", type=str, default=None, help="comma-separated page indices to dump verbosely")
    ap.add_argument("--max-pages", type=int, default=None, help="scan first N pages for aggregate stats")
    args = ap.parse_args()

    page_indices = None
    if args.pages:
        page_indices = [int(x) for x in args.pages.split(",")]

    analyze_pdf(args.pdf_path, page_indices=page_indices, max_pages=args.max_pages)


if __name__ == "__main__":
    main()
