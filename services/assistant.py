from config import SYSTEM_PROMPT
from services.gemini_service import ask_gemini

MAX_CONTEXT_MESSAGES = 20


def get_assistant_response(
        messages, 
        document_context=None,
        relevant_chunk=None
        ):

    conversation = [SYSTEM_PROMPT]

    if document_context:
        conversation.append(
            f"""
            Use ONLY the following document
            context when it is relevant.
            Document Context:
            {document_context}
            """
    )

    recent_messages = messages[-MAX_CONTEXT_MESSAGES:]

    for message in recent_messages:
        conversation.append(
            f"{message['role'].capitalize()}: {message['content']}"
        )

    return ask_gemini(conversation)