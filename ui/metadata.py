import streamlit as st


def display_metadata(metadata: dict):

    badges = []

    badges.append(f"⏱️ {metadata.get('response_time', 0)} s")
    badges.append(f"🤖 {metadata.get('model', 'Unknown')}")

    if metadata.get("used_web"):
        badges.append("🌐 Web")

    if metadata.get("used_pdf"):
        badges.append("📄 PDF")

    if metadata.get("used_url"):
        badges.append("🔗 URL")

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