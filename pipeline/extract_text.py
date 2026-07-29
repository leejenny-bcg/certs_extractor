"""Stage 1: extract per-page text AND word-level layout data (position +
font) from every PDF under an input folder, caching results by content hash
so re-runs only reprocess new/changed files.

This is the certs_riders extract_text.py stage, carried over unchanged for
its text-extraction/caching mechanics, plus one addition: each page also
stores its words with x0/top/fontname/size. That's what lets later stages
reconstruct bullet hierarchy (glyph + indent level) and bold-run boundaries
(e.g. "We pay for:" vs. body text) without re-opening the PDF.

Usage:
    python3 extract_text.py <input_dir> <output_dir> [--workers N]
"""
import argparse
import hashlib
import json
import re
import sys
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path

import pdfplumber

from normalize import tokenize_and_lemmatize

FORM_NUMBER_RE = re.compile(r"^(\S+)\s+")

# Only these attrs are kept per word - enough to reconstruct bullet
# nesting (x0) and bold-run boundaries (fontname) without bloating the cache
# with attrs nothing downstream uses.
WORD_ATTRS = ["fontname", "size"]


def sha256_of_file(path, chunk_size=1 << 20):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            h.update(chunk)
    return h.hexdigest()


def infer_doc_type(relative_path):
    parts = Path(relative_path).parts
    top = parts[0] if parts else ""
    name_upper = relative_path.upper()
    if "RIDER" in name_upper:
        return "Rider"
    if "CERTIFICATE" in name_upper:
        return "Certificate"
    return top or "Unknown"


def infer_form_number(filename):
    m = FORM_NUMBER_RE.match(filename)
    if not m:
        return None
    token = m.group(1)
    if re.match(r"^\d{2,4}[A-Za-z]{1,2}$", token):
        return token
    return None


def extract_words_compact(page):
    words = page.extract_words(extra_attrs=WORD_ATTRS)
    return [
        {
            "text": w["text"],
            "x0": round(w["x0"], 1),
            "top": round(w["top"], 1),
            "fontname": w.get("fontname", ""),
            "size": round(w.get("size", 0), 1),
        }
        for w in words
    ]


def extract_one_pdf(input_root, relative_path):
    full_path = Path(input_root) / relative_path
    content_hash = sha256_of_file(full_path)

    pages = []
    error = None
    try:
        with pdfplumber.open(full_path) as pdf:
            for page in pdf.pages:
                raw_text = page.extract_text() or ""
                lemma_tokens = tokenize_and_lemmatize(raw_text)
                pages.append(
                    {
                        "raw_text": raw_text,
                        "lemma_text": " ".join(lemma_tokens),
                        "words": extract_words_compact(page),
                    }
                )
    except Exception as e:  # noqa: BLE001 - want to record and continue, not crash the batch
        error = f"{type(e).__name__}: {e}"

    total_chars = sum(len(p["raw_text"]) for p in pages)
    low_text_flag = (len(pages) > 0) and (total_chars / max(len(pages), 1) < 20)

    doc_id = relative_path
    filename = Path(relative_path).name

    record = {
        "doc_id": doc_id,
        "relative_path": relative_path,
        "filename": filename,
        "doc_type": infer_doc_type(relative_path),
        "form_number": infer_form_number(filename),
        "content_hash": content_hash,
        "num_pages": len(pages),
        "total_chars": total_chars,
        "low_text_flag": low_text_flag,
        "error": error,
        "pages": pages,
    }
    return record


def safe_cache_name(relative_path):
    return relative_path.replace("/", "__").replace(" ", "_")


def cache_path_for(output_dir, relative_path):
    return Path(output_dir) / "extracted" / f"{safe_cache_name(relative_path)}.json"


def needs_processing(input_root, relative_path, output_dir):
    cache_file = cache_path_for(output_dir, relative_path)
    if not cache_file.exists():
        return True
    full_path = Path(input_root) / relative_path
    try:
        with open(cache_file) as f:
            cached = json.load(f)
    except (json.JSONDecodeError, OSError):
        return True
    return cached.get("content_hash") != sha256_of_file(full_path)


def find_pdfs(input_root):
    input_root = Path(input_root)
    return sorted(
        str(p.relative_to(input_root))
        for p in input_root.rglob("*.pdf")
    )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input_dir", type=Path)
    parser.add_argument("output_dir", type=Path)
    parser.add_argument("--workers", type=int, default=4)
    parser.add_argument("--force", action="store_true", help="Reprocess all files, ignore cache")
    args = parser.parse_args()

    args.output_dir.mkdir(parents=True, exist_ok=True)
    (args.output_dir / "extracted").mkdir(parents=True, exist_ok=True)

    all_pdfs = find_pdfs(args.input_dir)
    print(f"Found {len(all_pdfs)} PDFs under {args.input_dir}", file=sys.stderr)

    to_process = [
        rp for rp in all_pdfs
        if args.force or needs_processing(args.input_dir, rp, args.output_dir)
    ]
    skipped = len(all_pdfs) - len(to_process)
    print(f"{skipped} unchanged (cached), {len(to_process)} to process", file=sys.stderr)

    processed = 0
    errors = []
    with ProcessPoolExecutor(max_workers=args.workers) as pool:
        futures = {
            pool.submit(extract_one_pdf, args.input_dir, rp): rp
            for rp in to_process
        }
        for fut in as_completed(futures):
            rp = futures[fut]
            try:
                record = fut.result()
            except Exception as e:  # noqa: BLE001
                errors.append({"relative_path": rp, "error": str(e)})
                print(f"FAILED: {rp}: {e}", file=sys.stderr)
                continue

            cache_file = cache_path_for(args.output_dir, rp)
            with open(cache_file, "w") as f:
                json.dump(record, f)

            if record["error"]:
                errors.append({"relative_path": rp, "error": record["error"]})
            processed += 1
            print(f"[{processed}/{len(to_process)}] {rp} ({record['num_pages']} pages)", file=sys.stderr)

    print(f"Done. Processed {processed}, skipped {skipped}, errors {len(errors)}", file=sys.stderr)
    if errors:
        print(json.dumps(errors, indent=2), file=sys.stderr)


if __name__ == "__main__":
    main()
