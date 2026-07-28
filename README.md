# Certs/Riders Benefit Extraction

Extracts the full set of benefits/covered-services mentioned in BCBSM
certificates and riders — built bottom-up directly from the documents
themselves, not anchored to any predefined list. The Topic Tree is used
only at the end, as a comparison target, to answer: *what's in the
certs/riders that isn't on the Topic Tree, and vice versa?*

This is a sibling project to `certs_riders` (which does the inverse:
starts from the Topic Tree's ~1,986 benefit names and checks which ones
are mentioned in the documents). Both read the same certs/riders PDFs;
they just start from opposite ends.

## Pipeline overview

```
Stage 1  extract_text.py         PDF -> per-page text + word-level font/position data
Stage 2  segment.py              -> header-bounded sections per document
Stage 3  extract_candidates.py   -> benefit/procedure candidates per document
Stage 4  merge_candidates.py     -> canonical benefit list, deduped across all documents
Stage 5  compare_to_topic_tree.py -> diffed against the Topic Tree, both directions
```

Each stage's output is cached to `output/` and consumed by the next stage.
Re-running a stage only reprocesses what changed (Stage 1 is content-hash
cached per file).

### Stage 1 — Text extraction (`pipeline/extract_text.py`)

Walks the PDF folders, extracts per-page text via `pdfplumber`, and caches
one JSON per document to `output/extracted/`. Each page includes raw text
*and* word-level data (`fontname`, `size`, `x0`, `top` per word) — this is
what later stages use to detect bullet hierarchy, bold-font header
markers, and section boundaries. This is the one thing that makes this
pipeline's cache larger than `certs_riders`' (which only needs plain text).

### Stage 2 — Segmentation (`pipeline/segment.py`, `family_profiles.py`)

Classifies each document into one of 5 structural profiles discovered by
inspection (not assumed):

| Profile | Docs | Structure |
|---|---|---|
| `ppo_medical` | 14 certs | Benefit-per-header, bold-italic 14pt font marks headers, bounded by "We pay for:"/"We do not pay for:" |
| `vision` | 4 certs | Same header font, different section-boilerplate convention |
| `dental` | 2 certs | Only 3 headers (Class I/II/III) — real granularity lives in nested bullets, bold-run splits name from inline description |
| `csr_rider` | 9 riders | No benefit-name headers at all — bullets live under `"$X for:"` / `"N% of the approved amount for:"` cost-tier headings |
| `skip` | 24 riders | Confirmed (by reading full text) to introduce no new benefit names — Native American cost-sharing waivers, narrow administrative amendments |

Output: one JSON per document in `output/segments/`, with header text,
page range, and the enclosing `"SECTION N: TITLE"` context read off the
certificate's own page footer.

### Stage 3 — Candidate extraction (`pipeline/extract_candidates.py`)

Walks each section's bullet hierarchy to pull out benefit candidates,
tagged with tier/confidence rather than treated as flat:

- **Tier 1** — the section header itself (only from benefit-bearing
  sections, not cost-sharing ones).
- **Tier 2a** — bullets within benefit sections, bounded by "We pay
  for:"/"We do not pay for:" (tags `inclusion: covered/excluded`).
- **Tier 2b** — bullets within cost-sharing sections (`"WHAT YOU MUST
  PAY"` in certs, the whole document for CSR riders) — catches benefit
  names that only appear in a copay/coinsurance schedule, never in the
  main benefits section.
- **Tier 3** — INDEX page terms, mapped back to a section via the
  document's own printed-page-number footer (converted to an absolute
  page index — these are not the same number).

Every candidate also gets a `shape` tag (`phrase` vs `sentence`) — a
conservative heuristic for "looks like a benefit name" vs "looks like a
description/criterion" — surfaced, not used to silently drop anything.

Output: one JSON per document in `output/candidates/`.

### Stage 4 — Cross-document merge (`pipeline/merge_candidates.py`)

Merges the same benefit mentioned across all 53 documents into one
canonical record: exact match after lemmatizing + stripping leading
articles ("a"/"an"/"the"), then a fuzzy-match rescue pass for singleton
wording variants (typos, page-number-only differences, etc.).

Output: `output/benefits_master.json` (canonical records) and
`output/benefit_summary.csv` (flat summary, sorted by mention count).

### Stage 5 — Topic Tree comparison (`pipeline/build_benefits.py`, `compare_to_topic_tree.py`)

`build_benefits.py` (reused from `certs_riders`) turns `Topic Tree
v9.xlsx` into `output/benefits.json` — 1,986 unique benefit names after
filtering out procedure codes. `compare_to_topic_tree.py` then diffs the
two lists (exact match, then fuzzy for what's left) and writes:

- `output/corpus_benefits_not_in_tree.{json,csv}` — the original question.
- `output/tree_entries_not_in_corpus.{json,csv}` — the inverse gap.
- `output/matched_pairs.{json,csv}` — the overlap, tagged exact/fuzzy + score.

## Running the pipeline

```bash
cd pipeline
python3 extract_text.py .. ../output --workers 4
python3 segment.py ../output/extracted ../output/segments
python3 extract_candidates.py ../output/extracted ../output/segments ../output/candidates
python3 merge_candidates.py ../output/candidates ../output
python3 build_benefits.py "../Topic Tree v9.xlsx" ../output --sheet "Raw Data"
python3 compare_to_topic_tree.py ../output/benefits_master.json ../output/benefits.json ../output
```

## Running the UI

```bash
cd ui
pip install -r requirements.txt
streamlit run app.py
```

Two pages:
- **Benefit-level Explorer** — the full canonical benefit list, filterable
  by tier/profile/confidence, downloadable as CSV, with per-benefit
  drill-down into which documents/pages it came from (with a text-snippet
  preview, when the extracted-text cache is available).
- **Topic Tree Comparison** — three tabs (Not in Topic Tree / Not in
  Corpus / Matched) for validating overlaps and gaps in both directions.

## Known limitations (surfaced, not hidden)

- **53-document sample**, not BCBSM's full corpus — "not found in corpus"
  means "not found in this sample."
- **Inline single-item benefits are invisible to Tier 2a.** A benefit
  stated as flowing prose with no bullet (e.g. `"We pay for standard
  frames."`) never becomes a candidate beyond its section's Tier 1 header.
- **Shape classifier misses third-person criteria** — e.g. `"Four third
  molars are removed on the same date of service"` slips through as
  `"phrase"` because the copula/modal isn't the first word.
- **A few literal near-duplicates remain unmerged** in Stage 4 — fuzzy
  rescue only runs on true singletons (exactly one mention corpus-wide) to
  keep the pass tractable, so small-but-not-singleton duplicate clusters
  can stay split.
- **Topic Tree comparison threshold (90) is deliberately conservative** —
  lowering it would start merging genuinely different-scope benefits
  (e.g. `"Ambulance Services"` vs. `"Emergency Ambulance Services"`),
  which would hide real gaps rather than surface them.
- **`output/extracted/` (~115MB) is excluded from git** — needed for the
  UI's page-snippet preview, but too heavy for the deploy repo; the UI
  degrades gracefully to "not available" rather than erroring when it's
  missing.
