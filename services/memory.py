import streamlit as st


def initialize_memory():

    if "messages" not in st.session_state:
        st.session_state.messages = []

    if "pdf_text" not in st.session_state:
        st.session_state.pdf_text = ""

    if "pdf_chunks" not in st.session_state:
        st.session_state.pdf_chunks = []

    if "pending_regenerate" not in st.session_state:
        st.session_state.pending_regenerate = False


def get_messages():
    return st.session_state.messages


def add_message(role, content):

    st.session_state.messages.append(
        {
            "role": role,
            "content": content,
        }
    )


def clear_messages():

    st.session_state.messages = []


def get_last_user_message():

    for message in reversed(st.session_state.messages):

        if message["role"] == "user":
            return message["content"]

    return None


def remove_last_assistant_message():

    for i in range(
        len(st.session_state.messages) - 1,
        -1,
        -1,
    ):

        if st.session_state.messages[i]["role"] == "assistant":

            st.session_state.messages.pop(i)
            return