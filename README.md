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
Stage 1    extract_text.py            PDF -> per-page text + word-level font/position data
Stage 2    segment.py                 -> header-bounded sections per document
Stage 3    extract_candidates.py      -> benefit/procedure candidates per document
Stage 4    merge_candidates.py        -> canonical benefit list, deduped across all documents
Stage 4.5  classify_benefits.py       -> LLM pass flagging likely non-benefit noise (tags, doesn't delete)
Stage 5    compare_to_topic_tree.py   -> diffed against the Topic Tree, both directions (exact + fuzzy)
Stage 5.5  semantic_match_topic_tree.py -> LLM pass rechecking unmatched benefits fuzzy matching missed
```

Each stage's output is cached to `output/` and consumed by the next stage.
Re-running a stage only reprocesses what changed (Stage 1 is content-hash
cached per file; Stages 4.5/5.5 cache LLM results by a hash of the evidence
sent to the model, in `pipeline/.claude_*_cache.json`).

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

### Stage 4.5 — LLM classification (`pipeline/classify_benefits.py`)

Stage 3's lexical rules catch most non-benefit noise (generic-category
nouns, sentence fragments, agent clauses), but a residual set — things
like "Hospitalization" or "FDA approved" — has no clean lexical signal to
key off of. This stage reviews every non-Tier-1 canonical benefit with
Claude (Batches API), using real snippet evidence pulled from the source
pages, and classifies it as `benefit` / `generic_administrative` /
`fragment_or_criterion`. Only high/medium-confidence non-"benefit"
verdicts are applied (a precision gate — mislabeling a real benefit is a
worse error than missing a fragment); everything is tagged in `llm_review`
on the master record, never deleted. A high/medium "benefit" verdict can
also *rescue* a record the shape heuristic mistakenly called "sentence."

`pipeline/confidence.py` centralizes the resulting "is this benefit
trustworthy" logic (`is_high_confidence`, `is_top_level_header`,
`exclusion_reason`) so both later pipeline stages and the UI agree on what
counts as high-confidence, without the pipeline depending on the UI layer.

### Stage 5 — Topic Tree comparison (`pipeline/build_benefits.py`, `compare_to_topic_tree.py`)

`build_benefits.py` (reused from `certs_riders`) turns `Topic Tree
v9.xlsx` into `output/benefits.json` — 1,986 unique benefit names after
filtering out procedure codes. `compare_to_topic_tree.py` then diffs the
two lists on normalized-key text, in increasingly targeted passes — exact
match, fuzzy match (RapidFuzz, threshold 90), "and/or" compound
splitting, generic "Service(s)" suffix stripping — and writes:

- `output/corpus_benefits_not_in_tree.{json,csv}` — the original question.
- `output/tree_entries_not_in_corpus.{json,csv}` — the inverse gap.
- `output/matched_pairs.{json,csv}` — the overlap, tagged by match type + score.

### Stage 5.5 — LLM semantic matching (`pipeline/semantic_match_topic_tree.py`)

Fuzzy matching has a structural blind spot: it always returns the single
highest-scoring candidate, so a wrong candidate that happens to share more
surface words can outscore the right one — no threshold fixes that. This
stage takes every unmatched, high-confidence corpus benefit, generates its
top-10 fuzzy candidates (not just the top-1), and asks Claude for a strict
"is this the *same specific* benefit" verdict, backed by real source
snippets so it can see surrounding list context rather than just the bare
name. Same Batches API + precision-gate pattern as Stage 4.5. Accepted
matches are folded into `matched_pairs.json` (tagged
`match_type: "llm_semantic"`), and removed from the two "not in" files.

## Running the pipeline

```bash
cd pipeline
python3 extract_text.py .. ../output --workers 4
python3 segment.py ../output/extracted ../output/segments
python3 extract_candidates.py ../output/extracted ../output/segments ../output/candidates
python3 merge_candidates.py ../output/candidates ../output
python3 classify_benefits.py ../output/benefits_master.json ../output          # Stage 4.5, needs ANTHROPIC_API_KEY
python3 build_benefits.py "../Topic Tree v9.xlsx" ../output --sheet "Raw Data"
python3 compare_to_topic_tree.py ../output/benefits_master.json ../output/benefits.json ../output
python3 semantic_match_topic_tree.py ../output/benefits_master.json ../output/benefits.json ../output  # Stage 5.5, needs ANTHROPIC_API_KEY
```

Stages 4.5 and 5.5 call Claude via the Anthropic Batches API and cache
results by evidence hash — re-running after unrelated pipeline changes
doesn't re-bill unchanged benefits.

## Running the UI

```bash
cd ui
pip install -r requirements.txt
streamlit run app.py
```

Two pages:
- **Benefit-level Explorer** — "All Benefits" and "Low-Quality / Excluded"
  tabs (the latter for auditing what Stage 4.5 flagged, or what the shape
  heuristic excluded on its own), filterable by Topic Tree match status
  (matched/unmatched/all), downloadable as CSV, with per-benefit
  drill-down into which documents/pages it came from (with a text-snippet
  preview, when the extracted-text cache is available) and which Topic
  Tree entry it matched to.
- **Topic Tree Comparison** — three tabs (Not in Topic Tree / Not in
  Corpus / Matched) for validating overlaps and gaps in both directions;
  the Matched tab is filterable by match type and shows LLM reasoning for
  `llm_semantic` matches.

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
- **Stage 5.5's candidate pool is capped at the top 10 fuzzy matches** — if
  the correct Topic Tree entry doesn't rank in the top 10 by fuzzy score,
  Claude never sees it as an option. Closing this would need a full-tree
  semantic search rather than a fuzzy-prefiltered one; out of scope for now.
- **Tier-1 section headers are deliberately excluded from Stage 4.5's LLM
  review scope**, not because they're all real benefits, but because
  classifying them was tried and found inconsistent (two near-duplicate
  headers differing only by a dash character got opposite verdicts) and
  over-eager (flagged legitimate categories like "Surgery"). Whether to
  show them is a deterministic UI toggle instead (`is_top_level_header`),
  not an automated judgment call.
