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


# Page Configuration
st.set_page_config(
    page_title="Nova",
    page_icon="🤖",
    layout="centered",
)

# Apply Dynamic UI Theme
apply_theme()

# Initialize Session
initialize_memory()

# Sidebar
response_mode = show_sidebar()

# Header
st.title("🤖 Nova")
st.caption("Your Personal AI Assistant powered by Gemini & Local Offline AI")

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

# Welcome Screen
show_welcome()

# Handle Regenerate Request
if st.session_state.get("pending_regenerate", False):

    st.session_state.pending_regenerate = False

    with st.spinner("🔄 Regenerating response..."):

        result = regenerate_response()

    if result:

        display_response(
            result=result,
            response_mode=response_mode,
        )

    st.stop()

# Display Chat History
display_chat()

# Chat Input
user_prompt = get_user_input()

# New User Message
if user_prompt:

    with st.chat_message("user"):

        st.markdown(user_prompt)

    with st.spinner(THINKING_MESSAGE):

        result = process_chat(user_prompt)

    if result:

        display_response(
            result=result,
            response_mode=response_mode,
        )