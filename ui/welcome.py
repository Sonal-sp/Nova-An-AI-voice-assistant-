import streamlit as st


def show_welcome():
    """
    Renders Nova's AI Operating System Hero Banner & Quick Action Cards.
    Displays when conversation history is empty.
    """
    if not st.session_state.messages:
        hero_html = """
        <div style="
            background: linear-gradient(135deg, rgba(15, 23, 42, 0.7) 0%, rgba(30, 41, 59, 0.4) 100%);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            border: 1px solid rgba(56, 189, 248, 0.2);
            border-radius: 20px;
            padding: 28px;
            margin-bottom: 24px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5), 0 0 20px rgba(56, 189, 248, 0.1);
        ">
            <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 16px;">
                <div style="display: flex; align-items: center; gap: 12px;">
                    <div style="
                        width: 48px; height: 48px; border-radius: 14px;
                        background: linear-gradient(135deg, #38BDF8 0%, #8B5CF6 100%);
                        display: flex; align-items: center; justify-content: center;
                        font-size: 24px; box-shadow: 0 0 15px rgba(56, 189, 248, 0.4);
                    ">🤖</div>
                    <div>
                        <h2 style="margin: 0; font-size: 22px; font-weight: 700; background: linear-gradient(135deg, #F8FAFC 0%, #38BDF8 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">Nova AI Operating System</h2>
                        <span style="font-size: 13px; color: #94A3B8;">Multi-Modal Desktop & Cloud Intelligence Engine v2.5</span>
                    </div>
                </div>
                <span class="nova-badge">⚡ System Operational</span>
            </div>
            
            <p style="color: #CBD5E1; font-size: 14px; line-height: 1.6; margin-bottom: 20px;">
                Ready for continuous hands-free voice interaction, multi-document FAISS RAG analysis, visual diagram breakdown, and desktop system controls.
            </p>
            
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 12px;">
                <div style="background: rgba(30, 41, 59, 0.5); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 12px; padding: 12px 14px;">
                    <div style="font-weight: 600; color: #38BDF8; font-size: 13px; margin-bottom: 4px;">🎙️ Voice Mode</div>
                    <div style="font-size: 12px; color: #94A3B8;">Say "Hey Nova open Spotify" or click microphone.</div>
                </div>
                <div style="background: rgba(30, 41, 59, 0.5); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 12px; padding: 12px 14px;">
                    <div style="font-weight: 600; color: #A855F7; font-size: 13px; margin-bottom: 4px;">📄 Hybrid RAG</div>
                    <div style="font-size: 12px; color: #94A3B8;">Upload PDFs in sidebar for FAISS + BM25 search.</div>
                </div>
                <div style="background: rgba(30, 41, 59, 0.5); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 12px; padding: 12px 14px;">
                    <div style="font-weight: 600; color: #EC4899; font-size: 13px; margin-bottom: 4px;">👁️ Vision AI & OCR</div>
                    <div style="font-size: 12px; color: #94A3B8;">Analyze diagrams, UI mockups, and text images.</div>
                </div>
                <div style="background: rgba(30, 41, 59, 0.5); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 12px; padding: 12px 14px;">
                    <div style="font-weight: 600; color: #22D3EE; font-size: 13px; margin-bottom: 4px;">🖥️ System Launcher</div>
                    <div style="font-size: 12px; color: #94A3B8;">Launch VS Code, Chrome, or run diagnostics.</div>
                </div>
            </div>
        </div>
        """
        st.markdown(hero_html, unsafe_allow_html=True)