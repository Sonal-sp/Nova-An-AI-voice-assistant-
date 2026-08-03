import streamlit as st


def apply_theme():
    """
    Applies Nova's Futuristic AI Operating System Cyberpunk Glassmorphic Design System.
    Combines Glassmorphism, Raycast/Claude Desktop minimal aesthetics,
    cyberpunk neon gradients, custom scrollbars, and micro-animations.
    """
    theme_css = """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

        :root {
            --bg-deep: #07090E;
            --bg-card: rgba(15, 23, 42, 0.65);
            --bg-card-hover: rgba(30, 41, 59, 0.75);
            --border-glass: rgba(255, 255, 255, 0.1);
            --border-glow: rgba(56, 189, 248, 0.4);
            --accent-blue: #38BDF8;
            --accent-purple: #A855F7;
            --accent-pink: #EC4899;
            --accent-cyan: #22D3EE;
            --text-primary: #F8FAFC;
            --text-secondary: #94A3B8;
        }

        html, body, [class*="st-"] {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
        }

        /* Custom Scrollbars */
        ::-webkit-scrollbar {
            width: 6px;
            height: 6px;
        }
        ::-webkit-scrollbar-track {
            background: #07090E;
        }
        ::-webkit-scrollbar-thumb {
            background: rgba(148, 163, 184, 0.2);
            border-radius: 10px;
        }
        ::-webkit-scrollbar-thumb:hover {
            background: rgba(56, 189, 248, 0.5);
        }

        /* 1. Main Canvas */
        .stApp, [data-testid="stAppViewContainer"], header[data-testid="stHeader"] {
            background: radial-gradient(circle at 50% 0%, #111827 0%, #07090E 70%) !important;
            color: var(--text-primary) !important;
        }

        /* 2. Glassmorphic Sidebar */
        section[data-testid="stSidebar"] {
            background: rgba(11, 15, 25, 0.85) !important;
            backdrop-filter: blur(20px) saturate(180%) !important;
            -webkit-backdrop-filter: blur(20px) saturate(180%) !important;
            border-right: 1px solid rgba(255, 255, 255, 0.08) !important;
            box-shadow: 10px 0 30px rgba(0, 0, 0, 0.5) !important;
        }
        section[data-testid="stSidebar"] * {
            color: var(--text-primary) !important;
        }

        /* 3. Typography */
        h1, h2, h3 {
            background: linear-gradient(135deg, #F8FAFC 0%, #38BDF8 50%, #A855F7 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-weight: 700 !important;
            letter-spacing: -0.025em !important;
        }
        h4, h5, h6 {
            color: var(--text-primary) !important;
            font-weight: 600 !important;
        }

        /* 4. Chat Message Cards */
        [data-testid="stChatMessage"] {
            background: rgba(15, 23, 42, 0.6) !important;
            backdrop-filter: blur(16px) saturate(180%) !important;
            -webkit-backdrop-filter: blur(16px) saturate(180%) !important;
            border: 1px solid rgba(255, 255, 255, 0.09) !important;
            border-radius: 16px !important;
            box-shadow: 0 8px 24px rgba(0, 0, 0, 0.4) !important;
            margin-bottom: 14px !important;
            padding: 14px 18px !important;
            transition: transform 0.25s ease, border-color 0.25s ease, box-shadow 0.25s ease !important;
        }
        [data-testid="stChatMessage"]:hover {
            transform: translateY(-2px) !important;
            border-color: rgba(56, 189, 248, 0.3) !important;
            box-shadow: 0 12px 32px rgba(0, 0, 0, 0.5), 0 0 15px rgba(56, 189, 248, 0.15) !important;
        }

        /* 5. Raycast Floating Chat Input Bar */
        [data-testid="stBottom"], [data-testid="stChatInputContainer"], [data-testid="stBottom"] * {
            background: transparent !important;
        }
        [data-testid="stChatInput"] {
            background: rgba(15, 23, 42, 0.85) !important;
            backdrop-filter: blur(20px) saturate(180%) !important;
            -webkit-backdrop-filter: blur(20px) saturate(180%) !important;
            border: 1px solid rgba(56, 189, 248, 0.3) !important;
            border-radius: 20px !important;
            box-shadow: 0 12px 40px rgba(0, 0, 0, 0.6), 0 0 20px rgba(56, 189, 248, 0.15) !important;
            transition: all 0.3s ease !important;
        }
        [data-testid="stChatInput"]:focus-within {
            border-color: var(--accent-blue) !important;
            box-shadow: 0 14px 44px rgba(0, 0, 0, 0.7), 0 0 25px rgba(56, 189, 248, 0.35) !important;
        }
        [data-testid="stChatInput"] textarea {
            color: #F8FAFC !important;
            font-size: 15px !important;
        }
        [data-testid="stChatInputSubmitButton"] button {
            background: linear-gradient(135deg, #38BDF8 0%, #8B5CF6 100%) !important;
            border-radius: 12px !important;
            border: none !important;
        }

        /* 6. Buttons */
        .stButton > button {
            background: linear-gradient(135deg, rgba(30, 41, 59, 0.8) 0%, rgba(15, 23, 42, 0.9) 100%) !important;
            color: var(--text-primary) !important;
            border: 1px solid rgba(255, 255, 255, 0.12) !important;
            border-radius: 12px !important;
            padding: 8px 16px !important;
            font-weight: 600 !important;
            letter-spacing: 0.01em !important;
            transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1) !important;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3) !important;
        }
        .stButton > button:hover {
            background: linear-gradient(135deg, #38BDF8 0%, #8B5CF6 100%) !important;
            color: #FFFFFF !important;
            border-color: transparent !important;
            transform: translateY(-2px) scale(1.01) !important;
            box-shadow: 0 8px 20px rgba(56, 189, 248, 0.35) !important;
        }

        /* 7. Metric Cards */
        [data-testid="stMetric"] {
            background: rgba(15, 23, 42, 0.6) !important;
            backdrop-filter: blur(16px) !important;
            border: 1px solid rgba(255, 255, 255, 0.08) !important;
            border-radius: 16px !important;
            padding: 16px 20px !important;
            box-shadow: 0 8px 24px rgba(0, 0, 0, 0.4) !important;
            transition: transform 0.2s ease !important;
        }
        [data-testid="stMetric"]:hover {
            transform: translateY(-2px) !important;
            border-color: rgba(56, 189, 248, 0.3) !important;
        }
        [data-testid="stMetricValue"] {
            color: var(--accent-cyan) !important;
            font-weight: 700 !important;
            font-family: 'JetBrains Mono', monospace !important;
        }

        /* 8. Expanders */
        div[data-testid="stExpander"] {
            background: rgba(15, 23, 42, 0.5) !important;
            backdrop-filter: blur(14px) !important;
            border: 1px solid rgba(255, 255, 255, 0.08) !important;
            border-radius: 14px !important;
            box-shadow: 0 4px 16px rgba(0, 0, 0, 0.3) !important;
        }

        /* 9. Code Blocks */
        code, pre {
            background: #0B0F19 !important;
            color: #38BDF8 !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
            border-radius: 10px !important;
            font-family: 'JetBrains Mono', monospace !important;
        }

        /* 10. Badges */
        .nova-badge {
            display: inline-flex;
            align-items: center;
            padding: 4px 10px;
            border-radius: 20px;
            font-size: 11px;
            font-weight: 600;
            background: rgba(56, 189, 248, 0.15);
            color: #38BDF8;
            border: 1px solid rgba(56, 189, 248, 0.3);
            letter-spacing: 0.03em;
        }
    </style>
    """
    st.markdown(theme_css, unsafe_allow_html=True)
