import time
import streamlit as st

from services.memory import (
    add_message,
    get_messages,
    get_last_user_message,
    remove_last_assistant_message,
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


# Main Chat Pipeline
def process_chat(
    user_prompt,
    save_user=True,
):

    if not user_prompt:
        return None

    start_time = time.perf_counter()

    
    # Save User Message
    if save_user:

        add_message(
            "user",
            user_prompt,
        )

    document_context = None
    web_context = None
    url_context = None

   
    # PDF RAG
    pdf_chunks = st.session_state.get(
        "pdf_chunks",
        [],
    )

    if pdf_chunks:

        document_context = find_relevant_chunk(
            user_prompt,
            pdf_chunks,
        )

    
    # URL Reader
    url = extract_url(user_prompt)

    if url:

        try:

            webpage = extract_text_from_url(url)

            if webpage:

                url_context = webpage[:12000]

        except Exception:

            url_context = None

   
    # Web Search
    if should_search_web(user_prompt):

        try:

            results = search_web(user_prompt)

            if results:

                web_context = format_search_results(
                    results,
                )

        except Exception:

            web_context = None

    
    # Gemini Response
    assistant_response = get_assistant_response(
        messages=get_messages(),
        document_context=document_context,
        web_context=web_context,
        url_context=url_context,
    )

   
    # Save Assistant Message
    add_message(
        "assistant",
        assistant_response,
    )

    elapsed = round(
        time.perf_counter() - start_time,
        2,
    )

   
    # Return Response
    return {

        "text": assistant_response,

        "metadata": {

            "response_time": elapsed,

            "model": "Gemini",

            "used_pdf": bool(document_context),

            "used_web": bool(web_context),

            "used_url": bool(url_context),

        },

    }


# Regenerate Last Response
def regenerate_response():

    user_prompt = get_last_user_message()

    if not user_prompt:

        return None

    # Remove previous assistant reply only
    remove_last_assistant_message()

    return process_chat(
        user_prompt=user_prompt,
        save_user=False,
    )