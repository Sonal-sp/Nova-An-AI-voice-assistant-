import logging
import streamlit as st
from config import SYSTEM_PROMPT
from services.gemini_service import ask_gemini
from services.ollama_service import generate_local_response
from utils.constants import MAX_CONTEXT_MESSAGES

logger = logging.getLogger(__name__)


def get_assistant_response(
    messages,
    document_context=None,
    web_context=None,
    url_context=None,
):
    """
    Builds prompt and routes execution to selected model (Gemini vs Local Ollama).
    Provides automatic fallback to Gemini 2.5 Flash if local model fails.
    """

    conversation = [
        SYSTEM_PROMPT,
        """
You are Nova.

Priority for answering:
1. If PDF context answers the question, use the PDF.
2. Otherwise use webpage content if available.
3. Otherwise use web search results.
4. Otherwise use your own knowledge.

Always give the most accurate answer possible.
""",
    ]

    # ==========================================================
    # PDF Context
    # ==========================================================
    if document_context:
        conversation.append(
            f"""
You have been provided with relevant content from a PDF.

Instructions:
- Answer using the PDF whenever possible.
- If the answer is present in the PDF, prioritize it over your own knowledge.
- If the answer is not found in the PDF, then use your general knowledge.
- Do not invent information that is not present in the document.

PDF CONTENT:

{document_context}
"""
        )

    # ==========================================================
    # Web Search Context
    # ==========================================================
    if web_context:
        conversation.append(
            f"""
You have been provided with recent web search results.

Instructions:
- Use these search results to answer the user's question.
- Summarize naturally.
- Do not simply copy the search results.
- Mention sources only when useful.

WEB SEARCH RESULTS:

{web_context}
"""
        )

    # ==========================================================
    # URL Context
    # ==========================================================
    if url_context:
        conversation.append(
            f"""
The user has provided a webpage.

Instructions:
- Use the webpage content to answer the user's question.
- Ignore any unrelated information.

WEBPAGE CONTENT:

{url_context}
"""
        )

    # ==========================================================
    # Conversation History
    # ==========================================================
    recent_messages = messages[-MAX_CONTEXT_MESSAGES:]

    for message in recent_messages:
        conversation.append(
            f"{message['role'].capitalize()}: {message['content']}"
        )

    # ==========================================================
    # Model Selection & Inference Routing
    # ==========================================================
    selected_model = st.session_state.get("selected_model", "Gemini 2.5 Flash")

    if selected_model.startswith("Ollama:") or selected_model.startswith("Local:"):
        model_name = selected_model.split(":", 1)[1].strip() if ":" in selected_model else "llama3:latest"
        user_prompt = messages[-1]["content"] if messages else ""

        local_res = generate_local_response(
            prompt=user_prompt,
            model=model_name,
            system_prompt="\n".join(conversation[:-1]),
        )

        if local_res:
            return local_res

        # Fallback to Gemini if Ollama fails or times out
        logger.warning(f"Local model '{model_name}' did not return a response. Falling back to Gemini 2.5 Flash.")
        st.toast(f"⚠️ Local model '{model_name}' timed out. Switched to Gemini 2.5 Flash", icon="💡")

    # Default online Gemini synthesis
    return ask_gemini(conversation)