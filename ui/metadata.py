import streamlit as st
from typing import Dict, Any


def display_metadata(metadata: Dict[str, Any]):
    badges = []

    badges.append(f"⏱️ {metadata.get('response_time', 0)}s")
    badges.append(f"🤖 {metadata.get('model', 'Unknown')}")

    if metadata.get("used_vision"):
        badges.append("👁️ Vision AI")

    if metadata.get("used_ocr"):
        badges.append("🔤 OCR Engine")

    if metadata.get("used_browser"):
        badges.append("🌐 Browser Automation")

    if metadata.get("used_pdf"):
        badges.append("📄 PDF (Advanced RAG)")

    if metadata.get("used_web"):
        badges.append("🔍 Web Search")

    if metadata.get("used_url"):
        badges.append("🔗 URL Reader")

    confidence = metadata.get("confidence")
    if confidence and confidence.get("score", 0) > 0 and not metadata.get("used_browser") and not metadata.get("used_vision"):
        score_val = confidence["score"]
        level = confidence.get("level", "Medium")
        badges.append(f"🎯 Confidence: {score_val}% ({level})")

    st.markdown(
        f"""
<div style="
margin-top:10px;
font-size:0.82rem;
color:#888;
">
{' &nbsp;&nbsp;•&nbsp;&nbsp; '.join(badges)}
</div>
""",
        unsafe_allow_html=True,
    )