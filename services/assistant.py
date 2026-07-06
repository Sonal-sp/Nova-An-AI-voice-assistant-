from config import SYSTEM_PROMPT
from services.gemini_service import ask_gemini

MAX_CONTEXT_MESSAGES = 20
recent_messages=messages[-MAX_CONTEXT_MESSAGES:]  # Limit to the last 20 messages for context
def get_assistant_response(messages):
    """
    Receives the full chat history
    and returns Nova's response.
    """

    conversation = [
        SYSTEM_PROMPT,
    ]

    for message in recent_messages:  # Limit to the last 20 messages for context
        conversation.append(
            (f"{message['role'].capitalize()}: {message['content']}")
        )

    return ask_gemini(conversation)