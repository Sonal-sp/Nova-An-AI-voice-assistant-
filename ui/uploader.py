import streamlit as st
from typing import List, Optional, Any


def render_pdf_uploader(key: str = "pdf_uploader") -> Optional[List[Any]]:
    """
    Renders styled PDF file uploader component.
    """
    return st.file_uploader(
        "📄 Upload PDF Documents",
        type=["pdf"],
        accept_multiple_files=True,
        key=key,
        help="Upload single or multiple PDF documents for Hybrid FAISS + BM25 RAG analysis.",
    )


def render_image_uploader(key: str = "image_uploader") -> Optional[Any]:
    """
    Renders styled Image uploader component for Vision AI / OCR.
    """
    return st.file_uploader(
        "📷 Upload Image / Screenshot",
        type=["png", "jpg", "jpeg", "webp"],
        accept_multiple_files=False,
        key=key,
        help="Upload diagrams, screenshots, or code images for Gemini 2.5 Vision AI analysis.",
    )
