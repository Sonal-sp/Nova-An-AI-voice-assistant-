import streamlit as st

from services.memory import clear_messages
from services.document_service import (
    read_pdf,
    split_text_into_chunks,
)

from utils.helpers import chat_to_text
from utils.loading import loading

from utils.constants import (
    PDF_LOADING_MESSAGE,
    TEXT_ONLY,
    TEXT_AND_VOICE,
    VOICE_ONLY,
)


def show_sidebar():

    with st.sidebar:

        # =============================
        # Header
        # =============================
        st.title("🤖 Nova")
        st.caption("Your Personal AI Assistant")

        st.divider()

        # =============================
        # Response Mode
        # =============================
        response_mode = st.radio(
            "🔊 Response Mode",
            [
                TEXT_ONLY,
                VOICE_ONLY,
                TEXT_AND_VOICE,
            ],
        )

        st.divider()

        # =============================
        # PDF Upload
        # =============================
        uploaded_file = st.file_uploader(
            "📄 Upload PDF",
            type=["pdf"],
        )

        if uploaded_file:

            with loading(PDF_LOADING_MESSAGE):

                pdf_text = read_pdf(uploaded_file)

                pdf_chunks = split_text_into_chunks(pdf_text)

            st.session_state["pdf_text"] = pdf_text
            st.session_state["pdf_chunks"] = pdf_chunks

        # =============================
        # PDF Status
        # =============================
        st.subheader("📄 Document")

        pdf_chunks = st.session_state.get("pdf_chunks", [])

        if pdf_chunks:

            st.success("✅ PDF Loaded")

            st.caption(
                f"{len(pdf_chunks)} chunks available"
            )

        else:

            st.info("No PDF uploaded")

        st.divider()

        # =============================
        # Session Statistics
        # =============================
        st.subheader("📊 Session")

        st.write(
            f"Messages: {len(st.session_state.get('messages', []))}"
        )

        st.write(
            f"Voice Mode: {response_mode}"
        )

        if pdf_chunks:

            st.write(
                f"PDF Chunks: {len(pdf_chunks)}"
            )

        st.divider()

        # =============================
        # Export Chat
        # =============================
        chat_text = chat_to_text(
            st.session_state.get("messages", [])
        )

        st.download_button(
            label="📥 Export Chat",
            data=chat_text,
            file_name="nova_chat.txt",
            mime="text/plain",
            use_container_width=True,
        )

        st.divider()

        # =============================
        # Clear Chat
        # =============================
        if st.button(
            "🗑️ Clear Chat",
            use_container_width=True,
        ):

            clear_messages()

            st.rerun()

    return response_mode