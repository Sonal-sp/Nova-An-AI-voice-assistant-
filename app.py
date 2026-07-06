import streamlit as st
from services.assistant import get_assistant_response
from services.speech_to_text import record_audio
from services.text_to_speech import text_to_speech
import asyncio
from services.memory import (
    initialize_memory,
    get_messages,
    add_message,
    clear_messages,
)


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
initialize_memory()

# -----------------------------
# Sidebar
# -----------------------------
with st.sidebar:
    st.title("⚙️ Settings")
    st.write("**Nova AI Assistant**")
    st.write("Version 0.4")

    st.divider()

    if st.button("🗑️ Clear Chat"):
        clear_messages()
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

Choose one of the options below:
- ⌨️ Type a message
- 🎤 Click Speak
""")

# -----------------------------
# Display Chat History
# -----------------------------
for message in get_messages():
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# -----------------------------
# Input Section
# -----------------------------
voice_button = st.button("🎤 Speak")

user_prompt = None

# Text Input
text_input = st.chat_input("Ask Nova anything...")

if text_input:
    user_prompt = text_input

# Voice Input
elif voice_button:

    with st.spinner("🎤 Recording..."):
        audio_path = record_audio()

    if audio_path:

        with st.spinner("📝 Transcribing..."):
            user_prompt = transcribe_audio(audio_path)

        if user_prompt:
            st.success(f"🎤 You said: {user_prompt}")
        else:
            st.error("❌ I couldn't understand the audio.")
    else:
        st.error("❌ Recording failed.")

# -----------------------------
# Generate AI Response
# -----------------------------
if user_prompt:

    # Save user message
    add_message("user", user_prompt)

    # Display user message
    with st.chat_message("user"):
        st.markdown(user_prompt)

    # Generate response
    with st.spinner("🤖 Nova is thinking..."):
        assistant_response = get_assistant_response(
            get_messages()
        )

    # Save assistant response
    add_message("assistant", assistant_response)

    # Display assistant response
    with st.chat_message("assistant"):
        st.markdown(assistant_response)
        audio_file = asyncio.run(
            text_to_speech(assistant_response)
            )
        try:
            asyncio.run(
                text_to_speech(assistant_response)
                )
        except Exception as e:
            st.warning(f"🔊 Couldn't play audio: {e}")