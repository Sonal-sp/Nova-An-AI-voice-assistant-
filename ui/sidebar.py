import streamlit as st
import psutil
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
from services.ollama_service import get_local_models, is_ollama_available
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
    """
    Renders Nova's AI Operating System Control Center Sidebar.
    Featuring live CPU/RAM metrics, model engine selection, voice assistant widget,
    quick launch desktop shortcuts, document indexers, and transcript exporters.
    """
    with st.sidebar:
        # ============================================
        # AI OS Header & Status Banner
        # ============================================
        cpu_usage = psutil.cpu_percent(interval=None)
        mem_usage = psutil.virtual_memory().percent

        st.markdown(
            f"""
            <div style="
                background: linear-gradient(135deg, rgba(30, 41, 59, 0.7) 0%, rgba(15, 23, 42, 0.9) 100%);
                border: 1px solid rgba(56, 189, 248, 0.25);
                border-radius: 16px;
                padding: 16px;
                margin-bottom: 16px;
                box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4);
            ">
                <div style="display: flex; align-items: center; justify-content: space-between;">
                    <div style="display: flex; align-items: center; gap: 10px;">
                        <span style="font-size: 26px;">🤖</span>
                        <div>
                            <div style="font-weight: 700; font-size: 18px; color: #F8FAFC;">Nova OS</div>
                            <div style="font-size: 11px; color: #94A3B8;">AI Desktop Control</div>
                        </div>
                    </div>
                    <span class="nova-badge">🟢 Online</span>
                </div>
                <div style="display: flex; gap: 12px; margin-top: 14px; font-size: 11px; color: #CBD5E1; font-family: monospace;">
                    <div>💻 CPU: <b>{cpu_usage}%</b></div>
                    <div>🧠 RAM: <b>{mem_usage}%</b></div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.divider()

        # ============================================
        # Response Mode & Model Switcher
        # ============================================
        response_mode = st.radio(
            "🔊 Output Mode",
            [
                TEXT_ONLY,
                VOICE_ONLY,
                TEXT_AND_VOICE,
            ],
        )

        st.subheader("🧠 Model Engine")
        local_models = ["Gemini 2.5 Flash"]
        if is_ollama_available():
            for m in get_local_models():
                local_models.append(f"Ollama: {m}")
        else:
            local_models.extend(["Ollama: llama3:latest (Offline)", "Ollama: mistral:latest (Offline)"])

        selected_model = st.selectbox(
            "Select LLM Model",
            local_models,
            index=0,
            key="model_selector_dropdown",
        )
        st.session_state.selected_model = selected_model

        st.divider()

        # ============================================
        # Sidebar Primary Voice Assistant Widget
        # ============================================
        st.subheader("🎙️ Voice Assistant Engine")
        st.caption("Trigger hands-free with **'Hey Nova'** or click microphone:")

        if st.button("🎤 Speak Voice Command", use_container_width=True, key="sidebar_voice_btn"):
            st.session_state.is_listening = True
            render_audio_visualizer(state="listening", label="Listening for audio input...")

            with loading("🎤 Recording audio input (6s)..."):
                audio_file = record_audio(duration=6)

            if audio_file:
                with loading("⚡ Transcribing & processing wake word..."):
                    try:
                        transcript = transcribe_audio(audio_file)
                        if transcript and transcript.strip():
                            res = process_voice_command(transcript)
                            cmd_text = res["command_text"]
                            st.session_state.voice_prompt = cmd_text

                            if res["wake_word_detected"]:
                                st.toast(f"✨ Wake word 'Hey Nova' triggered! Command: '{cmd_text}'", icon="🎙️")
                            else:
                                st.toast(f"🎤 Voice command captured: '{cmd_text}'", icon="🎙️")

                            st.session_state.is_listening = False
                            st.rerun()
                        else:
                            st.warning("⚠️ No clear speech detected. Please try speaking again.")
                    except Exception as e:
                        st.error(f"Voice Recognition Error: {e}")
            else:
                st.error("❌ Audio recording failed. Check microphone hardware.")

            st.session_state.is_listening = False

        if st.session_state.get("is_listening", False):
            render_audio_visualizer(state="listening", label="Listening for 'Hey Nova'...")

        st.divider()

        # ============================================
        # Control Center Toggles
        # ============================================
        st.subheader("⚙️ Control Center")
        show_settings = st.toggle("Settings & System Health", value=st.session_state.get("show_settings_dashboard", False))
        st.session_state.show_settings_dashboard = show_settings

        show_analytics = st.toggle("System Analytics & Insights", value=st.session_state.get("show_analytics_dashboard", False))
        st.session_state.show_analytics_dashboard = show_analytics

        show_integrations = st.toggle("Cloud Integrations Suite", value=st.session_state.get("show_integrations_dashboard", False))
        st.session_state.show_integrations_dashboard = show_integrations

        show_prod = st.toggle("Productivity Dashboard", value=st.session_state.get("show_prod_dashboard", False))
        st.session_state.show_prod_dashboard = show_prod

        st.divider()

        # ============================================
        # Desktop Apps Quick Launcher (Raycast Style)
        # ============================================
        st.subheader("🖥️ Desktop Raycast Launcher")
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

        if st.button("📊 System Diagnostics", use_container_width=True):
            diag = get_system_diagnostics()
            st.info(diag["summary_markdown"])

        st.divider()

        # ============================================
        # Browser Quick Launcher
        # ============================================
        st.subheader("🌐 Quick Web Shortcuts")
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
        # Vision AI Upload
        # ============================================
        st.subheader("📸 Vision AI & Image Upload")
        uploaded_image = st.file_uploader(
            "Upload Image (Screenshot / Diagram)",
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
                "🎯 Vision Mode",
                ["general", "screenshot", "diagram", "ocr"],
                format_func=lambda x: {
                    "general": "🔍 General Visual QA",
                    "screenshot": "💻 Screenshot Breakdown",
                    "diagram": "📐 Diagram & Architecture Flow",
                    "ocr": "🔤 Tesseract OCR",
                }[x],
            )
            st.session_state.vision_mode = vision_mode

            if st.button("🗑️ Clear Image", use_container_width=True):
                st.session_state.active_image = None
                st.rerun()

        st.divider()

        # ============================================
        # Multi-Doc PDF RAG Upload
        # ============================================
        if "documents" not in st.session_state:
            st.session_state.documents = []

        st.subheader("📄 Hybrid FAISS + BM25 RAG")
        uploaded_files = st.file_uploader(
            "Upload PDFs for RAG",
            type=["pdf"],
            accept_multiple_files=True,
        )

        if uploaded_files:
            existing = {doc["filename"] for doc in st.session_state.documents}
            for file in uploaded_files:
                if file.name in existing:
                    continue

                with loading(f"{PDF_LOADING_MESSAGE} ({file.name})"):
                    document = create_document(file)
                    faiss_index, chunks = create_embeddings(document["chunks"])
                    bm25_index = build_bm25_index(chunks)

                    document["faiss_index"] = faiss_index
                    document["bm25_index"] = bm25_index
                    document["chunks"] = chunks
                    document["raw_file"] = file

                    st.session_state.documents.append(document)

        # Uploaded Documents Status
        documents = st.session_state.documents
        if documents:
            for i, doc in enumerate(documents):
                with st.expander(f"📄 {doc['filename']}", expanded=False):
                    st.write(f"Pages: {doc['pages']} | Chunks: {doc['chunk_count']}")
                    if doc.get("faiss_index") is not None:
                        st.success("🧠 FAISS Cosine Index Ready")
                    if doc.get("bm25_index") is not None:
                        st.success("🔍 BM25 Keyword Index Ready")

                    if doc.get("raw_file") and st.button("🖼️ Extract PDF Images", key=f"extract_img_{i}", use_container_width=True):
                        with loading("Extracting raster images..."):
                            doc["raw_file"].seek(0)
                            pdf_imgs = extract_images_from_pdf(doc["raw_file"])
                            doc["extracted_images"] = pdf_imgs

                    if doc.get("extracted_images"):
                        st.markdown(f"**Extracted {len(doc['extracted_images'])} images:**")
                        for idx_img, record in enumerate(doc["extracted_images"][:3]):
                            st.image(record["image"], caption=f"Page {record['page']}", use_container_width=True)
                            if st.button(f"👁️ Analyze #{idx_img+1}", key=f"analyze_pdf_img_{i}_{idx_img}"):
                                st.session_state.active_image = record["image"]
                                st.session_state.vision_mode = "general"
                                st.rerun()

                    if st.button("🗑 Remove", key=f"remove_{i}", use_container_width=True):
                        st.session_state.documents.pop(i)
                        st.rerun()

        st.divider()

        # ============================================
        # Export Transcript
        # ============================================
        from utils.exporters import export_chat_to_json, export_chat_to_markdown, export_chat_to_txt

        messages_list = st.session_state.get("messages", [])
        st.subheader("📥 Export Transcript")

        exp_col1, exp_col2, exp_col3 = st.columns(3)
        with exp_col1:
            st.download_button("📄 TXT", export_chat_to_txt(messages_list), file_name="nova_transcript.txt", mime="text/plain", use_container_width=True)
        with exp_col2:
            st.download_button("📝 MD", export_chat_to_markdown(messages_list), file_name="nova_transcript.md", mime="text/markdown", use_container_width=True)
        with exp_col3:
            st.download_button("📊 JSON", export_chat_to_json(messages_list), file_name="nova_transcript.json", mime="application/json", use_container_width=True)

        st.divider()

        # ============================================
        # Clear Chat Button
        # ============================================
        if st.button("🗑 Clear Session", use_container_width=True):
            clear_messages()
            st.rerun()

    return response_mode