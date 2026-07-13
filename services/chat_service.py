import streamlit as st

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
    format_search_results,
)

from services.url_detector import (
    extract_url,
)

from services.url_service import (
    extract_text_from_url,
)


def process_chat(user_prompt):
    """
    Main chat pipeline.

    Flow:
    User
      ↓
    Memory
      ↓
    PDF Context
      ↓
    URL Context
      ↓
    Web Search Context
      ↓
    Gemini
      ↓
    Save Response
    """

    # =============================
    # Save User Message
    # =============================
    add_message(
        "user",
        user_prompt,
    )

    # =============================
    # PDF Context
    # =============================
    document_context = None

    pdf_chunks = st.session_state.get(
        "pdf_chunks",
        [],
    )

    if pdf_chunks:

        document_context = find_relevant_chunk(
            user_prompt,
            pdf_chunks,
        )

    # =============================
    # URL Context
    # =============================
    url_context = None

    url = extract_url(user_prompt)

    if url:

        webpage = extract_text_from_url(url)

        if webpage:

            # Limit size sent to Gemini
            url_context = webpage[:12000]

    # =============================
    # Web Search Context
    # =============================
    web_context = None

    if should_search_web(user_prompt):

        search_results = search_web(
            user_prompt,
        )

        if search_results:

            web_context = format_search_results(
                search_results,
            )

    # =============================
    # Generate Assistant Response
    # =============================
    assistant_response = get_assistant_response(
        messages=get_messages(),
        document_context=document_context,
        web_context=web_context,
        url_context=url_context,
    )

    # =============================
    # Save Assistant Response
    # =============================
    add_message(
        "assistant",
        assistant_response,
    )

    return assistant_response