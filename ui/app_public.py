"""Deployed-build entry point for Streamlit Community Cloud.

Same codebase as app.py (imports its rendering functions directly, no
duplicated logic) but registers only the Benefit-level Explorer, in its
restricted "public_mode" view (see render_benefit_explorer's docstring in
app.py) - no Low-Quality/Excluded tab, and Topic Tree Comparison isn't
imported or registered at all, so it doesn't exist in this build.

Local dev keeps using `streamlit run app.py` for the full view. To deploy
this restricted view, point the Community Cloud app's "Main file path"
setting at ui/app_public.py instead of ui/app.py.

Run with: streamlit run app_public.py
"""
import streamlit as st

from app import render_benefit_explorer, render_sidebar  # also runs app.py's st.set_page_config() at import time


def main():
    render_sidebar()

    explorer_page = st.Page(
        lambda: render_benefit_explorer(public_mode=True),
        title="Benefit-level Explorer",
        url_path="benefit-explorer",
        default=True,
    )
    st.navigation([explorer_page]).run()


if __name__ == "__main__":
    main()
