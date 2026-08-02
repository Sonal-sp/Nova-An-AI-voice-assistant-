import streamlit as st


def render_audio_visualizer(state: str = "listening", label: str = ""):
    """
    Renders an interactive animated CSS audio spectrum visualizer widget in Streamlit.

    Parameters
    ----------
    state : str
        Current audio state ('listening', 'thinking', 'speaking', 'idle').
    label : str
        Optional status label string.
    """
    colors = {
        "listening": "#38BDF8",
        "thinking": "#A855F7",
        "speaking": "#10B981",
        "idle": "#64748B",
    }
    bar_color = colors.get(state, "#38BDF8")
    status_text = label if label else f"🎤 Voice Engine Active: {state.capitalize()}"

    visualizer_html = f"""
    <div style="
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        padding: 20px;
        background: radial-gradient(circle at 50% 50%, rgba(15, 23, 42, 0.9) 0%, rgba(7, 9, 14, 0.95) 100%);
        border: 1px solid {bar_color}66;
        border-radius: 18px;
        margin: 12px 0;
        box-shadow: 0 0 25px {bar_color}33, inset 0 0 15px {bar_color}22;
        backdrop-filter: blur(16px);
    ">
        <div style="
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 8px;
            height: 50px;
        ">
            <div class="bar bar1" style="width: 6px; height: 20px; background: linear-gradient(180deg, {bar_color} 0%, #EC4899 100%); border-radius: 4px; animation: soundwave 1.2s infinite ease-in-out;"></div>
            <div class="bar bar2" style="width: 6px; height: 40px; background: linear-gradient(180deg, {bar_color} 0%, #A855F7 100%); border-radius: 4px; animation: soundwave 0.8s infinite ease-in-out 0.2s;"></div>
            <div class="bar bar3" style="width: 6px; height: 25px; background: linear-gradient(180deg, {bar_color} 0%, #22D3EE 100%); border-radius: 4px; animation: soundwave 1.0s infinite ease-in-out 0.4s;"></div>
            <div class="bar bar4" style="width: 6px; height: 45px; background: linear-gradient(180deg, {bar_color} 0%, #EC4899 100%); border-radius: 4px; animation: soundwave 0.7s infinite ease-in-out 0.1s;"></div>
            <div class="bar bar5" style="width: 6px; height: 22px; background: linear-gradient(180deg, {bar_color} 0%, #38BDF8 100%); border-radius: 4px; animation: soundwave 1.1s infinite ease-in-out 0.3s;"></div>
            <div class="bar bar6" style="width: 6px; height: 35px; background: linear-gradient(180deg, {bar_color} 0%, #A855F7 100%); border-radius: 4px; animation: soundwave 0.9s infinite ease-in-out 0.15s;"></div>
        </div>
        <div style="color: {bar_color}; font-size: 13px; font-weight: 700; margin-top: 12px; letter-spacing: 0.04em; text-transform: uppercase; font-family: monospace;">
            {status_text}
        </div>
    </div>

    <style>
    @keyframes soundwave {{
        0%, 100% {{ transform: scaleY(0.3); opacity: 0.5; box-shadow: 0 0 5px {bar_color}44; }}
        50% {{ transform: scaleY(1.4); opacity: 1.0; box-shadow: 0 0 15px {bar_color}aa; }}
    }}
    </style>
    """

    st.markdown(visualizer_html, unsafe_allow_html=True)
