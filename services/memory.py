import streamlit as st


# Initialize Session State
def initialize_memory():

    defaults = {

        "messages": [],

        "pdf_text": "",

        "pdf_chunks": [],

        "pending_regenerate": False,

        "last_response": None,

    }

    for key, value in defaults.items():

        if key not in st.session_state:

            st.session_state[key] = value


# Messages
def get_messages():

    return st.session_state.messages


def add_message(
    role,
    content,
):

    st.session_state.messages.append(

        {

            "role": role,

            "content": content,

        }

    )


def clear_messages():

    st.session_state.messages = []

    st.session_state.last_response = None


# Last User Message
def get_last_user_message():

    for message in reversed(

        st.session_state.messages

    ):

        if message["role"] == "user":

            return message["content"]

    return None


# Last Assistant Message
def get_last_assistant_message():

    for message in reversed(

        st.session_state.messages

    ):

        if message["role"] == "assistant":

            return message["content"]

    return None


# Remove Last Assistant Response
def remove_last_assistant_message():

    for i in range(

        len(st.session_state.messages) - 1,

        -1,

        -1,

    ):

        if (

            st.session_state.messages[i]["role"]

            == "assistant"

        ):

            st.session_state.messages.pop(i)

            return


# Last Response Cache
def set_last_response(response):

    st.session_state.last_response = response


def get_last_response():

    return st.session_state.get(

        "last_response",

        None,

    )