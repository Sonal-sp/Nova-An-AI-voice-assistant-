import datetime
import logging
from typing import List, Dict, Any, Optional

from services.database_service import get_db_connection, init_db

logger = logging.getLogger(__name__)

# Ensure DB tables exist
init_db()


# ==========================================================
# 1. Notes Management
# ==========================================================
def add_note(title: str, content: str, tags: str = "") -> Dict[str, Any]:
    """
    Creates a new Note.
    """
    title_clean = title.strip() if title else "Untitled Note"
    content_clean = content.strip() if content else ""
    tags_clean = tags.strip() if tags else ""

    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO notes (title, content, tags) VALUES (?, ?, ?);",
            (title_clean, content_clean, tags_clean),
        )
        note_id = cursor.lastrowid
        logger.info(f"Created note #{note_id}: {title_clean}")
        return {
            "id": note_id,
            "title": title_clean,
            "content": content_clean,
            "tags": tags_clean,
        }


def get_all_notes(search_query: str = "") -> List[Dict[str, Any]]:
    """
    Retrieves all notes matching optional text search query.
    """
    with get_db_connection() as conn:
        cursor = conn.cursor()
        if search_query and search_query.strip():
            q = f"%{search_query.strip()}%"
            cursor.execute(
                "SELECT * FROM notes WHERE title LIKE ? OR content LIKE ? OR tags LIKE ? ORDER BY updated_at DESC;",
                (q, q, q),
            )
        else:
            cursor.execute("SELECT * FROM notes ORDER BY updated_at DESC;")

        rows = cursor.fetchall()
        return [dict(row) for row in rows]


def delete_note(note_id: int) -> bool:
    """
    Deletes a note by ID.
    """
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM notes WHERE id = ?;", (note_id,))
        return cursor.rowcount > 0


# ==========================================================
# 2. To-do Checklist Management
# ==========================================================
def add_todo(task: str, due_date: str = "", priority: str = "Medium") -> Dict[str, Any]:
    """
    Creates a new To-do item.
    """
    task_clean = task.strip()
    due_clean = due_date.strip() if due_date else datetime.date.today().isoformat()
    prio_clean = priority.capitalize() if priority in ["High", "Medium", "Low"] else "Medium"

    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO todos (task, due_date, priority, status) VALUES (?, ?, ?, 'pending');",
            (task_clean, due_clean, prio_clean),
        )
        todo_id = cursor.lastrowid
        logger.info(f"Created todo #{todo_id}: {task_clean}")
        return {
            "id": todo_id,
            "task": task_clean,
            "due_date": due_clean,
            "priority": prio_clean,
            "status": "pending",
        }


def get_all_todos(status_filter: str = "all") -> List[Dict[str, Any]]:
    """
    Retrieves all to-do items filtered by status.
    """
    with get_db_connection() as conn:
        cursor = conn.cursor()
        if status_filter in ["pending", "completed"]:
            cursor.execute("SELECT * FROM todos WHERE status = ? ORDER BY id DESC;", (status_filter,))
        else:
            cursor.execute("SELECT * FROM todos ORDER BY id DESC;")

        rows = cursor.fetchall()
        return [dict(row) for row in rows]


def toggle_todo_status(todo_id: int) -> bool:
    """
    Toggles to-do item status between 'pending' and 'completed'.
    """
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT status FROM todos WHERE id = ?;", (todo_id,))
        row = cursor.fetchone()
        if not row:
            return False

        new_status = "completed" if row["status"] == "pending" else "pending"
        cursor.execute("UPDATE todos SET status = ? WHERE id = ?;", (new_status, todo_id))
        return True


def delete_todo(todo_id: int) -> bool:
    """
    Deletes a to-do item by ID.
    """
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM todos WHERE id = ?;", (todo_id,))
        return cursor.rowcount > 0


# ==========================================================
# 3. Calendar Events
# ==========================================================
def add_event(
    title: str,
    start_time: str,
    end_time: str = "",
    location: str = "",
    description: str = "",
) -> Dict[str, Any]:
    """
    Schedules a new Calendar Event.
    """
    title_clean = title.strip()
    start_clean = start_time.strip() if start_time else datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO events (title, start_time, end_time, location, description) VALUES (?, ?, ?, ?, ?);",
            (title_clean, start_clean, end_time.strip(), location.strip(), description.strip()),
        )
        event_id = cursor.lastrowid
        logger.info(f"Created event #{event_id}: {title_clean}")
        return {
            "id": event_id,
            "title": title_clean,
            "start_time": start_clean,
            "end_time": end_time.strip(),
            "location": location.strip(),
            "description": description.strip(),
        }


def get_all_events() -> List[Dict[str, Any]]:
    """
    Retrieves all scheduled calendar events.
    """
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM events ORDER BY start_time ASC;")
        rows = cursor.fetchall()
        return [dict(row) for row in rows]


def delete_event(event_id: int) -> bool:
    """
    Deletes a calendar event by ID.
    """
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM events WHERE id = ?;", (event_id,))
        return cursor.rowcount > 0


# ==========================================================
# 4. Reminders
# ==========================================================
def add_reminder(reminder_text: str, remind_at: str) -> Dict[str, Any]:
    """
    Sets a new Reminder alert.
    """
    text_clean = reminder_text.strip()
    time_clean = remind_at.strip() if remind_at else "In 30 minutes"

    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO reminders (reminder_text, remind_at, is_triggered) VALUES (?, ?, 0);",
            (text_clean, time_clean),
        )
        rem_id = cursor.lastrowid
        logger.info(f"Created reminder #{rem_id}: {text_clean}")
        return {
            "id": rem_id,
            "reminder_text": text_clean,
            "remind_at": time_clean,
        }


def get_all_reminders() -> List[Dict[str, Any]]:
    """
    Retrieves all active reminders.
    """
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM reminders ORDER BY id DESC;")
        rows = cursor.fetchall()
        return [dict(row) for row in rows]


def delete_reminder(reminder_id: int) -> bool:
    """
    Deletes a reminder by ID.
    """
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM reminders WHERE id = ?;", (reminder_id,))
        return cursor.rowcount > 0


# ==========================================================
# 5. Daily Planner Aggregator
# ==========================================================
def get_daily_planner_summary() -> Dict[str, Any]:
    """
    Aggregates today's complete agenda: Pending To-dos, Upcoming Events, Active Reminders, and Notes.

    Returns
    -------
    Dict[str, Any]
        Structured dictionary with items and markdown formatted summary string.
    """
    today_str = datetime.date.today().strftime("%B %d, %Y")
    todos = get_all_todos(status_filter="pending")
    events = get_all_events()
    reminders = get_all_reminders()
    notes = get_all_notes()[:5]

    lines = [f"# 📅 Daily Planner Summary — {today_str}\n"]

    lines.append("### ✅ Pending Tasks")
    if todos:
        for t in todos:
            lines.append(f"- `[{t['priority']}]` **{t['task']}** (Due: {t['due_date']})")
    else:
        lines.append("_No pending tasks for today!_")

    lines.append("\n### 📅 Scheduled Events")
    if events:
        for e in events:
            loc = f" @ {e['location']}" if e['location'] else ""
            lines.append(f"- 🕒 **{e['start_time']}**: {e['title']}{loc}")
    else:
        lines.append("_No upcoming calendar events._")

    lines.append("\n### ⏰ Active Reminders")
    if reminders:
        for r in reminders:
            lines.append(f"- 🔔 **{r['reminder_text']}** ({r['remind_at']})")
    else:
        lines.append("_No active reminders set._")

    lines.append("\n### 📋 Recent Notes")
    if notes:
        for n in notes:
            lines.append(f"- 📝 **{n['title']}**: {n['content'][:80]}...")
    else:
        lines.append("_No notes created yet._")

    summary_md = "\n".join(lines)

    return {
        "today": today_str,
        "pending_todos": todos,
        "upcoming_events": events,
        "active_reminders": reminders,
        "recent_notes": notes,
        "summary_markdown": summary_md,
    }
