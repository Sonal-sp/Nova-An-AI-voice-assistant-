import logging
logger = logging.getLogger(__name__)

# Fallback memory storage for non-Streamlit (FastAPI / CLI) environments
_global_messages = []
_global_last_response = None

def _get_state():
    try:
        import streamlit as st
        if hasattr(st, "session_state"):
            try:
                # Test script run context
                _ = st.session_state.get("messages", None)
                return st.session_state
            except Exception:
                pass
    except Exception:
        pass
    return None

def initialize_memory():
    state = _get_state()
    if state is not None:
        defaults = {
            "messages": [],
            "pdf_text": "",
            "pdf_chunks": [],
            "pending_regenerate": False,
            "last_response": None,
        }
        for key, value in defaults.items():
            if key not in state:
                state[key] = value

def get_messages():
    state = _get_state()
    if state is not None:
        if "messages" not in state:
            state["messages"] = []
        return state.messages
    return _global_messages

def add_message(role, content):
    state = _get_state()
    msg = {"role": role, "content": content}
    if state is not None:
        if "messages" not in state:
            state["messages"] = []
        state.messages.append(msg)
    else:
        _global_messages.append(msg)

def clear_messages():
    global _global_messages, _global_last_response
    state = _get_state()
    if state is not None:
        state.messages = []
        state.last_response = None
    _global_messages = []
    _global_last_response = None

def get_last_user_message():
    msgs = get_messages()
    for message in reversed(msgs):
        if message.get("role") == "user":
            return message.get("content")
    return None

def get_last_assistant_message():
    msgs = get_messages()
    for message in reversed(msgs):
        if message.get("role") == "assistant":
            return message.get("content")
    return None

def remove_last_assistant_message():
    msgs = get_messages()
    for i in range(len(msgs) - 1, -1, -1):
        if msgs[i].get("role") == "assistant":
            msgs.pop(i)
            return

def set_last_response(response):
    global _global_last_response
    state = _get_state()
    if state is not None:
        state.last_response = response
    _global_last_response = response

def get_last_response():
    state = _get_state()
    if state is not None:
        return state.get("last_response", None)
    return _global_last_response