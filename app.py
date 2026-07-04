import streamlit as st
from services.gemini_service import ask_gemini, transcribe_audio
from services.speech_to_text import record_audio
from services.text_to_speech import text_to_speech
import asyncio

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
    st.write("Version 0.4")

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

Choose one of the options below:
- ⌨️ Type a message
- 🎤 Click Speak
""")

# -----------------------------
# Display Chat History
# -----------------------------
for message in st.session_state.messages:
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
    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_prompt
        }
    )

    # Display user message
    with st.chat_message("user"):
        st.markdown(user_prompt)

    # Generate response
    with st.spinner("🤖 Nova is thinking..."):
        assistant_response = ask_gemini(user_prompt)

    # Save assistant response
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": assistant_response
        }
    )

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