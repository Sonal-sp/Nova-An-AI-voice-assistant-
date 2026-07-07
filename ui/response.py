import asyncio
import time

import streamlit as st

from services.text_to_speech import text_to_speech
from utils.constants import (
    TEXT_ONLY,
    VOICE_ONLY,
    STREAM_DELAY,
)
from utils.loading import loading
from utils.constants import SPEAKING_MESSAGE


def stream_response(text: str):

    placeholder = st.empty()

    current = ""

    for word in text.split():

        current += word + " "

        placeholder.markdown(current)

        time.sleep(STREAM_DELAY)

    return current


def display_response(
    response: str,
    response_mode: str,
):

    with st.chat_message("assistant"):

        if response_mode != VOICE_ONLY:

            stream_response(response)

        if response_mode != TEXT_ONLY:

            try:

                with loading(SPEAKING_MESSAGE):

                    asyncio.run(
                        text_to_speech(response)
                    )

            except Exception as e:

                st.warning(
                    f"🔊 {e}"
                )