import streamlit as st
import pandas as pd

from utils.settings import load_settings, save_settings, update_setting
from services.system_diagnostics_service import get_full_system_health


def render_settings_dashboard():
    """
    Renders interactive Streamlit System Health Monitor and Assistant Settings Dashboard.
    """
    st.markdown("## ⚙️ Settings & System Health")
    st.caption("Monitor real-time system hardware performance and customize Nova AI preferences live.")

    tab_health, tab_config = st.tabs(["📊 System Health Monitor", "⚙️ Assistant Preferences"])

    # ==========================================================
    # 1. System Health Dashboard Tab
    # ==========================================================
    with tab_health:
        st.subheader("📊 Hardware Performance Monitor")
        health = get_full_system_health()

        # Gauge metrics row
        m1, m2, m3, m4 = st.columns(4)
        with m1:
            st.metric("💻 CPU Usage", f"{health['cpu']['percent']}%")
            st.progress(health['cpu']['percent'] / 100.0)
        with m2:
            st.metric("🧠 RAM Usage", f"{health['memory']['percent']}%", f"{health['memory']['used_gb']} / {health['memory']['total_gb']} GB")
            st.progress(health['memory']['percent'] / 100.0)
        with m3:
            st.metric("💾 Disk Usage", f"{health['storage']['percent']}%", f"{health['storage']['used_gb']} / {health['storage']['total_gb']} GB")
            st.progress(health['storage']['percent'] / 100.0)
        with m4:
            st.metric("⚡ Active Processes", f"{len(health['top_processes'])} top procs")

        st.divider()

        # Top Processes Inspector Table
        st.subheader("🔍 Top Process Memory Inspector")
        if health["top_processes"]:
            df_proc = pd.DataFrame(health["top_processes"])
            df_proc.columns = ["PID", "Process Name", "CPU (%)", "Memory (%)"]
            st.dataframe(df_proc, use_container_width=True, hide_index=True)
        else:
            st.info("No active process metrics available.")

        # System Hardware Specs Expander
        with st.expander("ℹ️ Detailed System Hardware & OS Info", expanded=False):
            info = health["system_info"]
            st.markdown(
                f"""
- **OS Platform:** `{info['os_name']} {info['os_release']}` ({info['architecture']})
- **Python Version:** `{info['python_version']}`
- **Host Name:** `{info['hostname']}`
- **Local IP Address:** `{info['local_ip']}`
- **CPU Cores:** `{health['cpu']['physical_cores']} Physical / {health['cpu']['logical_cores']} Logical`
- **CPU Frequency:** `{health['cpu']['freq_mhz']} MHz`
"""
            )

    # ==========================================================
    # 2. Assistant Preferences Tab (Instant Live Controls)
    # ==========================================================
    with tab_config:
        st.subheader("⚙️ Customizable Settings (Live Auto-Save)")
        curr = load_settings()

        st.markdown("### 🔊 Voice Engine Settings")
        col_v1, col_v2 = st.columns(2)
        with col_v1:
            v_speed = st.slider(
                "Voice Speed",
                min_value=0.5,
                max_value=2.0,
                value=float(curr.get("voice_speed", 1.0)),
                step=0.1,
                key="pref_voice_speed",
            )
            v_volume = st.slider(
                "Voice Volume",
                min_value=0.0,
                max_value=1.0,
                value=float(curr.get("voice_volume", 1.0)),
                step=0.05,
                key="pref_voice_volume",
            )
        with col_v2:
            v_gender = st.radio(
                "Voice Gender / Persona",
                ["Female", "Male"],
                index=0 if curr.get("voice_gender") == "Female" else 1,
                key="pref_voice_gender",
            )

        st.divider()
        st.markdown("### 🧠 Advanced RAG & Search Settings")
        col_r1, col_r2 = st.columns(2)
        with col_r1:
            rag_k = st.slider(
                "RAG Candidate Chunks (Top-K)",
                min_value=1,
                max_value=10,
                value=int(curr.get("rag_top_k", 4)),
                key="pref_rag_top_k",
            )
            min_conf = st.slider(
                "Minimum Confidence Threshold (%)",
                min_value=0,
                max_value=100,
                value=int(curr.get("min_confidence_threshold", 50)),
                key="pref_min_conf",
            )
        with col_r2:
            rerank_enable = st.toggle(
                "Enable Cross-Encoder Re-ranker",
                value=bool(curr.get("cross_encoder_enabled", True)),
                key="pref_rerank_enable",
            )

        st.divider()
        st.markdown("### 🤖 LLM Synthesis Preferences")
        col_l1, col_l2 = st.columns(2)
        with col_l1:
            model_opts = ["gemini-2.5-flash", "gemini-2.0-flash"]
            curr_mod = curr.get("default_model", "gemini-2.5-flash")
            mod_idx = model_opts.index(curr_mod) if curr_mod in model_opts else 0
            model_sel = st.selectbox(
                "Default LLM Model",
                model_opts,
                index=mod_idx,
                key="pref_model_sel",
            )
        with col_l2:
            temp_val = st.slider(
                "LLM Temperature (Creativity)",
                min_value=0.0,
                max_value=1.0,
                value=float(curr.get("temperature", 0.7)),
                step=0.05,
                key="pref_temp_val",
            )

        st.divider()
        st.markdown("### 🎨 System Preferences")
        col_s1, col_s2 = st.columns(2)
        with col_s1:
            theme_opts = ["Nova Cyberpunk", "Obsidian Dark"]
            curr_th = curr.get("theme", "Nova Cyberpunk")
            th_idx = theme_opts.index(curr_th) if curr_th in theme_opts else 0
            theme_val = st.selectbox(
                "UI Theme Palette",
                theme_opts,
                index=th_idx,
                key="pref_theme_val",
            )
        with col_s2:
            auto_save = st.toggle(
                "Auto-save Chat History",
                value=bool(curr.get("auto_save_chat", True)),
                key="pref_auto_save",
            )

        # Auto-save updated settings on every render pass
        new_settings = {
            "voice_speed": v_speed,
            "voice_volume": v_volume,
            "voice_gender": v_gender,
            "rag_top_k": rag_k,
            "min_confidence_threshold": min_conf,
            "cross_encoder_enabled": rerank_enable,
            "default_model": model_sel,
            "temperature": temp_val,
            "theme": theme_val,
            "auto_save_chat": auto_save,
        }

        # Check if settings changed from disk
        if new_settings != curr:
            save_settings(new_settings)
            st.toast("⚡ Settings updated and saved!", icon="💾")

        if st.button("💾 Force Save & Apply All Preferences", use_container_width=True):
            save_settings(new_settings)
            st.toast("✅ All preferences saved to disk!", icon="💾")
            st.rerun()
