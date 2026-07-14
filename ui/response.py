import asyncio
import streamlit as st

from services.text_to_speech import text_to_speech

from utils.code_formatter import parse_response
from utils.loading import loading

from utils.constants import (
    TEXT_ONLY,
    SPEAKING_MESSAGE,
)

from ui.metadata import display_metadata


def display_response(
    result: dict,
    response_mode: str,
):

    response = result["text"]
    metadata = result["metadata"]

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
        display_metadata(metadata)

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