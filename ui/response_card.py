import streamlit as st

from utils.code_formatter import parse_response

from ui.metadata import display_metadata

from ui.actions import (
    copy_button,
    replay_button,
    regenerate_button,
    feedback_buttons,
)


def display_response_card(
    result: dict,
    response_mode: str,
):

    response = result["text"]
    metadata = result["metadata"]

    # -----------------------------------------
    # Get citations
    # -----------------------------------------
    citations = result.get(
        "citations",
        [],
    )

    with st.chat_message("assistant"):

        # =====================================
        # Markdown + Code Blocks
        # =====================================
        blocks = parse_response(response)

        for block in blocks:

            if block["type"] == "markdown":

                st.markdown(
                    block["content"]
                )

            elif block["type"] == "code":

                st.code(
                    block["content"],
                    language=block["language"],
                )

        # =====================================
        # Sources
        # =====================================

        if citations:

            st.divider()

            st.markdown("### 📚 Sources")

            seen = set()

            for citation in citations:

                key = (
                    citation["document"],
                    citation["page"],
                )

                if key in seen:
                    continue

                seen.add(key)

                st.markdown(
                    f"""
📄 **{citation['document']}**

Page **{citation['page']}**
"""
                )

        # =====================================
        # Metadata
        # =====================================

        st.divider()

        display_metadata(metadata)

        # =====================================
        # Actions
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