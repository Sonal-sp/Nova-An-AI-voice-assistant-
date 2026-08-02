import streamlit as st
from typing import Dict, Any

from utils.code_formatter import parse_response
from ui.metadata import display_metadata
from ui.actions import (
    copy_button,
    replay_button,
    regenerate_button,
    feedback_buttons,
)


def display_response_card(
    result: Dict[str, Any],
    response_mode: str,
):
    """
    Renders structured assistant response card including markdown content,
    code blocks, attributed RAG sources, performance metadata, and interactive actions.
    """
    response = result.get("text", "")
    metadata = result.get("metadata", {})
    citations = result.get("citations", [])

    with st.chat_message("assistant"):
        # =====================================
        # Markdown + Code Blocks
        # =====================================
        blocks = parse_response(response)
        for block in blocks:
            if block["type"] == "markdown":
                st.markdown(block["content"])
            elif block["type"] == "code":
                st.code(
                    block["content"],
                    language=block["language"],
                )

        # =====================================
        # Attributed RAG Sources
        # =====================================
        if citations:
            st.divider()
            st.markdown("### 📚 Attributed Sources")

            seen_sources = set()
            for cit in citations:
                key = (cit.get("document"), cit.get("page"), cit.get("chunk_id"))
                if key in seen_sources:
                    continue
                seen_sources.add(key)

                doc_name = cit.get("document", "Document")
                page_num = cit.get("page", 1)
                score_pct = cit.get("score", 0.0)
                snippet = cit.get("text", "")

                badge_color = "#10B981" if score_pct >= 70 else "#F59E0B" if score_pct >= 45 else "#6B7280"

                with st.expander(f"📄 **{doc_name}** — Page {page_num}", expanded=False):
                    st.markdown(
                        f"""
<div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
    <span><strong>Source Document:</strong> {doc_name}</span>
    <span style="background-color:{badge_color}; color:white; padding:2px 8px; border-radius:12px; font-size:0.75rem; font-weight:bold;">
        Match Score: {score_pct}%
    </span>
</div>
<blockquote style="border-left: 3px solid #3B82F6; padding-left: 10px; margin: 4px 0; color: #D1D5DB; font-style: italic;">
    {snippet}
</blockquote>
""",
                        unsafe_allow_html=True,
                    )

        # =====================================
        # Metadata
        # =====================================
        st.divider()
        display_metadata(metadata)

        # =====================================
        # Action Buttons
        # =====================================
        st.divider()
        col1, col2, col3 = st.columns(3)

        with col1:
            copy_button(response)

        with col2:
            regenerate_button()

        with col3:
            replay_button(response)

        feedback_buttons()