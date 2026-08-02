import json
from typing import List, Dict, Any


def export_chat_to_json(messages: List[Dict[str, Any]]) -> str:
    """
    Exports chat history messages to structured JSON string.
    """
    cleaned = []
    for msg in messages:
        cleaned.append({
            "role": msg.get("role", "user"),
            "content": msg.get("content", ""),
            "metadata": msg.get("metadata", {}),
        })
    return json.dumps(cleaned, indent=2)


def export_chat_to_markdown(messages: List[Dict[str, Any]]) -> str:
    """
    Exports chat history to formatted Markdown document.
    """
    md_lines = ["# 🤖 Nova Chat Transcript\n"]
    for msg in messages:
        role = msg.get("role", "user").capitalize()
        content = msg.get("content", "")
        md_lines.append(f"### **{role}**")
        md_lines.append(f"{content}\n")
    return "\n".join(md_lines)


def export_chat_to_txt(messages: List[Dict[str, Any]]) -> str:
    """
    Exports chat history to clean plain text format.
    """
    txt_lines = []
    for msg in messages:
        role = msg.get("role", "user").capitalize()
        content = msg.get("content", "")
        txt_lines.append(f"{role}: {content}")
        txt_lines.append("-" * 40)
    return "\n".join(txt_lines)
