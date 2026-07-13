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

from services.intent_detector import (
    should_search_web,
)

from services.web_search import (
    search_web,
)

import streamlit as st


def process_chat(user_prompt):

    # Save user message
    add_message(
        "user",
        user_prompt,
    )

    # -----------------------------
    # PDF Context
    # -----------------------------
    document_context = None

    if "pdf_chunks" in st.session_state:

        document_context = find_relevant_chunk(
            user_prompt,
            st.session_state.pdf_chunks,
        )

    # -----------------------------
    # Web Context
    # -----------------------------
    web_context = None

    if should_search_web(user_prompt):

        search_results = search_web(user_prompt)

        if search_results:

            web_context = ""

            for result in search_results:

                web_context += (
                    f"Title: {result['title']}\n"
                    f"Summary: {result['body']}\n"
                    f"URL: {result['url']}\n\n"
                )

    # -----------------------------
    # Generate Response
    # -----------------------------
    assistant_response = get_assistant_response(
        messages=get_messages(),
        document_context=document_context,
        web_context=web_context,
    )

    # Save assistant response
    add_message(
        "assistant",
        assistant_response,
    )

    return assistant_response