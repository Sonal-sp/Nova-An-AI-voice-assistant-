import streamlit as st

from services.memory import get_messages


def display_chat():

    for message in get_messages():

        with st.chat_message(message["role"]):

            st.markdown(message["content"])