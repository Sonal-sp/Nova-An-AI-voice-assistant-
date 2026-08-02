import streamlit as st
from services.integrations_service import (
    github_search_repos,
    github_get_user_profile,
    slack_send_message,
    discord_send_message,
    gmail_create_draft,
    gmail_search_unread,
    gdrive_search_files,
    gcalendar_list_events,
    gcalendar_create_event,
    notion_search_pages,
    notion_create_page,
)


def render_integrations_dashboard():
    """
    Renders the Cloud Integrations Control Dashboard in Streamlit.
    """
    st.markdown("## 🌐 Cloud Integrations Control Center")
    st.caption("Connect and control external cloud services: Gmail, Google Drive, Google Calendar, GitHub, Notion, Slack, and Discord.")

    t_github, t_slack, t_discord, t_google, t_notion = st.tabs([
        "💻 GitHub",
        "💬 Slack",
        "🎮 Discord",
        "📧 Gmail & Drive",
        "📝 Notion",
    ])

    # 1. GitHub Tab
    with t_github:
        st.subheader("💻 GitHub Repository & User Lookup")
        gh_col1, gh_col2 = st.columns(2)
        with gh_col1:
            q = st.text_input("Search GitHub Repositories", value="voice assistant python", key="gh_search_q")
            if st.button("🔍 Search Repositories", use_container_width=True):
                repos = github_search_repos(q)
                if repos:
                    for r in repos:
                        st.markdown(f"- ⭐ **[{r['name']}]({r['url']})** ({r['stars']} stars): {r['description']}")
                else:
                    st.info("No repositories found.")

        with gh_col2:
            u = st.text_input("GitHub Username Lookup", value="torvalds", key="gh_user_u")
            if st.button("👤 Get User Profile", use_container_width=True):
                user = github_get_user_profile(u)
                if user:
                    st.image(user["avatar_url"], width=80)
                    st.write(f"**{user['name']}** (`@{user['username']}`)")
                    st.write(f"Public Repos: {user['public_repos']} | Followers: {user['followers']}")
                    st.markdown(f"[View Profile]({user['html_url']})")

    # 2. Slack Tab
    with t_slack:
        st.subheader("💬 Slack Webhook Dispatcher")
        slack_url = st.text_input("Slack Incoming Webhook URL", type="password", key="slack_webhook_input")
        slack_msg = st.text_area("Message to Post", value="Hello from Nova Assistant!", key="slack_msg_input")
        if st.button("📤 Send Slack Notification", use_container_width=True):
            res = slack_send_message(slack_url, slack_msg)
            if res["success"]:
                st.success(res["message"])
            else:
                st.error(res["message"])

    # 3. Discord Tab
    with t_discord:
        st.subheader("🎮 Discord Webhook Dispatcher")
        discord_url = st.text_input("Discord Webhook URL", type="password", key="discord_webhook_input")
        discord_msg = st.text_area("Message to Post", value="Nova AI Assistant online!", key="discord_msg_input")
        if st.button("🚀 Post to Discord Channel", use_container_width=True):
            res = discord_send_message(discord_url, discord_msg)
            if res["success"]:
                st.success(res["message"])
            else:
                st.error(res["message"])

    # 4. Google Workspace Tab
    with t_google:
        st.subheader("📧 Gmail, Drive & Calendar Integration")
        g_c1, g_c2 = st.columns(2)
        with g_c1:
            st.markdown("#### 📧 Gmail & Drive")
            rec = st.text_input("Recipient Email", value="user@example.com", key="gmail_rec")
            sub = st.text_input("Email Subject", value="Project Update", key="gmail_sub")
            body = st.text_area("Draft Body", value="Hi, here is the sprint progress...", key="gmail_body")
            if st.button("📝 Create Gmail Draft", use_container_width=True):
                res = gmail_create_draft(rec, sub, body)
                st.success(res["message"])

        with g_c2:
            st.markdown("#### 📅 Google Calendar")
            cal_title = st.text_input("Event Title", value="Sprint Review", key="gcal_title")
            cal_time = st.text_input("Start Time", value="17:00 Today", key="gcal_time")
            if st.button("📅 Schedule Calendar Event", use_container_width=True):
                res = gcalendar_create_event(cal_title, cal_time)
                st.success(res["message"])

    # 5. Notion Tab
    with t_notion:
        st.subheader("📝 Notion Workspace Integration")
        n_c1, n_c2 = st.columns(2)
        with n_c1:
            n_q = st.text_input("Search Notion Pages", value="Engineering", key="notion_q")
            if st.button("🔍 Search Notion", use_container_width=True):
                pages = notion_search_pages(n_q)
                for p in pages:
                    st.markdown(f"- 📄 **{p['title']}** (`{p['category']}`)")
        with n_c2:
            n_title = st.text_input("New Page Title", value="Architecture Notes", key="notion_title")
            n_content = st.text_area("Page Body", value="Details on pipeline architecture...", key="notion_body")
            if st.button("📝 Create Notion Page", use_container_width=True):
                res = notion_create_page(n_title, n_content)
                st.success(res["message"])
