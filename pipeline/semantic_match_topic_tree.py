"""Stage 5.5: LLM semantic verification of Topic Tree matches Stage 5's
fuzzy matching missed.

Stage 5's Pass B (fuzzy match on normalized keys) uses RapidFuzz's
extractOne, which always returns the single highest-scoring candidate
against a fixed threshold. That combination has a specific failure mode
confirmed against real corpus data: a *wrong* candidate can outscore the
*right* one, so raising or lowering the threshold can't fix it. Example:
"Speech language therapy" scores 78 against the tree's "Speech and
hearing therapy" but only 76 against the correct "Speech therapy" -
lowering the threshold to catch the second case also admits the first as
the winner, since extractOne only ever returns one answer per query. This
stage fixes that by giving Claude the top-10 candidates (not just the
top-1) per unmatched benefit and asking it to make the semantic judgment
the score alone can't.

Bar: SAME SPECIFIC benefit/service, not "related", "same family", or
"broader category that would cover it". This was explicitly chosen over a
looser "same broad family" standard - relaxing the bar was tried in
analysis (sampling the 60-74 fuzzy-score band under a looser standard)
and still found roughly a 50/50 good/bad split, so a loose bar doesn't
reliably separate real matches from false ones either. A wrong match
misdirects a user to the wrong coverage information, which is worse than
correctly reporting "no Topic Tree match yet" - so like classify_benefits.py,
this runs under a precision gate: only confidence="high" or "medium"
matches are applied; "low" (or no match) leaves the benefit unmatched,
recorded but not applied.

Scope: unmatched, high-confidence (is_high_confidence()) corpus benefits
that have at least one Topic Tree candidate scoring >=40 on normalized-key
token_sort_ratio (the same scorer Stage 5 uses). Below that floor there's
nothing plausible enough to bother reviewing - Claude would just be asked
to confirm "none of these", which the fuzzy pass already effectively
knows. Low-confidence (excluded) corpus benefits are skipped entirely -
reviewing likely-noise entries against the Topic Tree isn't a useful use
of this pass.

Candidates are drawn from the FULL Topic Tree, not just the entries Stage
5 left unmatched - multiple corpus benefits legitimately mapping to the
same tree entry is expected (Stage 5's Pass B docstring establishes this
same precedent), so an already-matched tree entry must still be offered
as a candidate here.

Each corpus benefit's evidence includes real source-text excerpts
(gather_snippets(), shared with classify_benefits.py), not just its name
and section headers - added after finding a concrete miss without it:
the first run rejected "Allogeneic Transplants" -> "Allogeneic bone
marrow transplantation" as "too broad a category" (reasoning from the
name alone, where "allogeneic transplant" is a broad general-medicine
term), but the source text lists it alongside "Tandem transplants" and
"single transplant" under Transplant Services - i.e. specifically a
bone-marrow/stem-cell modality in this corpus, not a general-organ
transplant claim. A 12-item random sample of the no-match verdicts from
that first run was otherwise mostly genuine correct rejections, so this
isn't a systemic rewrite, just closing the evidence gap classify_benefits.py
already established as necessary for this kind of context-dependent call.

Disclosed limitation: if the correct tree entry doesn't rank in the top
10 by fuzzy score, Claude never sees it as a candidate and can't catch it.
Closing that would need a full-tree semantic search rather than a
fuzzy-prefilter; out of scope for now.

Results are cached by a hash of the evidence bundle (canonical name +
exact candidate list), same convention as classify_benefits.py, so
re-running after unrelated pipeline changes doesn't re-bill unchanged
candidates.

Rewrites corpus_benefits_not_in_tree.json, tree_entries_not_in_corpus.json,
and matched_pairs.json in <output_dir> in place, folding in accepted
matches (tagged match_type="llm_semantic") and removing the now-matched
records from the two "not in" files.

Usage:
    python3 semantic_match_topic_tree.py <benefits_master.json> <topic_tree_benefits.json> <output_dir>
"""
import argparse
import hashlib
import json
import sys
import time
from pathlib import Path

from anthropic import Anthropic
from anthropic.types.message_create_params import MessageCreateParamsNonStreaming
from anthropic.types.messages.batch_create_params import Request
from rapidfuzz import fuzz, process

from confidence import is_high_confidence
from compare_to_topic_tree import (
    load_tree,
    write_corpus_csv,
    write_json,
    write_matched_csv,
    write_tree_csv,
)
from merge_candidates import strip_leading_article
from snippets import gather_snippets

HERE = Path(__file__).parent
CACHE_PATH = HERE / ".claude_semantic_match_cache.json"

MODEL = "claude-opus-4-8"
CANDIDATE_LIMIT = 10
CANDIDATE_FLOOR_SCORE = 40
APPLY_CONFIDENCE_LEVELS = ("high", "medium")
CONFIDENCE_SCORE = {"high": 95, "medium": 80, "low": 60}

MATCH_SCHEMA = {
    "type": "object",
    "properties": {
        "matched_tree_name": {
            "type": "string",
            "description": "The exact benefit_name string copied from the candidate list that is "
            "the SAME SPECIFIC benefit as the corpus name, or an empty string if none of the "
            "candidates are.",
        },
        "confidence": {"type": "string", "enum": ["high", "medium", "low"]},
        "reasoning": {"type": "string"},
    },
    "required": ["matched_tree_name", "confidence", "reasoning"],
    "additionalProperties": False,
}

SYSTEM_PROMPT = """You are verifying whether a benefit name extracted from health insurance \
certificates already has a matching entry on a separate Topic Tree benefit taxonomy. A \
text-similarity pass has already run and found candidate Topic Tree entries that are lexically \
similar to the benefit name - but text similarity is not the same as semantic accuracy. Confirmed \
failure mode: "Speech language therapy" scores higher on text similarity against "Speech and \
hearing therapy" than against the actually-correct "Speech therapy", because the wrong candidate \
happens to share more surface words. Your job is to make the semantic judgment the similarity \
score alone gets wrong.

You will be given the benefit name and a list of candidate Topic Tree entries (ranked by text \
similarity, NOT by correctness - a lower-ranked candidate can be the right one, or none can be). \
Decide whether any candidate refers to the SAME, SPECIFIC benefit or service. This means: the same \
service a member could point to and confirm "yes, this is what that certificate calls X". It does \
NOT mean:
- A broader category that would merely happen to cover the benefit (e.g. "Surgery" does not match \
  "Allogeneic bone marrow transplantation" just because the latter is a kind of surgery).
- A related but distinct service or modality (e.g. "Speech and hearing therapy" does not match \
  "Speech therapy" - hearing therapy is a different service bundled differently).
- Something that merely shares words or a generic tail word ("Services", "Care", "Treatment").

If one candidate is the same specific benefit, copy its exact benefit_name string into \
matched_tree_name. If none are, use an empty string.

Critical: a wrong match is a worse error than a missed one. Someone relying on this match would be \
misdirected to the wrong coverage information for that benefit - worse than being told (correctly) \
that it has no Topic Tree match yet. Only use confidence="high" when you're certain two names refer \
to the same specific thing. Use confidence="medium" when reasonably confident but not fully certain. \
Use confidence="low" - or an empty matched_tree_name - whenever there's real doubt about whether \
it's the same specific service versus a related-but-different one. When in doubt, lean toward no \
match."""

PROMPT_VERSION = 3  # v2: added snippet evidence; v3: widened snippet context_chars 80->300


def load_cache():
    if CACHE_PATH.exists():
        with open(CACHE_PATH) as f:
            return json.load(f)
    return {}


def save_cache(cache):
    with open(CACHE_PATH, "w") as f:
        json.dump(cache, f, indent=2)


def find_candidates(corpus_key, tree, tree_keys, limit=CANDIDATE_LIMIT, floor=CANDIDATE_FLOOR_SCORE):
    """Top fuzzy candidates for one corpus benefit, deduped by benefit_name
    (the Topic Tree can have distinct topic_ids sharing the same display
    name/key) so the model isn't shown the same name twice."""
    results = process.extract(corpus_key, tree_keys, scorer=fuzz.token_sort_ratio, limit=limit * 2)
    seen_names = set()
    candidates = []
    for _, score, idx in results:
        if score < floor:
            continue
        e = tree[idx]
        if e["benefit_name"] in seen_names:
            continue
        seen_names.add(e["benefit_name"])
        candidates.append(e)
        if len(candidates) >= limit:
            break
    return candidates


# Wider than gather_snippets()'s 80-char default - this stage specifically
# needs to see sibling list items around the matched phrase (e.g. "Search
# of the National Bone Marrow Donor Program Registry" two lines below
# "Allogeneic Transplants"), not just the immediate phrase classify_benefits.py
# needs for its narrower per-name classification call.
SNIPPET_CONTEXT_CHARS = 300


def build_evidence(output_dir, record, candidates):
    return {
        "canonical_name": record["canonical_name"],
        "parent_headers": record.get("parent_headers") or [],
        "candidates": [c["benefit_name"] for c in candidates],
        "snippets": gather_snippets(output_dir, record, context_chars=SNIPPET_CONTEXT_CHARS),
    }


def evidence_hash(evidence):
    payload = json.dumps({
        "prompt_version": PROMPT_VERSION,
        "canonical_name": evidence["canonical_name"],
        "candidates": evidence["candidates"],
        "snippets": evidence["snippets"],
    }, sort_keys=True)
    return hashlib.sha256(payload.encode()).hexdigest()[:16]


def build_prompt(evidence):
    lines = [
        f"Benefit name: {evidence['canonical_name']}",
    ]
    if evidence["parent_headers"]:
        lines.append(f"Section header(s) it appeared under: {'; '.join(evidence['parent_headers'])}")
    lines.append("")
    lines.append("Sample excerpts from where it matched in the source certificates:")
    if evidence["snippets"]:
        for s in evidence["snippets"]:
            lines.append(f"  - [{s['doc_id']} p{s['page']}]: {s['text']}")
    else:
        lines.append("  (no direct snippet found -- judge from the name and header alone)")
    lines.append("")
    lines.append("Candidate Topic Tree entries (ranked by text similarity, NOT correctness):")
    for i, name in enumerate(evidence["candidates"], 1):
        lines.append(f"  {i}. {name}")
    return "\n".join(lines)


def submit_batch(client, items):
    requests = [
        Request(
            custom_id=custom_id,
            params=MessageCreateParamsNonStreaming(
                model=MODEL,
                max_tokens=512,
                system=SYSTEM_PROMPT,
                messages=[{"role": "user", "content": build_prompt(evidence)}],
                output_config={"format": {"type": "json_schema", "schema": MATCH_SCHEMA}},
            ),
        )
        for custom_id, evidence in items
    ]
    return client.messages.batches.create(requests=requests)


def poll_batch(client, batch_id, poll_interval=20):
    while True:
        batch = client.messages.batches.retrieve(batch_id)
        if batch.processing_status == "ended":
            return batch
        print(f"  batch status: {batch.processing_status} "
              f"({batch.request_counts.processing} processing, "
              f"{batch.request_counts.succeeded} succeeded)", file=sys.stderr)
        time.sleep(poll_interval)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("benefits_master", type=Path)
    parser.add_argument("tree_path", type=Path, help="benefits.json (Topic Tree)")
    parser.add_argument("output_dir", type=Path)
    args = parser.parse_args()

    with open(args.benefits_master) as f:
        master_records = json.load(f)
    by_name = {r["canonical_name"]: r for r in master_records}

    tree = load_tree(args.tree_path)
    tree_keys = [e["_key"] for e in tree]

    with open(args.output_dir / "corpus_benefits_not_in_tree.json") as f:
        corpus_unmatched = json.load(f)
    with open(args.output_dir / "tree_entries_not_in_corpus.json") as f:
        tree_unmatched = json.load(f)
    with open(args.output_dir / "matched_pairs.json") as f:
        matched_pairs = json.load(f)

    # Scope: high-confidence + at least one plausible candidate. Everything
    # else (low-confidence, or no candidate scoring >=40) is left alone -
    # not reviewed, stays in corpus_unmatched untouched.
    review_items = []  # (corpus_record, candidates, evidence)
    skipped_low_confidence = 0
    skipped_no_candidate = 0
    for c in corpus_unmatched:
        record = by_name.get(c["canonical_name"])
        if record is None or not is_high_confidence(record):
            skipped_low_confidence += 1
            continue
        candidates = find_candidates(c["_key"], tree, tree_keys)
        if not candidates:
            skipped_no_candidate += 1
            continue
        evidence = build_evidence(args.output_dir, c, candidates)
        review_items.append((c, candidates, evidence))

    print(f"{len(corpus_unmatched)} unmatched corpus benefits total, "
          f"{skipped_low_confidence} skipped (not high-confidence), "
          f"{skipped_no_candidate} skipped (no candidate >={CANDIDATE_FLOOR_SCORE}), "
          f"{len(review_items)} in scope for review", file=sys.stderr)

    cache = load_cache()
    cached_results = {}
    to_classify = []
    for c, candidates, evidence in review_items:
        h = evidence_hash(evidence)
        cache_key = f"{c['canonical_name']}::{h}"
        if cache_key in cache:
            cached_results[c["canonical_name"]] = cache[cache_key]
        else:
            to_classify.append((cache_key, c, candidates, evidence))

    print(f"{len(cached_results)} already cached, {len(to_classify)} need a new Claude call",
          file=sys.stderr)

    new_results = {}
    if to_classify:
        client = Anthropic()
        batch_items = [(f"cand-{i}", evidence) for i, (_, _, _, evidence) in enumerate(to_classify)]
        batch = submit_batch(client, batch_items)
        print(f"Submitted batch {batch.id} ({len(to_classify)} requests)", file=sys.stderr)
        batch = poll_batch(client, batch.id)

        by_custom_id = {r.custom_id: r for r in client.messages.batches.results(batch.id)}
        for i, (cache_key, c, _, _) in enumerate(to_classify):
            result = by_custom_id.get(f"cand-{i}")
            if result is None or result.result.type != "succeeded":
                parsed = {"matched_tree_name": "", "confidence": "low",
                          "reasoning": "Batch request failed or errored."}
            else:
                text = next(b.text for b in result.result.message.content if b.type == "text")
                parsed = json.loads(text)
            cache[cache_key] = parsed
            new_results[c["canonical_name"]] = parsed

        save_cache(cache)

    all_results = {**cached_results, **new_results}
    items_by_name = {c["canonical_name"]: (c, candidates) for c, candidates, _ in review_items}

    accepted = 0
    rejected_bad_name = 0
    newly_matched_corpus_names = set()
    newly_matched_tree_keys = set()
    for name, parsed in all_results.items():
        applied = bool(parsed["matched_tree_name"]) and parsed["confidence"] in APPLY_CONFIDENCE_LEVELS
        if not applied:
            continue
        c, candidates = items_by_name[name]
        by_candidate_name = {cand["benefit_name"]: cand for cand in candidates}
        e = by_candidate_name.get(parsed["matched_tree_name"])
        if e is None:
            # Model returned a name that wasn't actually offered - treat
            # defensively as no match rather than trusting an unverifiable string.
            rejected_bad_name += 1
            continue
        matched_pairs.append({
            "corpus_canonical_name": c["canonical_name"],
            "corpus_total_mentions": c["total_mentions"],
            "corpus_tiers_present": c["tiers_present"],
            "corpus_profiles_present": c["profiles_present"],
            "tree_benefit_name": e["benefit_name"],
            "tree_topic_ids": e["topic_ids"],
            "tree_paths": e["tree_paths"],
            "match_type": "llm_semantic",
            "score": CONFIDENCE_SCORE[parsed["confidence"]],
            "llm_confidence": parsed["confidence"],
            "llm_reasoning": parsed["reasoning"],
        })
        newly_matched_corpus_names.add(c["canonical_name"])
        newly_matched_tree_keys.add(e["_key"])
        accepted += 1

    corpus_unmatched = [c for c in corpus_unmatched if c["canonical_name"] not in newly_matched_corpus_names]
    tree_unmatched = [e for e in tree_unmatched if e["_key"] not in newly_matched_tree_keys]

    corpus_unmatched.sort(key=lambda r: -r["total_mentions"])
    tree_unmatched.sort(key=lambda e: e["benefit_name"].lower())
    matched_pairs.sort(key=lambda p: -p["corpus_total_mentions"])

    write_json(corpus_unmatched, args.output_dir / "corpus_benefits_not_in_tree.json")
    write_json(tree_unmatched, args.output_dir / "tree_entries_not_in_corpus.json")
    write_json(matched_pairs, args.output_dir / "matched_pairs.json")
    write_corpus_csv(corpus_unmatched, args.output_dir / "corpus_benefits_not_in_tree.csv")
    write_tree_csv(tree_unmatched, args.output_dir / "tree_entries_not_in_corpus.csv")
    write_matched_csv(matched_pairs, args.output_dir / "matched_pairs.csv")

    print(f"\n--- summary ---", file=sys.stderr)
    print(f"{accepted} accepted (high/medium confidence), "
          f"{rejected_bad_name} rejected (model returned an unoffered name), "
          f"{len(all_results) - accepted - rejected_bad_name} left unmatched "
          f"(low confidence or no match found)", file=sys.stderr)
    print(f"Wrote {args.output_dir}/corpus_benefits_not_in_tree.json (-{len(newly_matched_corpus_names)}), "
          f"tree_entries_not_in_corpus.json (-{len(newly_matched_tree_keys)}), "
          f"matched_pairs.json (+{accepted})", file=sys.stderr)


if __name__ == "__main__":
    main()
