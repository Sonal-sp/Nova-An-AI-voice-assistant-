import streamlit as st


def is_pdf_loaded():

    return "pdf_chunks" in st.session_state


def get_pdf_chunks():

    return st.session_state.get(
        "pdf_chunks",
        [],
    )


def get_pdf_text():

    return st.session_state.get(
        "pdf_text",
        "",
    )


def chat_to_text(messages):

    text = ""

    for msg in messages:

        text += (
            f"{msg['role'].capitalize()}: "
            f"{msg['content']}\n\n"
        )

    return text