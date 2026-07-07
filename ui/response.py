import asyncio
import streamlit as st

from services.text_to_speech import text_to_speech


def display_assistant_response(
    response,
    response_mode,
):

    with st.chat_message("assistant"):

        if response_mode != "Voice Only":
            st.markdown(response)

        if response_mode != "Text Only":

            try:

                asyncio.run(
                    text_to_speech(response)
                )

            except Exception as e:

                st.warning(
                    f"🔊 Couldn't play audio: {e}"
                )