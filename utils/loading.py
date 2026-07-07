import streamlit as st
from contextlib import contextmanager


@contextmanager
def loading(message: str):
    with st.spinner(message):
        yield