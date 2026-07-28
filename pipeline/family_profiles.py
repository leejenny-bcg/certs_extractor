"""Stage 2 input: classify each Stage-1 record into one of the 5 profiles
locked in after prototyping (see certs_extraction conversation history / a
future BUILD_PLAN.md):

  1. ppo_medical  - header-per-benefit cert, "See Section 2 beginning on Page..."
  2. vision       - cert, different header convention, same bullet mechanics
  3. dental       - cert, only Class I/II/III headers; real granularity is nested
  4. csr_rider    - Med Rx cost-sharing-% riders; bullets live under "$X for:"
                    headings, no benefit-name header at all
  5. skip         - riders confirmed (by reading full text, not inferred) to
                    contain no benefit names: Native American cost-sharing
                    waivers, and narrow admin riders (waiting period, OOP max,
                    dental cost-sharing-vs-Class-I/II/III riders)

Cert classification (1-3) is signature-based and should generalize to a future
larger batch. Rider classification (4 vs 5) is a hardcoded list for THIS batch
only - it was decided by reading full text, not a generalizable rule, since a
content-based rule (e.g. bullet density) did not reliably separate them (see
Dental Riders 278N-283N, which have plenty of bullets but no new benefit
names). A future larger batch needs a real rule here, not this hardcoded list.
"""
from pathlib import Path

CERT_SIGNATURES = {
    "ppo_medical": "See Section 2 beginning on Page",
    "dental": "Class I",
    "vision": "Vision Care Services Not Covered",
}

CSR_RIDER_FILES = {
    "Med Rx Riders/129J RIDER BLUE CROSS PREMIER PPO SILVER SAVER COST-SHARING 73.pdf",
    "Med Rx Riders/130J RIDER BLUE CROSS PREMIER PPO SILVER SAVER COST-SHARING 87.pdf",
    "Med Rx Riders/131J RIDER BLUE CROSS PREMIER PPO SILVER SAVER COST-SHARING 94.pdf",
    "Med Rx Riders/607F RIDER BLUE CROSS PREMIER PPO SILVER COST-SHARING 73.pdf",
    "Med Rx Riders/608F RIDER BLUE CROSS PREMIER PPO SILVER COST-SHARING 87.pdf",
    "Med Rx Riders/609F RIDER BLUE CROSS PREMIER PPO SILVER COST-SHARING 94.pdf",
    "Med Rx Riders/824H RIDER BLUE CROSS PREMIER SILVER EXTRA COST-SHARING 73.pdf",
    "Med Rx Riders/825H RIDER BLUE CROSS PREMIER SILVER EXTRA COST-SHARING 87.pdf",
    "Med Rx Riders/826H RIDER BLUE CROSS PREMIER SILVER EXTRA COST-SHARING 94.pdf",
}


def classify(record):
    """Return one of: ppo_medical, vision, dental, csr_rider, skip."""
    rel_path = record["relative_path"]

    if record["doc_type"] == "Rider":
        return "csr_rider" if rel_path in CSR_RIDER_FILES else "skip"

    # Certificates: signature-phrase scan over first 60 pages is enough -
    # every signature we rely on appears well before page 60 in this sample.
    text = "\n".join(p["raw_text"] for p in record["pages"][:60])
    for profile, signature in CERT_SIGNATURES.items():
        if signature in text:
            return profile

    return "skip"


def classify_all(cached_records):
    by_profile = {}
    for record in cached_records:
        profile = classify(record)
        by_profile.setdefault(profile, []).append(record["relative_path"])
    return by_profile
