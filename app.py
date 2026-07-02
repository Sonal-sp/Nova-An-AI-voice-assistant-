import streamlit as st
from services.gemini_service import ask_gemini

st.set_page_config(
    page_title="Nova",
    page_icon=":robot_face:",
)

st.title("Nova: Your AI Assistant")
st.write("Welcome to Nova, your personal AI assistant. How can I help you today?")

question=st.text_input("Ask me anything")

if st.button("Ask Nova"):
    if question.strip():
        answer=ask_gemini(question)
        st.success(answer)
    else:
        st.error("Please enter a question before asking Nova.")