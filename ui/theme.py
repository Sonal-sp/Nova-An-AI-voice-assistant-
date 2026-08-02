import streamlit as st
from utils.settings import get_setting


def apply_theme():
    """
    Applies comprehensive custom CSS dynamic styling according to stored theme setting ('Dark', 'Light', 'Nova Cyberpunk').
    Fixes component-level background and text color overrides.
    """
    theme_name = get_setting("theme", "Dark")

    if theme_name == "Light":
        theme_css = """
        <style>
            /* 1. Main App Container & Headers */
            .stApp, [data-testid="stAppViewContainer"], header[data-testid="stHeader"] {
                background-color: #F8FAFC !important;
                color: #0F172A !important;
            }

            /* 2. Sidebar Container */
            section[data-testid="stSidebar"] {
                background-color: #FFFFFF !important;
                border-right: 1px solid #E2E8F0 !important;
            }
            section[data-testid="stSidebar"] * {
                color: #0F172A !important;
            }

            /* 3. Typography & Text Elements */
            h1, h2, h3, h4, h5, h6, p, label, span, div {
                color: #0F172A !important;
            }

            /* 4. Chat Messages & Cards */
            [data-testid="stChatMessage"] {
                background-color: #FFFFFF !important;
                color: #0F172A !important;
                border: 1px solid #E2E8F0 !important;
                border-radius: 12px !important;
                box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05) !important;
            }

            /* 5. Expanders & Containers */
            div[data-testid="stExpander"] {
                background-color: #FFFFFF !important;
                border: 1px solid #E2E8F0 !important;
                border-radius: 8px !important;
            }
            div[data-testid="stExpander"] * {
                color: #0F172A !important;
            }

            /* 6. Form Controls, Inputs & Selectboxes */
            input, textarea, div[data-baseweb="select"] > div {
                background-color: #FFFFFF !important;
                color: #FFFFFF !important;
                border-color: #CBD5E1 !important;
            }

            /* 7. Buttons */
            .stButton > button {
                background-color: #FFFFFF !important;
                color: #2563EB !important;
                border: 1px solid #CBD5E1 !important;
                font-weight: 600 !important;
            }
            .stButton > button:hover {
                background-color: #EFF6FF !important;
                border-color: #2563EB !important;
            }

            /* 8. Tabs & Navigation */
            button[data-baseweb="tab"] {
                color: #475569 !important;
            }
            button[aria-selected="true"] {
                color: #2563EB !important;
                border-bottom-color: #2563EB !important;
            }

            /* 9. Metrics Cards */
            [data-testid="stMetricValue"], [data-testid="stMetricLabel"] {
                color: #0F172A !important;
            }

            /* 10. Code & Pre Blocks */
            code, pre {
                background-color: #F1F5F9 !important;
                color: #0F172A !important;
                border: 1px solid #E2E8F0 !important;
            }
        </style>
        """

    elif theme_name == "Nova Cyberpunk":
        theme_css = """
        <style>
            /* Cyberpunk Background & Header */
            .stApp, [data-testid="stAppViewContainer"], header[data-testid="stHeader"] {
                background: linear-gradient(135deg, #0B001A 0%, #1A0033 100%) !important;
                color: #00F0FF !important;
            }

            /* Sidebar */
            section[data-testid="stSidebar"] {
                background-color: #0D0221 !important;
                border-right: 1px solid #FF007F !important;
            }
            section[data-testid="stSidebar"] * {
                color: #00F0FF !important;
            }

            /* Typography */
            h1, h2, h3, h4, h5, h6, label, span {
                color: #00F0FF !important;
            }

            /* Expanders */
            div[data-testid="stExpander"] {
                background-color: #16003B !important;
                border: 1px solid #00F0FF !important;
                border-radius: 10px !important;
                box-shadow: 0 0 10px rgba(0, 240, 255, 0.2) !important;
            }

            /* Buttons */
            .stButton > button {
                border: 1px solid #FF007F !important;
                background-color: #240046 !important;
                color: #00F0FF !important;
            }
            .stButton > button:hover {
                background-color: #FF007F !important;
                color: #FFFFFF !important;
            }

            /* Chat Messages */
            [data-testid="stChatMessage"] {
                background-color: #16003B !important;
                border: 1px solid #FF007F !important;
                color: #00F0FF !important;
            }
        </style>
        """

    else:
        # Default Dark Mode
        theme_css = """
        <style>
            .stApp, [data-testid="stAppViewContainer"], header[data-testid="stHeader"] {
                background-color: #0E1117 !important;
                color: #FAFAFA !important;
            }
            div[data-testid="stExpander"] {
                background-color: #1E293B !important;
                border-radius: 8px !important;
            }
        </style>
        """

    st.markdown(theme_css, unsafe_allow_html=True)
