import streamlit as st

from services.memory import clear_messages
from services.document_service import (
    read_pdf,
    split_text_into_chunks,
)


def show_sidebar():

    with st.sidebar:

        st.title("⚙️ Nova Settings")

        st.write("Version 0.4")

        st.divider()

        response_mode = st.radio(
            "🔊 Response Mode",
            [
                "Text Only",
                "Voice Only",
                "Text + Voice",
            ],
        )

        st.divider()

        uploaded_file = st.file_uploader(
            "📄 Upload PDF",
            type=["pdf"],
        )

        if uploaded_file:

            pdf_text = read_pdf(uploaded_file)

            pdf_chunks = split_text_into_chunks(pdf_text)

            st.session_state.pdf_text = pdf_text
            st.session_state.pdf_chunks = pdf_chunks

            st.success("✅ PDF Loaded")

            st.caption(
                f"{len(pdf_chunks)} chunks ready"
            )

        st.divider()

        if st.button("🗑️ Clear Chat", use_container_width=True):

            clear_messages()

            st.rerun()

    return response_mode