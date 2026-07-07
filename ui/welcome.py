import streamlit as st


def show_welcome():

    if not st.session_state.messages:

        st.info(
            """
👋 **Welcome to Nova!**

I can help you with:

- 💻 Programming
- 📚 Study Assistance
- 📄 PDF Question Answering
- 💡 Brainstorming
- 🌍 General Knowledge

Choose one:

- ⌨️ Type a message
- 🎤 Click Speak
"""
        )