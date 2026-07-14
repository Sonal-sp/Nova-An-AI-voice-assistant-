import asyncio
import streamlit as st

from services.text_to_speech import text_to_speech
from utils.code_formatter import parse_response
from utils.constants import (
    TEXT_ONLY,
    VOICE_ONLY,
)
from utils.loading import loading
from utils.constants import SPEAKING_MESSAGE


def display_response(
    response: str,
    response_mode: str,
):

    with st.chat_message("assistant"):

        blocks = parse_response(response)

        for block in blocks:

            if block["type"] == "markdown":

                st.markdown(
                    block["content"]
                )

            elif block["type"] == "code":

                st.code(
                    block["content"],
                    language=block["language"],
                )

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