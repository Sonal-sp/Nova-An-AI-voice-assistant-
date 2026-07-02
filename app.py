import streamlit as st
from services.gemini_service import ask_gemini

st.set_page_config(
    page_title="Nova",
    page_icon="🤖",
)


if "messages" not in st.session_state:
    st.session_state.messages = []


st.title("🤖 Nova")
st.write("Welcome to Nova! Ask me anything.")


for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.write(message["content"])


question = st.chat_input("Ask Nova anything...")

if question:

    
    st.session_state.messages.append(
        {
            "role": "user",
            "content": question
        }
    )

    
    with st.chat_message("user"):
        st.write(question)

   
    answer = ask_gemini(question)

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer
        }
    )

    
    with st.chat_message("assistant"):
        st.write(answer)