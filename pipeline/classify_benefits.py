"""Stage 4.5: LLM classification of residual low-signal canonical benefits.

Stage 3's lexical/regex rules catch most non-benefit noise (generic-category
nouns, sentence fragments, group-header colons, agent clauses, etc.) but a
residual set has no clean lexical signal to key off of -- e.g. "Hospitalization",
"Ancillary services", "FDA approved", or a long descriptive bullet like "Drugs
obtained from an out-of-network mail order provider" that reads as a phrase
(no leading verb, no terminal punctuation) but is actually an exclusion-list
fragment, not a benefit name. This stage reviews exactly that residual
population with Claude, using real snippet evidence, and tags (never deletes)
the ones it's confident are not real benefit names.

Scope gate: only canonical records where `1 not in tiers_present` (not a
section header) AND `shape_breakdown["phrase"] >= shape_breakdown["sentence"]`
(i.e. records is_high_confidence() currently marks confident via the
*shape* path, not the *Tier 1* path). Tier 1 was briefly included (found
two real gaps this way: "Temporary Benefits" and "Value Based Programs"
are policy/program section headers, not nameable services), but reverted
after finding the classification was inconsistent on Tier-1 headers
specifically -- two near-duplicate "Class I - Diagnostic and Preventive
Services" records (differing only by dash character) got opposite
verdicts, and several broad-but-legitimate "PAYS FOR" section categories
("Surgery", "Hospital Services", dental's "Class II/III" tiers) got
flagged too, which would hide primary navigation categories this whole
pipeline treats as ground-truth Tier 1 elsewhere. Tier-1 visibility is
now a deterministic user-facing UI toggle instead (see
ui/data.py:is_top_level_header) rather than an LLM judgment call. No
mention-count/MeSH-style gate is applied on top, because generic
administrative terms (e.g. "Coinsurance") often have *high* mention counts
precisely because they're generic -- mention count doesn't separate signal
from noise here the way it does in certs_riders' Topic-Tree-anchored
problem.

Every candidate is classified as exactly one of:
  - "benefit": a real, specific covered service/benefit name.
  - "generic_administrative": a category/process noun, not itself a benefit
    (e.g. "Hospitalization", "Coinsurance", "Equipment").
  - "fragment_or_criterion": a sentence fragment, exclusion clause, or
    eligibility criterion that isn't a benefit name at all, whether short
    ("FDA approved") or long ("Drugs obtained from an out-of-network mail
    order provider").

Under a precision gate: only confidence="high" or "medium" non-"benefit"
classifications are applied (i.e. hidden by the UI's "hide low-quality
entries" checkbox, via is_high_confidence()'s llm_review.applied check).
Mislabeling a real benefit is a much worse error than leaving a genuinely
generic/fragment one unflagged, so confidence="low" results are recorded but
never applied, and everything is tagged, never deleted, per this project's
"surface, don't hide" approach used throughout.

Results are cached by a hash of the evidence bundle sent to the model, so
re-running after unrelated pipeline changes doesn't re-bill unchanged
candidates.

Usage:
    python3 classify_benefits.py <benefits_master.json> <output_dir>
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

from snippets import find_snippet

HERE = Path(__file__).parent
CACHE_PATH = HERE / ".claude_classification_cache.json"

MODEL = "claude-opus-4-8"
MAX_SNIPPETS = 3
APPLY_CONFIDENCE_LEVELS = ("high", "medium")

CLASSIFICATION_SCHEMA = {
    "type": "object",
    "properties": {
        "classification": {
            "type": "string",
            "enum": ["benefit", "generic_administrative", "fragment_or_criterion"],
        },
        "confidence": {"type": "string", "enum": ["high", "medium", "low"]},
        "reasoning": {"type": "string"},
    },
    "required": ["classification", "confidence", "reasoning"],
    "additionalProperties": False,
}

SYSTEM_PROMPT = """You are auditing a bottom-up benefit-extraction pipeline for health \
insurance certificates and riders. The pipeline pulled candidate "benefit names" from \
bulleted lists and index terms in the source documents. Most are real, specific covered \
services. But some are not benefit names at all:

- Generic administrative/category nouns that describe the *kind* of provision, cost-share, \
  or process rather than a specific covered service -- e.g. "Hospitalization", \
  "Coinsurance", "Equipment", "Drugs", "Other Services".
- Sentence fragments, exclusion clauses, or eligibility criteria that were extracted as if \
  they were a bullet's benefit name, but actually describe a condition, limitation, or \
  exclusion -- e.g. "FDA approved", "Drugs obtained from an out-of-network mail order \
  provider", "The diagnosis of a condition". These can be short or long; length alone does \
  not distinguish them from real long benefit names (e.g. "High-dose chemotherapy and/or \
  total body irradiation" IS a real benefit despite being long).

IMPORTANT: this pipeline separately tracks whether each mention was covered ("we pay for") or \
excluded ("we do not pay for") -- that is not your job, and it MUST NOT influence your \
classification. A name that only ever appears in exclusion lists is still a "benefit" if it \
names a real, specific service or item -- e.g. "Custodial care", "Marital counseling", and \
"Dietary supplements" are all real, specific, nameable services that happen to be excluded in \
these plans; they are NOT fragments or criteria. Do not classify something as \
"generic_administrative" or "fragment_or_criterion" just because the snippet shows it under a \
"we do not pay for" heading -- judge only whether the NAME ITSELF refers to a specific, \
nameable service/item, independent of whether it's covered or excluded.

For each candidate, you're given its name, the section header(s) it appeared under, a few \
sample raw phrasings as they appeared in different documents, and real excerpts from the \
source pages. Classify it as exactly one of:

- "benefit": a real, specific, nameable service or item -- something a member could point to \
  and ask "is this covered?", regardless of whether the answer in these particular excerpts \
  happens to be yes or no.
- "generic_administrative": a category/process word or phrase, not itself a specific \
  nameable service (e.g. "Hospitalization", "Coinsurance", "Equipment") -- true regardless of \
  coverage status.
- "fragment_or_criterion": text that does not name a specific service at all, but instead \
  describes a condition, qualifier, scenario, or eligibility rule -- e.g. "Not listed in this \
  certificate", "when performed by an in-network provider", "The subscriber directs BCBSM not \
  to cover the newborn's services". This is about the text having no service name in it, not \
  about coverage status.

Critical: mislabeling a real, legitimate benefit as "generic_administrative" or \
"fragment_or_criterion" is a much worse error than leaving a genuinely generic/fragment one \
classified as "benefit". Only use confidence="high" when the section header and snippets \
give you concrete, unambiguous evidence. If there's real doubt, use confidence="medium" or \
"low" rather than force a confident-sounding verdict. When uncertain, lean toward "benefit". \
Never let coverage/exclusion status alone drive the classification."""

PROMPT_VERSION = 2  # bump whenever SYSTEM_PROMPT or CLASSIFICATION_SCHEMA changes, so
                     # evidence_hash() auto-invalidates stale cache entries from the old prompt


def load_cache():
    if CACHE_PATH.exists():
        with open(CACHE_PATH) as f:
            return json.load(f)
    return {}


def save_cache(cache):
    with open(CACHE_PATH, "w") as f:
        json.dump(cache, f, indent=2)


def is_scope_candidate(record):
    if 1 in record["tiers_present"]:
        return False
    phrase_count = record["shape_breakdown"].get("phrase", 0)
    sentence_count = record["shape_breakdown"].get("sentence", 0)
    return phrase_count >= sentence_count


def gather_snippets(output_dir, record, max_snippets=MAX_SNIPPETS):
    snippets = []
    docs = sorted(record["documents"], key=lambda d: -d["mention_count"])
    for doc in docs:
        if len(snippets) >= max_snippets:
            break
        for page_idx in doc["pages"][:2]:
            if len(snippets) >= max_snippets:
                break
            excerpt = find_snippet(output_dir, doc["doc_id"], page_idx, record["canonical_name"])
            if excerpt:
                snippets.append({
                    "doc_id": doc["doc_id"],
                    "page": page_idx,
                    "text": excerpt,
                })
    return snippets


def build_evidence(output_dir, record):
    variant_texts = sorted(record["variant_texts"].items(), key=lambda kv: -kv[1])
    return {
        "canonical_name": record["canonical_name"],
        "parent_headers": record.get("parent_headers") or [],
        "profiles_present": record["profiles_present"],
        "sample_variants": [v for v, _ in variant_texts[:3]],
        "total_mentions": record["total_mentions"],
        "document_count": record["document_count"],
        "snippets": gather_snippets(output_dir, record),
    }


def evidence_hash(evidence):
    payload = json.dumps({
        "prompt_version": PROMPT_VERSION,
        "parent_headers": evidence["parent_headers"],
        "sample_variants": evidence["sample_variants"],
        "snippets": evidence["snippets"],
    }, sort_keys=True)
    return hashlib.sha256(payload.encode()).hexdigest()[:16]


def build_prompt(evidence):
    lines = [
        f"Candidate name: {evidence['canonical_name']}",
        f"Section header(s) it appeared under: "
        f"{'; '.join(evidence['parent_headers']) if evidence['parent_headers'] else '(none -- likely an INDEX term)'}",
        f"Document profile(s): {', '.join(evidence['profiles_present'])}",
        f"Total mentions across corpus: {evidence['total_mentions']} "
        f"(in {evidence['document_count']} documents)",
    ]
    if len(evidence["sample_variants"]) > 1:
        lines.append(f"Sample raw phrasings: {' | '.join(evidence['sample_variants'])}")
    lines.append("")
    lines.append("Sample excerpts from where it matched:")
    if evidence["snippets"]:
        for s in evidence["snippets"]:
            lines.append(f"  - [{s['doc_id']} p{s['page']}]: {s['text']}")
    else:
        lines.append("  (no direct snippet found -- judge from the name, header, and phrasings alone)")
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
                output_config={"format": {"type": "json_schema", "schema": CLASSIFICATION_SCHEMA}},
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
    parser.add_argument("output_dir", type=Path)
    args = parser.parse_args()

    with open(args.benefits_master) as f:
        records = json.load(f)
    by_name = {r["canonical_name"]: r for r in records}

    candidates = [r for r in records if is_scope_candidate(r)]
    print(f"{len(records)} canonical benefits total, {len(candidates)} in scope "
          f"(non-Tier-1, phrase-majority)", file=sys.stderr)

    # Clear stale llm_review left over from a broader scope gate in a
    # previous run (e.g. the Tier-1 expansion this file's docstring
    # describes reverting) - keeps the data file matching the *current*
    # scope definition rather than accumulating leftovers from past ones.
    in_scope_names = {r["canonical_name"] for r in candidates}
    stale_cleared = 0
    for r in records:
        if r["canonical_name"] not in in_scope_names and r.get("llm_review") is not None:
            del r["llm_review"]
            stale_cleared += 1
    if stale_cleared:
        print(f"Cleared stale llm_review from {stale_cleared} out-of-scope record(s)", file=sys.stderr)

    evidence_by_name = {r["canonical_name"]: build_evidence(args.output_dir, r) for r in candidates}

    cache = load_cache()
    cached_results = {}
    to_classify = []
    for name, evidence in evidence_by_name.items():
        h = evidence_hash(evidence)
        cache_key = f"{name}::{h}"
        if cache_key in cache:
            cached_results[name] = cache[cache_key]
        else:
            to_classify.append((cache_key, name, evidence))

    print(f"{len(cached_results)} already cached, {len(to_classify)} need a new Claude call",
          file=sys.stderr)

    new_results = {}
    if to_classify:
        client = Anthropic()
        batch_items = [(f"cand-{i}", evidence) for i, (_, _, evidence) in enumerate(to_classify)]
        batch = submit_batch(client, batch_items)
        print(f"Submitted batch {batch.id} ({len(to_classify)} requests)", file=sys.stderr)
        batch = poll_batch(client, batch.id)

        by_custom_id = {r.custom_id: r for r in client.messages.batches.results(batch.id)}
        for i, (cache_key, name, _) in enumerate(to_classify):
            result = by_custom_id.get(f"cand-{i}")
            if result is None or result.result.type != "succeeded":
                parsed = {"classification": "benefit", "confidence": "low",
                          "reasoning": "Batch request failed or errored."}
            else:
                text = next(b.text for b in result.result.message.content if b.type == "text")
                parsed = json.loads(text)
            cache[cache_key] = parsed
            new_results[name] = parsed

        save_cache(cache)

    all_results = {**cached_results, **new_results}

    auto_flagged = 0
    for name, parsed in all_results.items():
        applied = (parsed["classification"] != "benefit"
                   and parsed["confidence"] in APPLY_CONFIDENCE_LEVELS)
        if applied:
            auto_flagged += 1
        by_name[name]["llm_review"] = {
            "classification": parsed["classification"],
            "confidence": parsed["confidence"],
            "reasoning": parsed["reasoning"],
            "applied": applied,
        }

    with open(args.benefits_master, "w") as f:
        json.dump(records, f, indent=2)

    classifications_path = args.output_dir / "llm_classifications.json"
    with open(classifications_path, "w") as f:
        json.dump(all_results, f, indent=2)

    log_lines = [
        "# LLM Classifications (Stage 4.5)\n",
        f"{len(candidates)} candidates evaluated. confidence=\"high\" or \"medium\" "
        "generic_administrative/fragment_or_criterion results are applied as flags (hidden "
        "by the UI's \"hide low-quality entries\" checkbox) -- everything else (low "
        "confidence, or \"benefit\") is left alone, per the precision gate.\n",
    ]
    for name, parsed in sorted(all_results.items(), key=lambda kv: kv[0]):
        log_lines.append(f"## \"{name}\" -> {parsed['classification']} (confidence={parsed['confidence']})")
        log_lines.append(f"- {parsed['reasoning']}")
        applied = by_name[name]["llm_review"]["applied"]
        if parsed["classification"] != "benefit" and not applied:
            log_lines.append("- **Not auto-flagged**: below the high/medium-confidence precision gate.")
        log_lines.append("")

    log_path = args.output_dir / "llm_classifications.md"
    with open(log_path, "w") as f:
        f.write("\n".join(log_lines) + "\n")

    print(f"Wrote {args.benefits_master} (llm_review added), {classifications_path}, {log_path}. "
          f"{auto_flagged} benefit(s) auto-flagged at high/medium confidence.", file=sys.stderr)


if __name__ == "__main__":
    main()
