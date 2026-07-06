import streamlit as st


def initialize_memory():
    """Initialize chat history."""

    if "messages" not in st.session_state:
        st.session_state.messages = []


def get_messages():
    """Return all chat messages."""

    return st.session_state.messages


def add_message(role, content):
    """Add a message to memory."""

    st.session_state.messages.append(
        {
            "role": role,
            "content": content,
        }
    )


def clear_messages():
    """Clear the conversation."""

    st.session_state.messages = []