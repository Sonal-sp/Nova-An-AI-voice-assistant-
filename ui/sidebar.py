import streamlit as st
from PIL import Image

from services.memory import clear_messages
from services.document_service import (
    create_document,
    get_document_statistics,
)
from services.embedding_service import create_embeddings
from services.bm25_service import build_bm25_index
from services.browser_service import open_url
from services.desktop_service import launch_app, get_system_diagnostics
from services.vision_service import extract_images_from_pdf
from services.speech_to_text import record_audio
from services.gemini_service import transcribe_audio
from services.voice_engine import process_voice_command
from ui.audio_visualizer import render_audio_visualizer
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
        # Live Voice Assistant Widget (Wake-Word Enabled)
        # ============================================
        st.subheader("🎙️ Live Voice Assistant")
        st.caption("Say **'Hey Nova'** or click below to speak!")

        if st.button("🎤 Speak Voice Command", use_container_width=True):
            st.session_state.is_listening = True
            with loading("Listening for voice input..."):
                audio_file = record_audio(duration=6)
                if audio_file:
                    try:
                        transcript = transcribe_audio(audio_file)
                        if transcript:
                            res = process_voice_command(transcript)
                            st.session_state.voice_prompt = res["command_text"]
                            if res["wake_word_detected"]:
                                st.toast("✨ Wake word 'Hey Nova' recognized!", icon="🎙️")
                            st.rerun()
                    except Exception as e:
                        st.error(f"Voice Recognition Error: {e}")

        if st.session_state.get("is_listening", False):
            render_audio_visualizer(state="listening", label="Listening for 'Hey Nova'...")

        st.divider()

        # ============================================
        # Settings, Analytics & Productivity Toggles
        # ============================================
        st.subheader("⚙️ Control Center")
        show_settings = st.toggle("Settings & System Health", value=st.session_state.get("show_settings_dashboard", False))
        st.session_state.show_settings_dashboard = show_settings

        show_analytics = st.toggle("System Analytics & Insights", value=st.session_state.get("show_analytics_dashboard", False))
        st.session_state.show_analytics_dashboard = show_analytics

        show_prod = st.toggle("Productivity Dashboard", value=st.session_state.get("show_prod_dashboard", False))
        st.session_state.show_prod_dashboard = show_prod

        st.divider()

        # ============================================
        # Desktop Assistant Quick Launcher
        # ============================================
        st.subheader("🖥️ Desktop Apps Quick Launch")
        d_col1, d_col2 = st.columns(2)
        with d_col1:
            if st.button("💻 VS Code", use_container_width=True):
                res = launch_app("vscode")
                st.toast(res["message"])
            if st.button("🎵 Spotify", use_container_width=True):
                res = launch_app("spotify")
                st.toast(res["message"])
        with d_col2:
            if st.button("🌐 Chrome", use_container_width=True):
                res = launch_app("chrome")
                st.toast(res["message"])
            if st.button("🧮 Calculator", use_container_width=True):
                res = launch_app("calc")
                st.toast(res["message"])

        if st.button("📊 Quick Diagnostics", use_container_width=True):
            diag = get_system_diagnostics()
            st.info(diag["summary_markdown"])

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
        # Vision AI & Image Understanding
        # ============================================
        st.subheader("📸 Vision AI & Image Upload")
        uploaded_image = st.file_uploader(
            "Upload Image (Screenshot / Diagram / Doc)",
            type=["png", "jpg", "jpeg", "webp", "bmp"],
            key="vision_image_uploader",
        )

        if uploaded_image:
            try:
                pil_img = Image.open(uploaded_image)
                st.session_state.active_image = pil_img
            except Exception as e:
                st.error(f"Image error: {e}")

        if st.session_state.get("active_image") is not None:
            st.image(st.session_state.active_image, caption="📷 Active Vision Image", use_container_width=True)

            vision_mode = st.selectbox(
                "🎯 Vision Analysis Mode",
                ["general", "screenshot", "diagram", "ocr"],
                format_func=lambda x: {
                    "general": "🔍 General Visual Understanding",
                    "screenshot": "💻 Screenshot Explanation",
                    "diagram": "📐 Diagram & Architecture Flow",
                    "ocr": "🔤 Optical Character Recognition (OCR)",
                }[x],
            )
            st.session_state.vision_mode = vision_mode

            if st.button("🗑️ Clear Active Image", use_container_width=True):
                st.session_state.active_image = None
                st.rerun()

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
                    document["raw_file"] = file

                    st.session_state.documents.append(document)

        # ============================================
        # Uploaded Documents Status & PDF Image Extraction
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

                    # Extract PDF embedded images button
                    if doc.get("raw_file") and st.button("🖼️ Extract PDF Images", key=f"extract_img_{i}", use_container_width=True):
                        with loading("Extracting raster images from PDF..."):
                            doc["raw_file"].seek(0)
                            pdf_imgs = extract_images_from_pdf(doc["raw_file"])
                            doc["extracted_images"] = pdf_imgs
                            st.session_state[f"show_pdf_imgs_{i}"] = True

                    if doc.get("extracted_images"):
                        st.markdown(f"**Found {len(doc['extracted_images'])} embedded images:**")
                        for idx_img, record in enumerate(doc["extracted_images"][:3]):
                            st.image(record["image"], caption=f"Page {record['page']} ({record['width']}x{record['height']})", use_container_width=True)
                            if st.button(f"👁️ Analyze Image #{idx_img+1}", key=f"analyze_pdf_img_{i}_{idx_img}"):
                                st.session_state.active_image = record["image"]
                                st.session_state.vision_mode = "general"
                                st.rerun()

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