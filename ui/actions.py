import asyncio
import streamlit as st

from services.text_to_speech import text_to_speech
from utils.loading import loading
from utils.constants import SPEAKING_MESSAGE


from st_copy_to_clipboard import st_copy_to_clipboard

def copy_button(response: str):
    st_copy_to_clipboard(
        response,
        before_copy_label="📋 Copy",
        after_copy_label="✅ Copied!"
    )


def replay_button(response: str):

    if st.button(
        "🔊 Replay",
        key=f"replay_{hash(response)}",
    ):

        try:

            with loading(SPEAKING_MESSAGE):

                asyncio.run(
                    text_to_speech(response)
                )

        except Exception as e:

            st.warning(f"🔊 {e}")


def regenerate_button():

    st.button(
        "🔄 Regenerate",
        disabled=True,
        help="Coming in Sprint 11",
        key="regen_btn",
    )


def feedback_buttons():

    col1, col2 = st.columns(2)

    with col1:

        if st.button(
            "👍",
            use_container_width=True,
            key="like_btn",
        ):

            st.toast("Thanks for your feedback!")

    with col2:

        if st.button(
            "👎",
            use_container_width=True,
            key="dislike_btn",
        ):

            st.toast("Feedback recorded.")