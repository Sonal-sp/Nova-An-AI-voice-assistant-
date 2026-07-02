import streamlit as st
from services.gemini_service import ask_gemini

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="Nova",
    page_icon="🤖",
    layout="centered"
)

# -----------------------------
# Session State
# -----------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# -----------------------------
# Sidebar
# -----------------------------
with st.sidebar:
    st.title("⚙️ Settings")
    st.write("**Nova AI Assistant**")
    st.write("Version 0.3")

    st.divider()

    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.rerun()

# -----------------------------
# Main Header
# -----------------------------
st.title("🤖 Nova")
st.caption("Your Personal AI Assistant powered by Gemini")

# -----------------------------
# Welcome Screen
# -----------------------------
if not st.session_state.messages:
    st.info("""
👋 **Welcome to Nova!**

I can help you with:

- 💻 Programming
- 📚 Study Assistance
- 🌍 General Knowledge
- 💡 Brainstorming Ideas

Type your first message below!
""")

# -----------------------------
# Display Chat History
# -----------------------------
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# -----------------------------
# Chat Input
# -----------------------------
user_prompt = st.chat_input("Ask Nova anything...")

if user_prompt:

    # Save user message
    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_prompt,
        }
    )

    # Display user message immediately
    with st.chat_message("user"):
        st.markdown(user_prompt)

    # Get AI response
    with st.spinner("🤖 Nova is thinking..."):
        assistant_response = ask_gemini(user_prompt)

    # Save assistant response
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": assistant_response,
        }
    )

    # Display assistant response
    with st.chat_message("assistant"):
        st.markdown(assistant_response)