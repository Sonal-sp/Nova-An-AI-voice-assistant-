import streamlit as st

st.title("Session State Demo")

if "count" not in st.session_state:
    st.session_state.count = 0

if st.button("Increase"):
    st.session_state.count += 1

st.write("Counter:", st.session_state.count)
