import streamlit as st

from services.memory import initialize_memory
from services.chat_service import process_chat

from ui.sidebar import show_sidebar
from ui.welcome import show_welcome
from ui.chat import display_chat
from ui.input import get_user_input
from ui.response import display_assistant_response

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="Nova",
    page_icon="🤖",
    layout="centered",
)

# -----------------------------
# Initialize Memory
# -----------------------------
initialize_memory()

# -----------------------------
# Sidebar
# -----------------------------
response_mode = show_sidebar()

# -----------------------------
# Header
# -----------------------------
st.title("🤖 Nova")
st.caption("Your Personal AI Assistant powered by Gemini")

# -----------------------------
# Welcome Screen
# -----------------------------
show_welcome()

# -----------------------------
# Chat History
# -----------------------------
display_chat()

# -----------------------------
# User Input
# -----------------------------
user_prompt = get_user_input()

# -----------------------------
# AI Conversation
# -----------------------------
if user_prompt:

    # Show user's latest message immediately
    with st.chat_message("user"):
        st.markdown(user_prompt)

    # Generate assistant response
    with st.spinner("🤖 Nova is thinking..."):
        assistant_response= process_chat(user_prompt)

    # Display assistant response
    display_assistant_response(
        assistant_response,
        response_mode,
    )