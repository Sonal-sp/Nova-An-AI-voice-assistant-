import asyncio
import streamlit as st

from services.text_to_speech import text_to_speech

from ui.response_card import display_response_card

from utils.loading import loading

from utils.constants import (
    TEXT_ONLY,
    SPEAKING_MESSAGE,
)


# Display Assistant Response
def display_response(
    result: dict,
    response_mode: str,
):

    # Render complete response card
    display_response_card(
        result=result,
        response_mode=response_mode,
    )

    # Voice Playback
    if response_mode == TEXT_ONLY:
        return

    response = result["text"]

    try:

        with loading(SPEAKING_MESSAGE):

            asyncio.run(
                text_to_speech(response)
            )

    except RuntimeError:

        loop = asyncio.new_event_loop()

        asyncio.set_event_loop(loop)

        with loading(SPEAKING_MESSAGE):

            loop.run_until_complete(
                text_to_speech(response)
            )

        loop.close()

    except Exception as e:

        st.warning(f"🔊 {e}")