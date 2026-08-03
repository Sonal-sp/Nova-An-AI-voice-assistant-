import streamlit as st


def get_user_input():
    """
    Retrieves user prompt either from text chat input or from sidebar voice assistant.
    Main area contains exclusively the chat input.
    """
    # 1. Check if a voice command prompt was triggered from sidebar Voice Assistant
    if "voice_prompt" in st.session_state and st.session_state.voice_prompt:
        prompt = st.session_state.voice_prompt
        st.session_state.voice_prompt = None
        return prompt

    # 2. Native Raycast-Style Floating Chat Input
    text_input = st.chat_input("Ask Nova anything (or say 'Hey Nova' via Sidebar Voice)...")
    if text_input and text_input.strip():
        return text_input.strip()

    return None