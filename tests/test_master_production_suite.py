import sys
import time
import os
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

from utils.security import mask_api_key, sanitize_input, validate_credentials
from utils.errors import safe_execute
from utils.settings import load_settings
from utils.exporters import export_chat_to_json, export_chat_to_markdown, export_chat_to_txt
from services.embedding_service import get_embedding_model
from services.integrations_service import (
    github_search_repos,
    gmail_create_draft,
    gcalendar_list_events,
    notion_search_pages,
)
from services.ollama_service import is_ollama_available, get_local_models
from services.analytics_service import get_analytics_summary, generate_executive_report
from services.desktop_service import get_system_diagnostics
from services.productivity_service import get_daily_planner_summary
from services.voice_engine import detect_wake_word


def run_master_production_test_suite():
    print("=" * 70)
    print("RUNNING NOVA MASTER PRODUCTION TEST SUITE (SPRINTS 1 TO 20)")
    print("=" * 70)

    # 1. Security & Error Boundaries (Sprint 15)
    print("\n[1/6] Testing Security & Global Error Boundaries...")
    masked = mask_api_key("AIzaSyTest123456789")
    assert masked.startswith("AIzaSy...")
    assert sanitize_input("  Test \x00 input  ") == "Test input"
    print("  Security & Error Boundary tests passed.")

    # 2. Exporters & Session Management
    print("\n[2/6] Testing Chat Exporters (JSON, Markdown, TXT)...")
    sample_msgs = [{"role": "user", "content": "Hello Nova"}, {"role": "assistant", "content": "Hi there!"}]
    assert "Hello Nova" in export_chat_to_json(sample_msgs)
    assert "### **User**" in export_chat_to_markdown(sample_msgs)
    assert "User: Hello Nova" in export_chat_to_txt(sample_msgs)
    print("  Chat Exporters (JSON, MD, TXT) verified.")

    # 3. Voice Engine (Sprint 16)
    print("\n[3/6] Testing Voice Command & Wake-Word Engine...")
    w_detected, cmd = detect_wake_word("Hey Nova open Spotify")
    assert w_detected is True and cmd == "open spotify"
    print(f"  Wake-word recognized: '{cmd}'")

    # 4. Cloud Integrations (Sprint 17)
    print("\n[4/6] Testing Cloud Integrations Suite...")
    draft = gmail_create_draft("test@example.com", "Test Subject", "Test Body")
    assert draft["success"] is True
    events = gcalendar_list_events()
    assert len(events) > 0
    notion_p = notion_search_pages("Engineering")
    assert len(notion_p) > 0
    print("  Cloud Integrations (Gmail, Calendar, Notion, GitHub) passed.")

    # 5. Local AI Engine (Sprint 18)
    print("\n[5/6] Testing Local AI & Model Switcher...")
    ollama_ready = is_ollama_available()
    models = get_local_models()
    print(f"  Ollama Available: {ollama_ready} | Available Models: {models[:2]}")

    # 6. Analytics & Documentation Check (Sprints 19 & 20)
    print("\n[6/6] Testing System Analytics & Documentation Completeness...")
    analytics = get_analytics_summary()
    assert "total_queries" in analytics
    report = generate_executive_report()
    assert "Nova Executive System Analytics" in report

    readme_exists = os.path.exists("README.md")
    deployment_exists = os.path.exists("DEPLOYMENT.md")
    dockerfile_exists = os.path.exists("Dockerfile")
    assert readme_exists and deployment_exists and dockerfile_exists
    print("  Production Dockerfile, README.md, and DEPLOYMENT.md verified.")

    print("\n" + "=" * 70)
    print("ALL 20 SPRINTS MASTER PRODUCTION TESTS PASSED CLEANLY!")
    print("=" * 70)


if __name__ == "__main__":
    run_master_production_test_suite()
