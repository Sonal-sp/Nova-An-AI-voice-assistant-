import streamlit as st

from services.memory import clear_messages
from services.document_service import (
    create_document,
    get_document_statistics,
)
from services.embedding_service import create_embeddings
from services.bm25_service import build_bm25_index
from services.browser_service import open_url
from utils.helpers import chat_to_text
from utils.loading import loading
from utils.constants import (
    PDF_LOADING_MESSAGE,
    TEXT_ONLY,
    TEXT_AND_VOICE,
    VOICE_ONLY,
)


def show_sidebar() -> str:
    with st.sidebar:
        # ============================================
        # Header
        # ============================================
        st.title("🤖 Nova")
        st.caption("Your Personal AI Assistant")

        st.divider()

        # ============================================
        # Response Mode
        # ============================================
        response_mode = st.radio(
            "🔊 Response Mode",
            [
                TEXT_ONLY,
                VOICE_ONLY,
                TEXT_AND_VOICE,
            ],
        )

        st.divider()

        # ============================================
        # Quick Web Launcher
        # ============================================
        st.subheader("🌐 Quick Browser Launch")
        b_col1, b_col2 = st.columns(2)
        with b_col1:
            if st.button("💻 GitHub", use_container_width=True):
                open_url("https://github.com")
            if st.button("🤖 ChatGPT", use_container_width=True):
                open_url("https://chatgpt.com")
        with b_col2:
            if st.button("✉️ Gmail", use_container_width=True):
                open_url("https://mail.google.com")
            if st.button("▶️ YouTube", use_container_width=True):
                open_url("https://www.youtube.com")

        st.divider()

        # ============================================
        # Initialize Documents Session State
        # ============================================
        if "documents" not in st.session_state:
            st.session_state.documents = []

        # ============================================
        # Upload PDFs
        # ============================================
        uploaded_files = st.file_uploader(
            "📄 Upload PDFs (Multi-Doc RAG)",
            type=["pdf"],
            accept_multiple_files=True,
        )

        if uploaded_files:
            existing = {
                doc["filename"]
                for doc in st.session_state.documents
            }

            for file in uploaded_files:
                if file.name in existing:
                    continue

                with loading(f"{PDF_LOADING_MESSAGE} ({file.name})"):
                    # 1. Read & Chunk Document
                    document = create_document(file)

                    # 2. Build FAISS Cosine Index
                    faiss_index, chunks = create_embeddings(
                        document["chunks"]
                    )

                    # 3. Build BM25 Keyword Index
                    bm25_index = build_bm25_index(
                        chunks
                    )

                    # Store document & indexes
                    document["faiss_index"] = faiss_index
                    document["bm25_index"] = bm25_index
                    document["chunks"] = chunks

                    st.session_state.documents.append(document)

        # ============================================
        # Uploaded Documents Status
        # ============================================
        st.subheader("📂 Uploaded Documents")
        documents = st.session_state.documents

        if documents:
            for i, doc in enumerate(documents):
                with st.expander(f"📄 {doc['filename']}", expanded=False):
                    st.write(f"Pages: {doc['pages']}")
                    st.write(f"Chunks: {doc['chunk_count']}")

                    if doc.get("faiss_index") is not None:
                        st.success("🧠 FAISS Cosine Index")

                    if doc.get("bm25_index") is not None:
                        st.success("🔍 BM25 Keyword Index")

                    st.info("⚡ RRF & Re-ranker Ready")

                    if st.button(
                        "🗑 Remove",
                        key=f"remove_{i}",
                        use_container_width=True,
                    ):
                        st.session_state.documents.pop(i)
                        st.rerun()
        else:
            st.info("No PDF uploaded.")

        st.divider()

        # ============================================
        # Statistics
        # ============================================
        stats = get_document_statistics(documents)
        st.subheader("📊 Document Intelligence")
        st.write(f"Files: {stats['files']}")
        st.write(f"Pages: {stats['pages']}")
        st.write(f"Chunks: {stats['chunks']}")

        st.divider()

        # ============================================
        # Session
        # ============================================
        st.subheader("💬 Session")
        st.write(f"Messages: {len(st.session_state.get('messages', []))}")
        st.write(f"Voice Mode: {response_mode}")

        st.divider()

        # ============================================
        # Export Chat
        # ============================================
        chat_text = chat_to_text(st.session_state.get("messages", []))
        st.download_button(
            "📥 Export Chat",
            chat_text,
            file_name="nova_chat.txt",
            mime="text/plain",
            use_container_width=True,
        )

        st.divider()

        # ============================================
        # Clear Chat
        # ============================================
        if st.button("🗑 Clear Chat", use_container_width=True):
            clear_messages()
            st.rerun()

    return response_mode