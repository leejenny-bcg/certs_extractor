"""Certs/Riders Benefit Extraction — Streamlit UI.

Run with: streamlit run app.py
"""
from pathlib import Path

import altair as alt
import pandas as pd
import streamlit as st

import data

st.set_page_config(page_title="Certs/Riders Benefit Extraction", layout="wide")

# Same palette as certs_riders/ui/app.py, for visual consistency between the
# two tools (light mode only; not hooked into Streamlit's dark-mode vars).
BLUE = "#2a78d6"
ORANGE = "#eb6834"
AQUA = "#1baf7a"


def records_to_df(records):
    rows = []
    for r in records:
        rows.append(
            {
                "canonical_name": r["canonical_name"],
                "total_mentions": r["total_mentions"],
                "document_count": r["document_count"],
                "tiers_present": ",".join(str(t) for t in r["tiers_present"]),
                "profiles_present": ", ".join(r["profiles_present"]),
                "covered": r["inclusion_breakdown"].get("covered", 0),
                "excluded": r["inclusion_breakdown"].get("excluded", 0),
                "unknown": r["inclusion_breakdown"].get("unknown", 0),
                "phrase": r["shape_breakdown"].get("phrase", 0),
                "sentence": r["shape_breakdown"].get("sentence", 0),
                "high_confidence": data.is_high_confidence(r),
                "parent_headers": " | ".join(r["parent_headers"][:5]),
            }
        )
    return pd.DataFrame(rows)


def download_button(df, label, file_name, key):
    st.download_button(
        label,
        data=df.to_csv(index=False),
        file_name=file_name,
        mime="text/csv",
        key=key,
    )


def render_benefit_explorer():
    st.title("Benefit-level Explorer")
    st.caption(
        "Benefits extracted bottom-up from the certs/riders themselves - not anchored to the "
        "Topic Tree. See Topic Tree Comparison for how this list lines up against it."
    )

    records = data.load_benefits_master()
    df = records_to_df(records)

    col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
    with col1:
        search = st.text_input("Search benefit name")
    with col2:
        tier_filter = st.multiselect("Tier", ["1", "2", "3"], default=[])
    with col3:
        profile_filter = st.multiselect(
            "Profile", sorted({p for r in records for p in r["profiles_present"]}), default=[]
        )
    with col4:
        min_mentions = st.number_input("Min mentions", min_value=1, value=1)
    hide_low_confidence = st.checkbox(
        "Hide low-confidence (Tier 3 / mostly-criteria) benefits", value=True
    )

    filtered = df
    if search:
        filtered = filtered[filtered["canonical_name"].str.contains(search, case=False, na=False)]
    if tier_filter:
        filtered = filtered[filtered["tiers_present"].apply(lambda t: any(tf in t.split(",") for tf in tier_filter))]
    if profile_filter:
        filtered = filtered[filtered["profiles_present"].apply(lambda p: any(pf in p for pf in profile_filter))]
    filtered = filtered[filtered["total_mentions"] >= min_mentions]
    if hide_low_confidence:
        filtered = filtered[filtered["high_confidence"]]

    filtered = filtered.sort_values("total_mentions", ascending=False)

    st.caption(f"{len(filtered):,} of {len(df):,} benefits shown")
    st.dataframe(
        filtered[["canonical_name", "total_mentions", "document_count", "tiers_present",
                  "profiles_present", "covered", "excluded", "high_confidence"]],
        use_container_width=True,
        hide_index=True,
        height=400,
    )
    download_button(filtered, "Download filtered benefits (CSV)", "benefits_filtered.csv", "explorer_download")

    st.divider()
    st.subheader("Benefit detail")
    options = filtered["canonical_name"].tolist()
    if not options:
        st.info("No benefits match the current filters.")
        return
    selected = st.selectbox("Pick a benefit to inspect", options, key="explorer_detail_select")
    render_benefit_detail(selected)


def render_benefit_detail(canonical_name):
    record = data.benefits_by_name().get(canonical_name)
    if record is None:
        st.warning("Benefit not found.")
        return

    st.markdown(f"### {record['canonical_name']}")

    variants = list(record["variant_texts"].keys())
    if len(variants) > 1:
        with st.expander(f"{len(variants)} wording variants merged into this benefit"):
            for v, count in record["variant_texts"].items():
                st.write(f"- \"{v}\" ({count}x)")

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Total mentions", record["total_mentions"])
    m2.metric("Documents", record["document_count"])
    m3.metric("Tiers present", ", ".join(str(t) for t in record["tiers_present"]))
    m4.metric("Profiles", ", ".join(record["profiles_present"]))

    st.write(
        f"**Inclusion:** {record['inclusion_breakdown'].get('covered', 0)} covered, "
        f"{record['inclusion_breakdown'].get('excluded', 0)} excluded, "
        f"{record['inclusion_breakdown'].get('unknown', 0)} unknown &nbsp;&nbsp; "
        f"**Shape:** {record['shape_breakdown'].get('phrase', 0)} phrase, "
        f"{record['shape_breakdown'].get('sentence', 0)} sentence"
    )

    if record["parent_headers"]:
        with st.expander(f"Parent headers ({len(record['parent_headers'])})"):
            for h in record["parent_headers"]:
                st.write(f"- {h}")

    st.write("**Documents:**")
    for d in record["documents"]:
        filename = Path(d["doc_id"]).name
        with st.expander(f"{filename} — {d['mention_count']} mention(s)"):
            st.write(f"**Pages:** {', '.join(str(p) for p in d['pages'])}")
            if d["pages"]:
                page_pick = st.selectbox(
                    "Preview a page", d["pages"], key=f"snippet_{d['doc_id']}_{canonical_name}"
                )
                snippet = data.find_snippet(d["doc_id"], page_pick, record["canonical_name"])
                if snippet:
                    st.markdown(f"> {snippet}")
                else:
                    doc = data.get_extracted_doc(d["doc_id"])
                    if doc is None:
                        st.caption("Page text not available in this deployment (extracted-text cache not included).")
                    else:
                        st.caption("No direct text match on this page (matched via a wording variant) — showing full page instead.")
                        with st.expander("Full page text"):
                            st.text(doc["pages"][page_pick]["raw_text"])


def render_topic_tree_comparison():
    st.title("Topic Tree Comparison")
    st.caption(
        "The corpus-derived benefit list (left) diffed against the Topic Tree (right) - "
        "answers which certs/riders benefits have no Topic Tree match, and vice versa."
    )

    total_corpus = len(data.load_benefits_master())
    total_tree = len(data.load_topic_tree())
    corpus_not_in_tree = data.load_corpus_not_in_tree()
    tree_not_in_corpus = data.load_tree_not_in_corpus()
    matched_pairs = data.load_matched_pairs()

    corpus_matched = total_corpus - len(corpus_not_in_tree)
    tree_matched = total_tree - len(tree_not_in_corpus)

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Corpus benefits", f"{total_corpus:,}")
    c2.metric("...matched to tree", f"{corpus_matched:,} ({corpus_matched/total_corpus:.0%})")
    c3.metric("Topic Tree entries", f"{total_tree:,}")
    c4.metric("...matched to corpus", f"{tree_matched:,} ({tree_matched/total_tree:.0%})")

    st.divider()

    tab1, tab2, tab3 = st.tabs(["Not in Topic Tree", "Not in Corpus", "Matched"])

    with tab1:
        st.caption(
            "Corpus benefits with no Topic Tree match (exact or fuzzy). Benefits containing a "
            "Tier 1 (section header) mention are the highest-confidence gaps - sorted first."
        )
        df1 = records_to_df(corpus_not_in_tree)
        df1["contains_tier1"] = df1["tiers_present"].apply(lambda t: "1" in t.split(","))

        search1 = st.text_input("Search", key="tab1_search")
        filtered1 = df1
        if search1:
            filtered1 = filtered1[filtered1["canonical_name"].str.contains(search1, case=False, na=False)]
        filtered1 = filtered1.sort_values(["contains_tier1", "total_mentions"], ascending=[False, False])

        st.caption(f"{len(filtered1):,} of {len(df1):,} shown ({df1['contains_tier1'].sum()} contain a Tier 1 header)")
        st.dataframe(
            filtered1[["canonical_name", "contains_tier1", "total_mentions", "document_count",
                       "tiers_present", "profiles_present"]],
            use_container_width=True, hide_index=True, height=400,
        )
        download_button(filtered1, "Download (CSV)", "corpus_benefits_not_in_tree.csv", "tab1_download")

        st.divider()
        options1 = filtered1["canonical_name"].tolist()
        if options1:
            selected1 = st.selectbox("Inspect a benefit's documents", options1, key="tab1_detail_select")
            render_benefit_detail(selected1)

    with tab2:
        st.caption(
            "Topic Tree entries never found anywhere in this corpus. Revenue-code-prefixed entries "
            "(e.g. \"0420 - General classification for...\") are internal billing categories that "
            "wouldn't appear in consumer-facing cert text - hidden by default, confirmed as expected "
            "noise (~29% of this list) rather than a gap."
        )
        hide_codes = st.checkbox("Hide revenue-code-prefixed entries", value=True, key="tab2_hide_codes")
        search2 = st.text_input("Search", key="tab2_search")

        rows2 = [
            {
                "benefit_name": e["benefit_name"],
                "has_code_prefix": data.has_revenue_code_prefix(e["benefit_name"]),
                "topic_ids": ", ".join(str(t) for t in e["topic_ids"]),
                "tree_paths": " | ".join(e["tree_paths"][:2]),
            }
            for e in tree_not_in_corpus
        ]
        df2 = pd.DataFrame(rows2)
        filtered2 = df2
        if hide_codes:
            filtered2 = filtered2[~filtered2["has_code_prefix"]]
        if search2:
            filtered2 = filtered2[filtered2["benefit_name"].str.contains(search2, case=False, na=False)]
        filtered2 = filtered2.sort_values("benefit_name")

        st.caption(f"{len(filtered2):,} of {len(df2):,} shown")
        st.dataframe(
            filtered2[["benefit_name", "topic_ids", "tree_paths"]],
            use_container_width=True, hide_index=True, height=450,
        )
        download_button(filtered2, "Download (CSV)", "tree_entries_not_in_corpus.csv", "tab2_download")

    with tab3:
        st.caption(
            "Overlap between the two sources, tagged exact/fuzzy with score - sorted by score "
            "ascending by default so the most borderline fuzzy matches surface first for review."
        )
        match_type_filter = st.selectbox("Match type", ["All", "exact", "fuzzy"], key="tab3_match_type")
        search3 = st.text_input("Search", key="tab3_search")

        rows3 = [
            {
                "corpus_canonical_name": p["corpus_canonical_name"],
                "tree_benefit_name": p["tree_benefit_name"],
                "match_type": p["match_type"],
                "score": p["score"],
                "corpus_total_mentions": p["corpus_total_mentions"],
            }
            for p in matched_pairs
        ]
        df3 = pd.DataFrame(rows3)
        filtered3 = df3
        if match_type_filter != "All":
            filtered3 = filtered3[filtered3["match_type"] == match_type_filter]
        if search3:
            mask = (
                filtered3["corpus_canonical_name"].str.contains(search3, case=False, na=False)
                | filtered3["tree_benefit_name"].str.contains(search3, case=False, na=False)
            )
            filtered3 = filtered3[mask]
        filtered3 = filtered3.sort_values("score")

        st.caption(f"{len(filtered3):,} of {len(df3):,} shown")
        st.dataframe(filtered3, use_container_width=True, hide_index=True, height=450)
        download_button(filtered3, "Download (CSV)", "matched_pairs.csv", "tab3_download")


def main():
    with st.sidebar:
        st.title("Certs Extraction")

    explorer_page = st.Page(render_benefit_explorer, title="Benefit-level Explorer",
                             url_path="benefit-explorer", default=True)
    comparison_page = st.Page(render_topic_tree_comparison, title="Topic Tree Comparison",
                               url_path="topic-tree-comparison")

    pg = st.navigation([explorer_page, comparison_page])
    pg.run()


if __name__ == "__main__":
    main()
