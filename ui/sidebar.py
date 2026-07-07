import streamlit as st
from utils.helpers import chat_to_text
from services.memory import clear_messages
from services.document_service import (
    read_pdf,
    split_text_into_chunks,
)
from utils.helpers import is_pdf_loaded
from utils.loading import loading
from utils.constants import (
    THINKING_MESSAGE,
    PDF_LOADING_MESSAGE,
    SPEAKING_MESSAGE,
    TRANSCRIBE_MESSAGE,
)
def show_sidebar():

    with st.sidebar:

        # -----------------------------
        # Header
        # -----------------------------
        st.title("🤖 Nova")
        st.caption("Your Personal AI Assistant")

        st.divider()

        # -----------------------------
        # Response Mode
        # -----------------------------
        response_mode = st.radio(
            "🔊 Response Mode",
            [
                "Text Only",
                "Voice Only",
                "Text + Voice",
            ],
        )

        st.divider()

        # -----------------------------
        # PDF Upload
        # -----------------------------
        uploaded_file = st.file_uploader(
            "📄 Upload PDF",
            type=["pdf"],
        )

        if uploaded_file:
            with loading(PDF_LOADING_MESSAGE):
                pdf_text = read_pdf(uploaded_file)
            pdf_chunks = split_text_into_chunks(pdf_text)

            st.session_state.pdf_text = pdf_text
            st.session_state.pdf_chunks = pdf_chunks

        # -----------------------------
        # PDF Status
        # -----------------------------
        st.subheader("📄 Document")

        if is_pdf_loaded:
            st.success("PDF Loaded")

            st.caption(
                f"{len(st.session_state.pdf_chunks)} chunks available"
            )

        else:

            st.info("No PDF uploaded")

        st.divider()

        # -----------------------------
        # Session Statistics
        # -----------------------------
        st.subheader("📊 Session")

        st.write(
            f"Messages: {len(st.session_state.messages)}"
        )

        st.write(
            f"Voice: {'Enabled' if response_mode != 'Text Only' else 'Disabled'}"
        )

        if "pdf_chunks" in st.session_state:

            st.write(
                f"PDF Chunks: {len(st.session_state.pdf_chunks)}"
            )

        st.divider()

        # -----------------------------
        # Export Chat
        # -----------------------------
        chat_text = chat_to_text(
    st.session_state.messages
)

        for msg in st.session_state.messages:

            chat_text += (
                f"{msg['role'].capitalize()}: "
                f"{msg['content']}\n\n"
            )

        st.download_button(
            label="📥 Export Chat",
            data=chat_text,
            file_name="nova_chat.txt",
            mime="text/plain",
            use_container_width=True,
        )

        st.divider()

        # -----------------------------
        # Clear Chat
        # -----------------------------
        if st.button(
            "🗑️ Clear Chat",
            use_container_width=True,
        ):

            clear_messages()
            st.rerun()

    return response_mode