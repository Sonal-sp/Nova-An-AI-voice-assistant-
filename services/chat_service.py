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
from services.intent_detector import should_search_web, detect_browser_intent
from services.browser_service import execute_browser_action
from services.web_search import search_web, format_search_results
from services.url_detector import extract_url
from services.url_service import extract_text_from_url
from services.rag_service import retrieve_advanced_rag_context
from services.vision_service import analyze_image_with_vision, extract_text_ocr

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
    1. Vision AI & Image Understanding (if active image uploaded)
    2. Browser Desktop Assistant (Open Websites, Google/YouTube/Maps Search)
    3. Multi-document Advanced RAG (FAISS + BM25 + RRF + Re-ranking)
    4. URL Text Extraction
    5. Web Search
    6. Gemini LLM synthesis
    """
    if not user_prompt or not user_prompt.strip():
        return None

    start_time = time.perf_counter()

    # Save user prompt to conversation memory
    if save_user:
        add_message("user", user_prompt)

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
                prompt=user_prompt,
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
    # 2. Desktop Browser Assistant Check
    # ==========================================================
    browser_intent = detect_browser_intent(user_prompt)
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
    # 3. Advanced Multi-Document RAG (FAISS + BM25 + RRF + Re-ranking)
    # ==========================================================
    documents = st.session_state.get("documents", [])
    if documents:
        try:
            rag_output = retrieve_advanced_rag_context(
                documents=documents,
                query=user_prompt,
                top_k=4,
            )
            document_context = rag_output.get("document_context")
            citations = rag_output.get("citations", [])
            rag_confidence = rag_output.get("confidence", {"score": 0.0, "level": "Low"})
        except Exception as e:
            logger.error(f"Failed during Advanced RAG processing: {e}")

    # ==========================================================
    # 4. URL Reader
    # ==========================================================
    url = extract_url(user_prompt)
    if url:
        try:
            webpage = extract_text_from_url(url)
            if webpage:
                url_context = webpage[:12000]
        except Exception as e:
            logger.warning(f"Error fetching URL content: {e}")

    # ==========================================================
    # 5. Web Search
    # ==========================================================
    if should_search_web(user_prompt):
        try:
            results = search_web(user_prompt)
            if results:
                web_context = format_search_results(results)
        except Exception as e:
            logger.warning(f"Error executing web search: {e}")

    # ==========================================================
    # 6. Gemini Synthesis
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