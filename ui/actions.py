import asyncio
import streamlit as st

from st_copy_to_clipboard import st_copy_to_clipboard

from services.text_to_speech import text_to_speech

from utils.loading import loading
from utils.constants import SPEAKING_MESSAGE


# Copy Button
def copy_button(response: str):

    st_copy_to_clipboard(
        response,
        before_copy_label="📋 Copy",
        after_copy_label="✅ Copied!",
        key=f"copy_{hash(response)}",
    )


# Replay Button
def replay_button(response: str):

    if st.button(
        "🔊 Replay",
        key=f"replay_{hash(response)}",
        use_container_width=True,
    ):

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


# Regenerate Button
def regenerate_button():

    if st.button(
        "🔄 Regenerate",
        use_container_width=True,
        key="regenerate_button",
    ):

        st.session_state.pending_regenerate = True

        st.rerun()


# Feedback Buttons
def feedback_buttons():

    col1, col2 = st.columns(2)

    with col1:

        if st.button(
            "👍",
            key="feedback_like",
            use_container_width=True,
        ):

            st.toast("😊 Thanks for your feedback!")

    with col2:

        if st.button(
            "👎",
            key="feedback_dislike",
            use_container_width=True,
        ):

            st.toast("📝 Feedback recorded!")