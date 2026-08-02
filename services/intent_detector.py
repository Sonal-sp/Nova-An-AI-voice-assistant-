import re
import logging
from typing import Optional, Dict, Any

logger = logging.getLogger(__name__)

WEB_KEYWORDS = [
    "latest",
    "today",
    "news",
    "current",
    "weather",
    "stock",
    "price",
    "live",
    "update",
    "recent",
    "headline",
    "who won",
    "score",
    "match",
]


def should_search_web(prompt: str) -> bool:
    """
    Checks if prompt implies live web search intent.
    """
    if not prompt:
        return False
    prompt_lower = prompt.lower()
    return any(keyword in prompt_lower for keyword in WEB_KEYWORDS)


def detect_browser_intent(prompt: str) -> Optional[Dict[str, str]]:
    """
    Detects if the user prompt is a desktop browser command.
    """
    if not prompt or not prompt.strip():
        return None

    clean_prompt = prompt.strip()

    # 1. YouTube Search
    yt_match = re.search(
        r"(?:search\s+youtube\s+for|youtube\s+search|find\s+on\s+youtube|search\s+on\s+youtube)\s+(.+)",
        clean_prompt,
        re.IGNORECASE,
    )
    if yt_match:
        return {"action_type": "search_youtube", "target": yt_match.group(1).strip()}

    # 2. Google Maps Search
    maps_match = re.search(
        r"(?:search\s+(?:google\s+)?maps\s+for|maps\s+search|find\s+on\s+maps|show\s+on\s+maps)\s+(.+)",
        clean_prompt,
        re.IGNORECASE,
    )
    if maps_match:
        return {"action_type": "search_maps", "target": maps_match.group(1).strip()}

    # 3. Explicit Google Search command
    g_match = re.search(
        r"(?:search\s+google\s+for|google\s+search|search\s+on\s+google)\s+(.+)",
        clean_prompt,
        re.IGNORECASE,
    )
    if g_match:
        return {"action_type": "search_google", "target": g_match.group(1).strip()}

    # 4. Open Presets or URLs
    open_match = re.search(
        r"^(?:open|launch|go\s+to|navigate\s+to)\s+([a-zA-Z0-9.\-_:/]+(?:\.[a-zA-Z]{2,})?)$",
        clean_prompt,
        re.IGNORECASE,
    )
    if open_match:
        target = open_match.group(1).strip()
        target_lower = target.lower()

        presets = ["github", "gmail", "chatgpt", "youtube", "google", "maps", "stackoverflow", "linkedin", "reddit"]
        if target_lower in presets:
            return {"action_type": "open_preset", "target": target_lower}

        if "." in target or target_lower.startswith("http"):
            return {"action_type": "open_url", "target": target}

        return {"action_type": "open_preset", "target": target_lower}

    return None


def detect_productivity_intent(prompt: str) -> Optional[Dict[str, Any]]:
    """
    Detects if user prompt is a productivity action request.

    Supported intents:
    - "show daily planner", "my planner", "today's agenda"
    - "create note <title>: <content>", "add note <title>: <content>", "show notes"
    - "add task <task>", "add todo <task>", "show todos", "show tasks"
    - "schedule event <title> at <time>", "show calendar"
    - "set reminder <text> at <time>", "show reminders"

    Returns
    -------
    Optional[Dict[str, Any]]
        Action type and extracted parameters or None.
    """
    if not prompt or not prompt.strip():
        return None

    clean = prompt.strip()
    lower = clean.lower()

    # 1. Daily Planner
    if any(k in lower for k in ["show daily planner", "my daily planner", "daily planner", "today's agenda", "show agenda", "my agenda"]):
        return {"action_type": "show_planner"}

    # 2. Notes - Create Note
    note_create = re.search(r"(?:create\s+note|add\s+note|new\s+note)\s+([^:]+)(?::\s*(.+))?", clean, re.IGNORECASE)
    if note_create:
        title = note_create.group(1).strip()
        content = note_create.group(2).strip() if note_create.group(2) else title
        return {"action_type": "create_note", "title": title, "content": content}

    # 3. Notes - Show Notes
    if any(k in lower for k in ["show notes", "list notes", "my notes", "get notes"]):
        return {"action_type": "show_notes"}

    # 4. To-do - Create Task
    todo_create = re.search(r"(?:add\s+task|add\s+todo|create\s+task|new\s+task|create\s+todo)\s+(.+)", clean, re.IGNORECASE)
    if todo_create:
        task_str = todo_create.group(1).strip()
        # Check optional due date or priority
        priority = "Medium"
        if "priority high" in task_str.lower():
            priority = "High"
            task_str = re.sub(r"priority\s+high", "", task_str, flags=re.IGNORECASE).strip()
        elif "priority low" in task_str.lower():
            priority = "Low"
            task_str = re.sub(r"priority\s+low", "", task_str, flags=re.IGNORECASE).strip()

        return {"action_type": "create_todo", "task": task_str, "priority": priority}

    # 5. To-do - Show Tasks
    if any(k in lower for k in ["show todos", "show tasks", "list todos", "list tasks", "my todos", "my tasks"]):
        return {"action_type": "show_todos"}

    # 6. Calendar Event
    event_create = re.search(r"(?:schedule\s+event|add\s+event|new\s+event)\s+([^\b]+?)(?:\s+at\s+(.+))?$", clean, re.IGNORECASE)
    if event_create:
        title = event_create.group(1).strip()
        start_time = event_create.group(2).strip() if event_create.group(2) else "Today 3:00 PM"
        return {"action_type": "create_event", "title": title, "start_time": start_time}

    if any(k in lower for k in ["show calendar", "show events", "my calendar", "my events"]):
        return {"action_type": "show_calendar"}

    # 7. Reminders
    rem_create = re.search(r"(?:set\s+reminder|add\s+reminder|remind\s+me\s+to)\s+([^\b]+?)(?:\s+at\s+(.+))?$", clean, re.IGNORECASE)
    if rem_create:
        rem_text = rem_create.group(1).strip()
        rem_time = rem_create.group(2).strip() if rem_create.group(2) else "In 30 minutes"
        return {"action_type": "create_reminder", "reminder_text": rem_text, "remind_at": rem_time}

    if any(k in lower for k in ["show reminders", "list reminders", "my reminders"]):
        return {"action_type": "show_reminders"}

    return None