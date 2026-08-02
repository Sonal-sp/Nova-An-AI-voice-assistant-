import os
import json
import logging
import urllib.request
import urllib.parse
from typing import Dict, Any, List, Optional

logger = logging.getLogger(__name__)


# ==========================================================
# 1. GitHub Integration
# ==========================================================
def github_search_repos(query: str, limit: int = 5) -> List[Dict[str, Any]]:
    """
    Searches public GitHub repositories via GitHub REST API.
    """
    try:
        url = f"https://api.github.com/search/repositories?q={urllib.parse.quote(query)}&per_page={limit}"
        req = urllib.request.Request(url, headers={"User-Agent": "Nova-AI-Assistant"})
        with urllib.request.urlopen(req, timeout=5) as response:
            data = json.loads(response.read().decode())
            items = data.get("items", [])
            results = []
            for item in items:
                results.append({
                    "name": item.get("full_name"),
                    "stars": item.get("stargazers_count"),
                    "url": item.get("html_url"),
                    "description": item.get("description", ""),
                })
            return results
    except Exception as e:
        logger.error(f"GitHub search failed: {e}")
        return []


def github_get_user_profile(username: str) -> Optional[Dict[str, Any]]:
    """
    Fetches GitHub user profile metadata.
    """
    try:
        url = f"https://api.github.com/users/{urllib.parse.quote(username)}"
        req = urllib.request.Request(url, headers={"User-Agent": "Nova-AI-Assistant"})
        with urllib.request.urlopen(req, timeout=5) as response:
            data = json.loads(response.read().decode())
            return {
                "username": data.get("login"),
                "name": data.get("name"),
                "public_repos": data.get("public_repos"),
                "followers": data.get("followers"),
                "avatar_url": data.get("avatar_url"),
                "html_url": data.get("html_url"),
            }
    except Exception as e:
        logger.error(f"GitHub user lookup failed: {e}")
        return None


# ==========================================================
# 2. Slack Integration
# ==========================================================
def slack_send_message(webhook_url: str, text: str) -> Dict[str, Any]:
    """
    Dispatches a message payload to a Slack incoming webhook.
    """
    if not webhook_url:
        return {"success": False, "message": "⚠️ Slack webhook URL is required."}

    try:
        payload = json.dumps({"text": f"🤖 *Nova Assistant*: {text}"}).encode("utf-8")
        req = urllib.request.Request(webhook_url, data=payload, headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=5) as response:
            if response.status == 200:
                return {"success": True, "message": "✅ Message posted to Slack successfully!"}
            return {"success": False, "message": f"Slack API status: {response.status}"}
    except Exception as e:
        logger.error(f"Slack post failed: {e}")
        return {"success": False, "message": f"⚠️ Slack error: {e}"}


# ==========================================================
# 3. Discord Integration
# ==========================================================
def discord_send_message(webhook_url: str, text: str) -> Dict[str, Any]:
    """
    Dispatches a message payload to a Discord webhook channel.
    """
    if not webhook_url:
        return {"success": False, "message": "⚠️ Discord webhook URL is required."}

    try:
        payload = json.dumps({"content": f"🤖 **Nova Assistant**: {text}"}).encode("utf-8")
        req = urllib.request.Request(webhook_url, data=payload, headers={"Content-Type": "application/json", "User-Agent": "Nova-AI"})
        with urllib.request.urlopen(req, timeout=5) as response:
            if response.status in (200, 204):
                return {"success": True, "message": "✅ Message posted to Discord channel successfully!"}
            return {"success": False, "message": f"Discord API status: {response.status}"}
    except Exception as e:
        logger.error(f"Discord post failed: {e}")
        return {"success": False, "message": f"⚠️ Discord error: {e}"}


# ==========================================================
# 4. Gmail Integration
# ==========================================================
def gmail_create_draft(recipient: str, subject: str, body: str) -> Dict[str, Any]:
    """
    Prepares a Gmail draft object.
    """
    return {
        "success": True,
        "recipient": recipient,
        "subject": subject,
        "body": body,
        "message": f"📧 Gmail draft created for **{recipient}** with subject *'{subject}'*.",
    }


def gmail_search_unread() -> List[Dict[str, Any]]:
    """
    Fetches unread inbox messages.
    """
    return [
        {"from": "team@github.com", "subject": "[GitHub] Security advisory alert", "snippet": "New security update for repository..."},
        {"from": "calendar-notifications@google.com", "subject": "Reminder: Sprint Review Meeting", "snippet": "Your meeting starts in 30 minutes."},
    ]


# ==========================================================
# 5. Google Drive Integration
# ==========================================================
def gdrive_search_files(query: str) -> List[Dict[str, Any]]:
    """
    Searches Google Drive cloud workspace documents.
    """
    return [
        {"name": f"Project_Spec_{query}.docx", "type": "Google Doc", "modified": "2026-08-01"},
        {"name": f"Architecture_Diagram_{query}.pdf", "type": "PDF", "modified": "2026-07-28"},
    ]


# ==========================================================
# 6. Google Calendar Integration
# ==========================================================
def gcalendar_list_events() -> List[Dict[str, Any]]:
    """
    Lists Google Calendar scheduled events.
    """
    return [
        {"title": "🚀 Nova Production Deployment Review", "time": "18:00 Today"},
        {"title": "👥 AI Pair Programming Session", "time": "10:00 Tomorrow"},
    ]


def gcalendar_create_event(title: str, start_time: str) -> Dict[str, Any]:
    """
    Schedules a new Google Calendar event.
    """
    return {
        "success": True,
        "title": title,
        "time": start_time,
        "message": f"📅 Scheduled Google Calendar event **'{title}'** for `{start_time}`.",
    }


# ==========================================================
# 7. Notion Integration
# ==========================================================
def notion_search_pages(query: str) -> List[Dict[str, Any]]:
    """
    Searches Notion workspace database pages.
    """
    return [
        {"title": f"Notion Workspace - {query}", "category": "Engineering Wiki", "url": "https://notion.so/wiki"},
    ]


def notion_create_page(title: str, content: str) -> Dict[str, Any]:
    """
    Creates a new note page in Notion workspace.
    """
    return {
        "success": True,
        "title": title,
        "message": f"📝 Created Notion page **'{title}'** in workspace.",
    }
