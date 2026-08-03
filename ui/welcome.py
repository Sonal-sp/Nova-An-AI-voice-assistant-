import streamlit as st


def show_welcome():
    """
    Renders Nova's AI Operating System Welcome Cards.
    Displays cleanly when conversation history is empty.
    """
    if not st.session_state.messages:
        st.subheader("👋 Welcome to Nova AI Operating System")
        st.caption("Ready for continuous hands-free voice interaction, multi-document FAISS RAG analysis, visual diagram breakdown, and desktop system controls.")

        w_col1, w_col2, w_col3, w_col4 = st.columns(4)
        with w_col1:
            st.info("**🎙️ Voice Mode**\n\nSay *'Hey Nova open Spotify'* or click the microphone.")
        with w_col2:
            st.success("**📄 Hybrid RAG**\n\nUpload PDFs in sidebar for FAISS + BM25 document search.")
        with w_col3:
            st.warning("**👁️ Vision AI & OCR**\n\nAnalyze diagrams, UI mockups, screenshots, and text images.")
        with w_col4:
            st.error("**🖥️ System Launcher**\n\nLaunch VS Code, Chrome, Spotify, or run diagnostics.")