import streamlit as st
import datetime

from services.productivity_service import (
    add_note,
    get_all_notes,
    delete_note,
    add_todo,
    get_all_todos,
    toggle_todo_status,
    delete_todo,
    add_event,
    get_all_events,
    delete_event,
    add_reminder,
    get_all_reminders,
    delete_reminder,
    get_daily_planner_summary,
)


def render_productivity_dashboard():
    """
    Renders interactive Streamlit Productivity Dashboard tabs for Notes, To-dos, Calendar, Reminders, and Daily Planner.
    """
    st.markdown("## ⚡ Productivity Suite")
    st.caption("Manage Notes, Tasks, Calendar Events, Reminders, and Daily Agenda.")

    tab_planner, tab_notes, tab_todos, tab_calendar, tab_reminders = st.tabs(
        [
            "📅 Daily Planner",
            "📋 Notes",
            "✅ To-do Checklist",
            "📅 Calendar",
            "⏰ Reminders & Timers",
        ]
    )

    # ==========================================================
    # 1. Daily Planner Overview
    # ==========================================================
    with tab_planner:
        st.subheader("📅 Today's Aggregated Agenda")
        summary_data = get_daily_planner_summary()
        st.markdown(summary_data["summary_markdown"])

    # ==========================================================
    # 2. Notes Manager
    # ==========================================================
    with tab_notes:
        st.subheader("📋 Notes Manager")

        with st.expander("➕ Create New Note", expanded=False):
            with st.form("create_note_form", clear_on_submit=True):
                note_title = st.text_input("Note Title", placeholder="e.g. Q3 Architecture Notes")
                note_content = st.text_area("Note Content", placeholder="Write your note details here...")
                note_tags = st.text_input("Tags (comma separated)", placeholder="work, architecture, nova")
                submitted = st.form_submit_button("💾 Save Note", use_container_width=True)
                if submitted and note_title.strip():
                    add_note(note_title, note_content, note_tags)
                    st.success(f"Saved note '{note_title}'!")
                    st.rerun()

        search_q = st.text_input("🔍 Search Notes", placeholder="Search by title, content, or tag...")
        notes = get_all_notes(search_q)

        if notes:
            for note in notes:
                with st.expander(f"📝 **{note['title']}** — {note['updated_at'][:10]}", expanded=False):
                    if note["tags"]:
                        st.caption(f"🏷️ Tags: `{note['tags']}`")
                    st.markdown(note["content"])
                    if st.button("🗑️ Delete Note", key=f"del_note_{note['id']}", use_container_width=True):
                        delete_note(note["id"])
                        st.rerun()
        else:
            st.info("No notes found.")

    # ==========================================================
    # 3. To-do Checklist
    # ==========================================================
    with tab_todos:
        st.subheader("✅ To-do Checklist")

        with st.expander("➕ Add New Task", expanded=False):
            with st.form("create_todo_form", clear_on_submit=True):
                col_t1, col_t2 = st.columns([2, 1])
                with col_t1:
                    task_text = st.text_input("Task Description", placeholder="e.g. Prepare presentation slides")
                with col_t2:
                    priority_val = st.selectbox("Priority", ["High", "Medium", "Low"], index=1)
                due_date_val = st.date_input("Due Date", value=datetime.date.today())
                submitted_todo = st.form_submit_button("➕ Add Task", use_container_width=True)
                if submitted_todo and task_text.strip():
                    add_todo(task_text, due_date=due_date_val.isoformat(), priority=priority_val)
                    st.success(f"Added task '{task_text}'!")
                    st.rerun()

        status_filter = st.radio("Filter Tasks", ["all", "pending", "completed"], horizontal=True)
        todos = get_all_todos(status_filter)

        if todos:
            for todo in todos:
                c1, c2, c3, c4 = st.columns([0.1, 2, 0.8, 0.5])
                is_done = todo["status"] == "completed"

                with c1:
                    checked = st.checkbox("", value=is_done, key=f"todo_chk_{todo['id']}")
                    if checked != is_done:
                        toggle_todo_status(todo["id"])
                        st.rerun()

                with c2:
                    task_display = f"~~{todo['task']}~~" if is_done else f"**{todo['task']}**"
                    st.markdown(task_display)

                with c3:
                    prio_color = "#EF4444" if todo["priority"] == "High" else "#F59E0B" if todo["priority"] == "Medium" else "#6B7280"
                    st.markdown(
                        f"<span style='background-color:{prio_color}; color:white; padding:2px 6px; border-radius:10px; font-size:0.75rem; font-weight:bold;'>{todo['priority']}</span>",
                        unsafe_allow_html=True,
                    )

                with c4:
                    if st.button("🗑️", key=f"del_todo_{todo['id']}"):
                        delete_todo(todo["id"])
                        st.rerun()
        else:
            st.info("No tasks in checklist.")

    # ==========================================================
    # 4. Calendar Events
    # ==========================================================
    with tab_calendar:
        st.subheader("📅 Calendar Agenda")

        with st.expander("➕ Schedule New Event", expanded=False):
            with st.form("create_event_form", clear_on_submit=True):
                ev_title = st.text_input("Event Title", placeholder="e.g. Sprint Review Meeting")
                ev_start = st.text_input("Start Time / Date", placeholder="e.g. 2026-08-03 14:00")
                ev_loc = st.text_input("Location / Link", placeholder="e.g. Zoom / Conference Room A")
                ev_desc = st.text_area("Description", placeholder="Meeting agenda...")
                submitted_ev = st.form_submit_button("📅 Schedule Event", use_container_width=True)
                if submitted_ev and ev_title.strip():
                    add_event(ev_title, ev_start, location=ev_loc, description=ev_desc)
                    st.success(f"Scheduled event '{ev_title}'!")
                    st.rerun()

        events = get_all_events()
        if events:
            for ev in events:
                with st.expander(f"📅 **{ev['title']}** — {ev['start_time']}", expanded=False):
                    if ev["location"]:
                        st.caption(f"📍 Location: `{ev['location']}`")
                    if ev["description"]:
                        st.markdown(ev["description"])
                    if st.button("🗑️ Delete Event", key=f"del_ev_{ev['id']}", use_container_width=True):
                        delete_event(ev["id"])
                        st.rerun()
        else:
            st.info("No upcoming calendar events.")

    # ==========================================================
    # 5. Reminders & Timers
    # ==========================================================
    with tab_reminders:
        st.subheader("⏰ Reminders & Timers")

        with st.form("create_reminder_form", clear_on_submit=True):
            rem_text = st.text_input("Reminder Text", placeholder="e.g. Take break & stretch")
            rem_at = st.text_input("Remind At / Time", placeholder="e.g. 30 minutes")
            submitted_rem = st.form_submit_button("🔔 Set Reminder", use_container_width=True)
            if submitted_rem and rem_text.strip():
                add_reminder(rem_text, rem_at)
                st.success(f"Set reminder '{rem_text}'!")
                st.rerun()

        reminders = get_all_reminders()
        if reminders:
            st.markdown("### 🔔 Active Alerts")
            for rem in reminders:
                col_r1, col_r2 = st.columns([3, 1])
                with col_r1:
                    st.markdown(f"🔔 **{rem['reminder_text']}** (Time: `{rem['remind_at']}`)")
                with col_r2:
                    if st.button("🗑️ Delete", key=f"del_rem_{rem['id']}"):
                        delete_reminder(rem["id"])
                        st.rerun()
        else:
            st.info("No active reminders set.")
