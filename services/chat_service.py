from services.memory import (
    add_message,
    get_messages,
)

from services.assistant import (
    get_assistant_response,
)

from services.document_service import (
    find_relevant_chunk,
)

import streamlit as st


def process_chat(user_prompt):

    add_message(
        "user",
        user_prompt,
    )

    relevant_chunk = None

    if "pdf_chunks" in st.session_state:

        relevant_chunk = find_relevant_chunk(
            user_prompt,
            st.session_state.pdf_chunks,
        )

    assistant_response = get_assistant_response(
        get_messages(),
        document_context=relevant_chunk,
    )

    add_message(
        "assistant",
        assistant_response,
    )

    return assistant_response