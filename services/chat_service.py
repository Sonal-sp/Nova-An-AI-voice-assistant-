import time
import logging
from typing import Dict, Any, Optional
import streamlit as st

from services.memory import (
    add_message,
    get_messages,
    get_last_user_message,
    remove_last_assistant_message,
)
from services.assistant import get_assistant_response
from services.intent_detector import (
    should_search_web,
    detect_browser_intent,
    detect_productivity_intent,
    detect_desktop_intent,
)
from services.browser_service import execute_browser_action
from services.productivity_service import (
    add_note,
    get_all_notes,
    add_todo,
    get_all_todos,
    add_event,
    get_all_events,
    add_reminder,
    get_all_reminders,
    get_daily_planner_summary,
)
from services.desktop_service import (
    launch_app,
    open_folder,
    search_files,
    get_clipboard_text,
    set_clipboard_text,
    get_system_diagnostics,
)
from services.web_search import search_web, format_search_results
from services.url_detector import extract_url
from services.url_service import extract_text_from_url
from services.rag_service import retrieve_advanced_rag_context
from services.vision_service import analyze_image_with_vision, extract_text_ocr
from utils.settings import get_setting
from utils.security import sanitize_input
from utils.errors import safe_execute

logger = logging.getLogger(__name__)


# ==========================================================
# Main Chat Pipeline
# ==========================================================
def process_chat(
    user_prompt: str,
    save_user: bool = True,
) -> Optional[Dict[str, Any]]:
    """
    Processes user query through Nova's complete intelligence pipeline:
    1. Input sanitization & security check
    2. Vision AI & Image Understanding (if active image attached)
    3. Desktop Automation Commands
    4. Desktop Productivity Suite Commands
    5. Browser Desktop Assistant
    6. Multi-document Advanced RAG (Cached Embeddings & Re-ranking)
    7. URL Text Extraction
    8. Web Search
    9. Gemini LLM synthesis
    """
    clean_prompt = sanitize_input(user_prompt)
    if not clean_prompt:
        return None

    start_time = time.perf_counter()

    # Save user prompt to conversation memory
    if save_user:
        add_message("user", clean_prompt)

    # ==========================================================
    # 1. Vision AI Analysis (Active Image attached)
    # ==========================================================
    active_image = st.session_state.get("active_image")
    if active_image is not None:
        vision_mode = st.session_state.get("vision_mode", "general")
        logger.info(f"Processing Vision AI prompt with mode '{vision_mode}'...")

        if vision_mode == "ocr":
            ocr_res = extract_text_ocr(active_image)
            response_text = f"### 🔤 Extracted Text ({ocr_res['engine']}):\n\n{ocr_res['text']}"
            used_ocr = True
        else:
            response_text = analyze_image_with_vision(
                image=active_image,
                prompt=clean_prompt,
                analysis_type=vision_mode,
            )
            used_ocr = False

        add_message("assistant", response_text)
        elapsed = round(time.perf_counter() - start_time, 2)

        return {
            "text": response_text,
            "metadata": {
                "response_time": elapsed,
                "model": "Gemini 2.5 Flash Vision",
                "used_pdf": False,
                "used_web": False,
                "used_url": False,
                "used_browser": False,
                "used_vision": True,
                "used_ocr": used_ocr,
                "confidence": {"score": 95.0, "level": "High"},
            },
            "citations": [],
        }

    # ==========================================================
    # 2. Desktop System Automation Commands
    # ==========================================================
    desktop_intent = detect_desktop_intent(clean_prompt)
    if desktop_intent:
        logger.info(f"Desktop intent detected: {desktop_intent}")
        act = desktop_intent["action_type"]
        response_text = ""

        if act == "launch_app":
            res = launch_app(desktop_intent["target"])
            response_text = res["message"]

        elif act == "open_folder":
            res = open_folder(desktop_intent["target"])
            response_text = res["message"]

        elif act == "search_files":
            matches = search_files(desktop_intent["target"])
            if matches:
                lines = [f"### 🔍 Found {len(matches)} matching files:\n"]
                for f in matches:
                    lines.append(f"- 📄 **{f['name']}** ({f['size_kb']} KB) — `{f['path']}`")
                response_text = "\n".join(lines)
            else:
                response_text = f"🔍 No files found matching **'{desktop_intent['target']}'**."

        elif act == "copy_clipboard":
            success = set_clipboard_text(desktop_intent["text"])
            response_text = f"📋 Copied to system clipboard: **'{desktop_intent['text']}'**" if success else "⚠️ Clipboard error."

        elif act == "read_clipboard":
            text = get_clipboard_text()
            response_text = f"### 📋 System Clipboard Content:\n\n```text\n{text}\n```" if text else "📋 System clipboard is empty."

        elif act == "system_stats":
            diag = get_system_diagnostics()
            response_text = diag["summary_markdown"]

        if response_text:
            add_message("assistant", response_text)
            elapsed = round(time.perf_counter() - start_time, 2)
            return {
                "text": response_text,
                "metadata": {
                    "response_time": elapsed,
                    "model": "Nova Desktop Controller",
                    "used_pdf": False,
                    "used_web": False,
                    "used_url": False,
                    "used_browser": False,
                    "used_desktop": True,
                    "confidence": {"score": 100.0, "level": "High"},
                },
                "citations": [],
            }

    # ==========================================================
    # 3. Desktop Productivity Commands Check
    # ==========================================================
    prod_intent = detect_productivity_intent(clean_prompt)
    if prod_intent:
        logger.info(f"Productivity intent detected: {prod_intent}")
        act = prod_intent["action_type"]
        response_text = ""

        if act == "show_planner":
            planner_data = get_daily_planner_summary()
            response_text = planner_data["summary_markdown"]

        elif act == "create_note":
            res = add_note(prod_intent["title"], prod_intent["content"])
            response_text = f"📝 Saved Note **'{res['title']}'** to database."

        elif act == "show_notes":
            notes = get_all_notes()
            if notes:
                lines = ["### 📋 Saved Notes\n"]
                for n in notes:
                    lines.append(f"- 📝 **{n['title']}**: {n['content']}")
                response_text = "\n".join(lines)
            else:
                response_text = "📋 No saved notes found."

        elif act == "create_todo":
            res = add_todo(prod_intent["task"], priority=prod_intent.get("priority", "Medium"))
            response_text = f"✅ Added Task **'{res['task']}'** `[{res['priority']}]` to checklist."

        elif act == "show_todos":
            todos = get_all_todos()
            if todos:
                lines = ["### ✅ To-do Checklist\n"]
                for t in todos:
                    st_icon = "☑️" if t["status"] == "completed" else "🔲"
                    lines.append(f"- {st_icon} `[{t['priority']}]` **{t['task']}** (Due: {t['due_date']})")
                response_text = "\n".join(lines)
            else:
                response_text = "✅ No tasks in checklist."

        elif act == "create_event":
            res = add_event(prod_intent["title"], prod_intent["start_time"])
            response_text = f"📅 Scheduled Event **'{res['title']}'** for `{res['start_time']}`."

        elif act == "show_calendar":
            events = get_all_events()
            if events:
                lines = ["### 📅 Scheduled Events\n"]
                for e in events:
                    lines.append(f"- 🕒 **{e['start_time']}**: {e['title']}")
                response_text = "\n".join(lines)
            else:
                response_text = "📅 No calendar events scheduled."

        elif act == "create_reminder":
            res = add_reminder(prod_intent["reminder_text"], prod_intent["remind_at"])
            response_text = f"🔔 Set Reminder **'{res['reminder_text']}'** (`{res['remind_at']}`)."

        elif act == "show_reminders":
            rems = get_all_reminders()
            if rems:
                lines = ["### 🔔 Active Reminders\n"]
                for r in rems:
                    lines.append(f"- 🔔 **{r['reminder_text']}** (`{r['remind_at']}`)")
                response_text = "\n".join(lines)
            else:
                response_text = "🔔 No active reminders set."

        if response_text:
            add_message("assistant", response_text)
            elapsed = round(time.perf_counter() - start_time, 2)
            return {
                "text": response_text,
                "metadata": {
                    "response_time": elapsed,
                    "model": "Nova Productivity Engine",
                    "used_pdf": False,
                    "used_web": False,
                    "used_url": False,
                    "used_browser": False,
                    "used_productivity": True,
                    "confidence": {"score": 100.0, "level": "High"},
                },
                "citations": [],
            }

    # ==========================================================
    # 4. Desktop Browser Assistant Check
    # ==========================================================
    browser_intent = detect_browser_intent(clean_prompt)
    if browser_intent:
        logger.info(f"Browser intent detected: {browser_intent}")
        browser_res = execute_browser_action(
            action_type=browser_intent["action_type"],
            target=browser_intent["target"],
        )

        response_text = browser_res["message"]
        add_message("assistant", response_text)
        elapsed = round(time.perf_counter() - start_time, 2)

        return {
            "text": response_text,
            "metadata": {
                "response_time": elapsed,
                "model": "Nova Desktop Assistant",
                "used_pdf": False,
                "used_web": False,
                "used_url": False,
                "used_browser": True,
                "used_vision": False,
                "browser_action": browser_res,
                "confidence": {"score": 100.0, "level": "High"},
            },
            "citations": [],
        }

    document_context: Optional[str] = None
    web_context: Optional[str] = None
    url_context: Optional[str] = None
    citations = []
    rag_confidence = {"score": 0.0, "level": "N/A"}

    # ==========================================================
    # 5. Advanced Multi-Document RAG (FAISS + BM25 + RRF + Re-ranking)
    # ==========================================================
    documents = st.session_state.get("documents", [])
    if documents:
        try:
            rag_top_k = get_setting("rag_top_k", 4)
            rag_output = retrieve_advanced_rag_context(
                documents=documents,
                query=clean_prompt,
                top_k=rag_top_k,
            )
            document_context = rag_output.get("document_context")
            citations = rag_output.get("citations", [])
            rag_confidence = rag_output.get("confidence", {"score": 0.0, "level": "Low"})
        except Exception as e:
            logger.error(f"Failed during Advanced RAG processing: {e}")

    # ==========================================================
    # 6. URL Reader
    # ==========================================================
    url = extract_url(clean_prompt)
    if url:
        try:
            webpage = extract_text_from_url(url)
            if webpage:
                url_context = webpage[:12000]
        except Exception as e:
            logger.warning(f"Error fetching URL content: {e}")

    # ==========================================================
    # 7. Web Search
    # ==========================================================
    if should_search_web(clean_prompt):
        try:
            results = search_web(clean_prompt)
            if results:
                web_context = format_search_results(results)
        except Exception as e:
            logger.warning(f"Error executing web search: {e}")

    # ==========================================================
    # 8. Gemini Synthesis
    # ==========================================================
    assistant_response = get_assistant_response(
        messages=get_messages(),
        document_context=document_context,
        web_context=web_context,
        url_context=url_context,
    )

    # Save assistant response to memory
    add_message("assistant", assistant_response)

    elapsed = round(time.perf_counter() - start_time, 2)

    return {
        "text": assistant_response,
        "metadata": {
            "response_time": elapsed,
            "model": "Gemini",
            "used_pdf": bool(document_context),
            "used_web": bool(web_context),
            "used_url": bool(url_context),
            "used_browser": False,
            "used_vision": False,
            "confidence": rag_confidence,
        },
        "citations": citations,
    }


# ==========================================================
# Regenerate Response
# ==========================================================
def regenerate_response() -> Optional[Dict[str, Any]]:
    """
    Regenerates response for the previous user prompt.
    """
    user_prompt = get_last_user_message()
    if not user_prompt:
        return None

    remove_last_assistant_message()
    return process_chat(user_prompt=user_prompt, save_user=False)