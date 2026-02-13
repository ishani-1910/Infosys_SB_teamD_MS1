import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

def show_daily_checkin():
    # --- DATA INIT ---
    if 'history' not in st.session_state: st.session_state.history = []
    if 'selected_mood' not in st.session_state: st.session_state.selected_mood = None

    # --- STYLE INJECTION (GRADIENT BACKGROUND) ---
    st.markdown("""
        <style>
        [data-testid="stAppViewContainer"] {
            background: linear-gradient(135deg, #a78bfa 0%, #f472b6 50%, #fbbf24 100%);
            background-attachment: fixed;
        }
        h1, h2, h3, p, span { color: white !important; }
        .main-card {
            background-color: rgba(255, 255, 255, 0.95);
            border-radius: 30px;
            padding: 40px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.2);
            color: #333 !important;
        }
        .main-card h1, .main-card h2, .main-card p, .main-card span { color: #333 !important; }
        .mood-box {
            background: white;
            border: 2px solid #f0f0f0;
            border-radius: 15px;
            padding: 15px;
            text-align: center;
            cursor: pointer;
        }
        .mood-box:hover { transform: translateY(-5px); border-color: #a78bfa; }
        .mood-box-selected {
            border-color: #6366f1 !important;
            background-color: #f5f3ff !important;
            transform: translateY(-5px);
        }
        </style>
    """, unsafe_allow_html=True)

    # --- PAGE CONTENT ---
    st.markdown("<h1>💜 Routine X</h1>", unsafe_allow_html=True)
    st.markdown("<p>Welcome back to your safe space.</p>", unsafe_allow_html=True)

    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    st.markdown("### 💜 Daily Mental Check-in")
    st.divider()

    mood_map = {
        "Terrible": {"val": 1, "emoji": "😫", "color": "#ef4444"},
        "Bad":      {"val": 2, "emoji": "☹️", "color": "#fb923c"},
        "Meh":      {"val": 3, "emoji": "😐", "color": "#fbbf24"},
        "Good":     {"val": 4, "emoji": "🙂", "color": "#60a5fa"},
        "Awesome":  {"val": 5, "emoji": "😊", "color": "#34d399"},
    }

    cols = st.columns(5)
    for i, (label, data) in enumerate(mood_map.items()):
        with cols[i]:
            sel = st.session_state.selected_mood == label
            css = "mood-box-selected" if sel else "mood-box"
            st.markdown(f"""
                <div class="{css}">
                    <div style="background:{data['color']};color:white;padding:2px 8px;border-radius:4px;font-size:10px;display:inline-block;">{label}</div>
                    <div style="font-size:35px;margin-top:5px;">{data['emoji']}</div>
                </div>
            """, unsafe_allow_html=True)
            if st.button(f"Select {label}", key=f"btn_{label}", use_container_width=True):
                st.session_state.selected_mood = label
                st.rerun()

    st.write("")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("**Small Wins?**")
        st.checkbox("Drank Water")
        st.checkbox("Walked")
        st.checkbox("Meditated")
    with c2:
        st.markdown("**Notes**")
        st.text_area("Reflect...", label_visibility="collapsed")
        if st.button("COMPLETE CHECK-IN", type="primary", use_container_width=True):
            if st.session_state.selected_mood:
                st.session_state.history.append({
                    "Time": datetime.now().strftime("%H:%M"),
                    "Mood Score": mood_map[st.session_state.selected_mood]["val"],
                    "Mood Label": st.session_state.selected_mood
                })
                st.success("Saved!")
            else:
                st.warning("Select a mood first.")

    if st.session_state.history:
        st.divider()
        df = pd.DataFrame(st.session_state.history)
        fig = px.line(df, x="Time", y="Mood Score", text="Mood Label", markers=True)
        fig.update_layout(yaxis=dict(range=[0,6]), height=300)
        st.plotly_chart(fig, use_container_width=True)

    st.markdown('</div>', unsafe_allow_html=True)