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

from services.embedding_service import (
    search_similar_chunks,
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


# ==========================================================
# Main Chat Pipeline
# ==========================================================
def process_chat(
    user_prompt,
    save_user=True,
):

    if not user_prompt:
        return None

    start_time = time.perf_counter()

    # ---------------------------------------
    # Save user message
    # ---------------------------------------
    if save_user:

        add_message(
            "user",
            user_prompt,
        )

    document_context = None
    web_context = None
    url_context = None

    citations = []

    # ==========================================================
    # Semantic PDF Search
    # ==========================================================

    documents = st.session_state.get(
        "documents",
        [],
    )

    if documents:

        contexts = []

        for document in documents:

            results = search_similar_chunks(
                question=user_prompt,
                index=document["index"],
                chunks=document["chunks"],
                top_k=3,
            )

            if results:

                chunk_text = []

                for chunk in results:

                    chunk_text.append(
                        chunk["text"]
                    )

                    citations.append(
                        {
                            "document": document["filename"],
                            "page": chunk["page"],
                            "chunk_id": chunk["chunk_id"],
                        }
                    )

                contexts.append(
                    f"""
Document:
{document['filename']}

{"\n\n".join(chunk_text)}
"""
                )

        if contexts:

            document_context = "\n\n------------------------\n\n".join(
                contexts
            )

    # ==========================================================
    # URL Reader
    # ==========================================================

    url = extract_url(user_prompt)

    if url:

        try:

            webpage = extract_text_from_url(url)

            if webpage:

                url_context = webpage[:12000]

        except Exception:

            pass

    # ==========================================================
    # Web Search
    # ==========================================================

    if should_search_web(user_prompt):

        try:

            results = search_web(user_prompt)

            if results:

                web_context = format_search_results(
                    results
                )

        except Exception:

            pass

    # ==========================================================
    # Gemini
    # ==========================================================

    assistant_response = get_assistant_response(
        messages=get_messages(),
        document_context=document_context,
        web_context=web_context,
        url_context=url_context,
    )

    # ---------------------------------------
    # Save assistant response
    # ---------------------------------------

    add_message(
        "assistant",
        assistant_response,
    )

    elapsed = round(
        time.perf_counter() - start_time,
        2,
    )

    return {

        "text": assistant_response,

        "metadata": {

            "response_time": elapsed,

            "model": "Gemini",

            "used_pdf": bool(document_context),

            "used_web": bool(web_context),

            "used_url": bool(url_context),

        },

        # ⭐ NEW
        "citations": citations,

    }


# ==========================================================
# Regenerate
# ==========================================================
def regenerate_response():

    user_prompt = get_last_user_message()

    if not user_prompt:

        return None

    remove_last_assistant_message()

    return process_chat(
        user_prompt=user_prompt,
        save_user=False,
    )