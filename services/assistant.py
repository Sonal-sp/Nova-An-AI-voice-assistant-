from config import SYSTEM_PROMPT
from services.gemini_service import ask_gemini
from utils.constants import MAX_CONTEXT_MESSAGES


def get_assistant_response(
    messages,
    document_context=None,
    web_context=None,
):

    conversation = [SYSTEM_PROMPT]

    # -----------------------------
    # PDF Context
    # -----------------------------
    if document_context:

        conversation.append(
            f"""
Use the following document context only if it helps answer the user's question.

DOCUMENT CONTEXT:

{document_context}
"""
        )

    # -----------------------------
    # Web Context
    # -----------------------------
    if web_context:
        conversation.append(
        f"""
You have been provided with recent web search results.

Instructions:
- Use these search results to answer the user's question.
- Summarize the information naturally.
- Do not simply copy the search results.
- Mention sources only when useful.
- If the search results are insufficient, say so.

WEB SEARCH RESULTS:

{web_context}
"""
    )

    # -----------------------------
    # Conversation History
    # -----------------------------
    recent_messages = messages[-MAX_CONTEXT_MESSAGES:]

    for message in recent_messages:

        conversation.append(
            f"{message['role'].capitalize()}: {message['content']}"
        )

    # -----------------------------
    # Ask Gemini
    # -----------------------------
    return ask_gemini(conversation)