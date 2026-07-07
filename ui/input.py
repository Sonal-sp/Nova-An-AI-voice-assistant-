import streamlit as st
from utils.loading import loading
from services.speech_to_text import record_audio
from services.gemini_service import transcribe_audio
from utils.constants import (
    THINKING_MESSAGE,
    PDF_LOADING_MESSAGE,
    SPEAKING_MESSAGE,
    TRANSCRIBE_MESSAGE,
)

def get_user_input():

    voice_button = st.button("🎤 Speak")

    text_input = st.chat_input("Ask Nova anything...")

    if text_input:
        with loading(THINKING_MESSAGE):
            return text_input

    if voice_button:

        with loading("🎤 Recording..."):

            audio_path = record_audio()

        if audio_path:

            with loading(TRANSCRIBE_MESSAGE):

                transcript = transcribe_audio(audio_path)

            if transcript:

                st.success(f"🎤 You said: {transcript}")

                return transcript

            st.error("❌ Couldn't understand audio.")

        else:

            st.error("❌ Recording failed.")

    return None