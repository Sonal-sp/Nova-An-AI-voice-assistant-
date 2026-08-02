import streamlit as st


def render_audio_visualizer(state: str = "listening", label: str = ""):
    """
    Renders an interactive animated CSS soundwave visualizer widget in Streamlit.

    Parameters
    ----------
    state : str
        Current audio state ('listening', 'thinking', 'speaking', 'idle').
    label : str
        Optional status label string.
    """
    colors = {
        "listening": "#00F0FF",
        "thinking": "#F59E0B",
        "speaking": "#10B981",
        "idle": "#6B7280",
    }
    bar_color = colors.get(state, "#00F0FF")
    status_text = label if label else f"🎤 Voice Engine: {state.capitalize()}"

    visualizer_html = f"""
    <div style="
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        padding: 15px;
        background: rgba(15, 23, 42, 0.6);
        border: 1px solid {bar_color};
        border-radius: 12px;
        margin: 10px 0;
        box-shadow: 0 0 15px {bar_color}44;
    ">
        <div style="
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 6px;
            height: 40px;
        ">
            <div class="bar bar1" style="width: 5px; height: 15px; background-color: {bar_color}; border-radius: 3px; animation: soundwave 1.2s infinite ease-in-out;"></div>
            <div class="bar bar2" style="width: 5px; height: 30px; background-color: {bar_color}; border-radius: 3px; animation: soundwave 0.8s infinite ease-in-out 0.2s;"></div>
            <div class="bar bar3" style="width: 5px; height: 20px; background-color: {bar_color}; border-radius: 3px; animation: soundwave 1.0s infinite ease-in-out 0.4s;"></div>
            <div class="bar bar4" style="width: 5px; height: 35px; background-color: {bar_color}; border-radius: 3px; animation: soundwave 0.7s infinite ease-in-out 0.1s;"></div>
            <div class="bar bar5" style="width: 5px; height: 18px; background-color: {bar_color}; border-radius: 3px; animation: soundwave 1.1s infinite ease-in-out 0.3s;"></div>
        </div>
        <div style="color: {bar_color}; font-size: 0.85rem; font-weight: 600; margin-top: 8px;">
            {status_text}
        </div>
    </div>

    <style>
    @keyframes soundwave {{
        0%, 100% {{ transform: scaleY(0.4); opacity: 0.6; }}
        50% {{ transform: scaleY(1.3); opacity: 1.0; }}
    }}
    </style>
    """

    st.markdown(visualizer_html, unsafe_allow_html=True)
