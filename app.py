import streamlit as st

from services.memory import initialize_memory
from services.chat_service import (
    process_chat,
    regenerate_response,
)

from ui.response import display_response
from ui.sidebar import show_sidebar
from ui.welcome import show_welcome
from ui.chat import display_chat
from ui.input import get_user_input
from ui.productivity_ui import render_productivity_dashboard
from ui.settings_ui import render_settings_dashboard
from ui.analytics_ui import render_analytics_dashboard
from ui.integrations_ui import render_integrations_dashboard
from ui.theme import apply_theme

from utils.constants import THINKING_MESSAGE


# Page Configuration - Set to Wide Layout for AI OS Experience
st.set_page_config(
    page_title="Nova AI Operating System",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Apply Dynamic AI OS Glassmorphic Theme
apply_theme()

# Initialize Session Memory
initialize_memory()

# Render Control Center Sidebar
response_mode = show_sidebar()

# Main Workspace Header
st.markdown(
    """
    <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 8px;">
        <div>
            <h1 style="margin: 0; font-size: 26px; font-weight: 800;">🤖 Nova AI OS</h1>
            <div style="font-size: 13px; color: #94A3B8;">Next-Generation Multi-Modal Desktop & Cloud Intelligence</div>
        </div>
        <div style="display: flex; gap: 8px; align-items: center;">
            <span class="nova-badge">⚡ Gemini 2.5 Flash</span>
            <span class="nova-badge">🔒 Privacy Protected</span>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.divider()

# Settings & System Health View (if toggled in sidebar)
if st.session_state.get("show_settings_dashboard", False):
    render_settings_dashboard()
    st.divider()

# System Analytics & Insights View (if toggled in sidebar)
if st.session_state.get("show_analytics_dashboard", False):
    render_analytics_dashboard()
    st.divider()

# Cloud Integrations Control Suite (if toggled in sidebar)
if st.session_state.get("show_integrations_dashboard", False):
    render_integrations_dashboard()
    st.divider()

# Productivity Dashboard View (if toggled in sidebar)
if st.session_state.get("show_prod_dashboard", False):
    render_productivity_dashboard()
    st.divider()

# Welcome Screen (renders if history is empty)
show_welcome()

# Handle Regenerate Request
if st.session_state.get("pending_regenerate", False):
    st.session_state.pending_regenerate = False
    with st.spinner("🔄 Synthesizing updated response..."):
        result = regenerate_response()
    if result:
        display_response(
            result=result,
            response_mode=response_mode,
        )
    st.stop()

# Display Chat Conversation History
display_chat()

# Raycast-Style Floating Chat Input
user_prompt = get_user_input()

# Process User Query
if user_prompt:
    with st.chat_message("user", avatar="👤"):
        st.markdown(user_prompt)

    with st.spinner(THINKING_MESSAGE):
        result = process_chat(user_prompt)

    if result:
        display_response(
            result=result,
            response_mode=response_mode,
        )