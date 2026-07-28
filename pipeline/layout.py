"""Shared layout helpers for turning pdfplumber word-level output into
visual lines, used by both the extraction stage and family-profile detection.
"""
from collections import defaultdict

BULLET_CHARS = {"•", "-", "–", "−", "◦", "○", "\xad"}


def group_words_into_lines(words, y_tol=2.5):
    """Group words with close 'top' values into visual lines, sorted left-to-right.

    words: list of dicts with at least x0/top/text (pdfplumber extract_words output).
    Returns a list of (top, [word, ...]) sorted top-to-bottom.
    """
    lines = defaultdict(list)
    line_tops = []
    for w in sorted(words, key=lambda w: w["top"]):
        placed = False
        for lt in line_tops:
            if abs(w["top"] - lt) <= y_tol:
                lines[lt].append(w)
                placed = True
                break
        if not placed:
            line_tops.append(w["top"])
            lines[w["top"]].append(w)
    return [
        (lt, sorted(lines[lt], key=lambda w: w["x0"]))
        for lt in sorted(lines.keys())
    ]


def merge_lone_bullet_lines(lines):
    """Some renders (seen in one CSR rider, using a soft-hyphen "\xad" as
    the bullet glyph) place the bullet character on its own visual line,
    vertically offset just enough that group_words_into_lines splits it from
    the text it introduces, instead of "- Bariatric surgery" on one line.
    Detect a line that is nothing but a single bullet-char word and fold it
    into the next line as its leading word."""
    merged = []
    i = 0
    while i < len(lines):
        top, words = lines[i]
        if len(words) == 1 and words[0]["text"] in BULLET_CHARS and i + 1 < len(lines):
            next_top, next_words = lines[i + 1]
            merged.append((next_top, [words[0]] + next_words))
            i += 2
            continue
        merged.append((top, words))
        i += 1
    return merged


def is_bullet_word(word):
    """A word counts as a bullet glyph if its text is exactly one of the
    known bullet characters. Originally this also required a "Symbol" font
    hint, to reject a stray lowercase 'o' word-wrap artifact seen in one
    Dental cert - but that artifact is excluded by BULLET_CHARS not
    containing plain 'o' at all, and the font-gate turned out to be too
    strict: some documents (all riders; at least one base cert's Section 2)
    render bullet dashes in the body font (e.g. BookmanOldStyle) rather than
    a dedicated Symbol font, and the font-gate was silently dropping those.
    """
    return word["text"] in BULLET_CHARS
