import streamlit as st
import time

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="Routine X — Breathe", layout="centered")

# ---------------- SESSION STATE ----------------
defaults = {
    "screen": "home",
    "mode": None,
    "duration": 60,
    "phase_index": 0,
    "seconds_left": 0,
    "session_start": None,
    "running": False,
    "user_mood": None
}

for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ---------------- BREATHING MODES ----------------
BREATHING_MODES = {
    "Box Breathing": {
        "emoji": "🌿",
        "title": "Balanced Calm",
        "short": "Steady breathing to regain control and focus.",
        "detail": "A simple rhythm that balances your breath and settles your mind."
    },
    "4-7-8 Relax": {
        "emoji": "🌊",
        "title": "Deep Relaxation",
        "short": "Slows your body and eases anxiety.",
        "detail": "A deeper breathing pattern that relaxes your nervous system."
    },
    "Quick Reset": {
        "emoji": "⚡",
        "title": "Quick Clarity",
        "short": "Fast tension relief in under a minute.",
        "detail": "A short breathing exercise for instant calm."
    },
    "Calm Night": {
        "emoji": "🌙",
        "title": "Sleep Wind-Down",
        "short": "Gentle breathing to prepare for rest.",
        "detail": "Slow breathing to help your body relax for sleep."
    }
}

# ---------------- MOOD → MODE SUGGESTION ----------------
def suggest_mode(mood):
    # UPDATED: Now uses the full keys from BREATHING_MODES
    mapping = {
        "Stressed": "Box Breathing",
        "Anxious": "4-7-8 Relax",
        "Overwhelmed": "4-7-8 Relax",
        "Tired": "Calm Night",
        "Sleepy": "Calm Night",
        "Busy": "Quick Reset"
    }
    return mapping.get(mood, "Box Breathing")

# ---------------- BREATHING PATTERNS ----------------
def get_pattern(mode):
    # UPDATED: Checks for the full names used in BREATHING_MODES
    if mode == "Box Breathing":
        return [("Inhale", 4), ("Hold", 4), ("Exhale", 4), ("Hold", 4)]
    if mode == "4-7-8 Relax":
        return [("Inhale", 4), ("Hold", 7), ("Exhale", 8)]
    if mode == "Quick Reset":
        return [("Inhale", 3), ("Exhale", 5)]
    # Default for "Calm Night" or others
    return [("Inhale", 4), ("Exhale", 6)]

# ---------------- PREMIUM CSS ----------------
st.markdown("""
<style>
.stApp {background: linear-gradient(180deg,#0f172a,#1e1b4b); color:white;}
.title {text-align:center;font-size:40px;font-weight:600;}
.subtitle {text-align:center;color:#cbd5e1;}
.mode-card {
    padding:18px;border-radius:16px;background:rgba(255,255,255,0.05);
    border:1px solid rgba(255,255,255,0.1);margin-bottom:10px;
}
.orb {
    width:200px;height:200px;margin:auto;border-radius:50%;
    background: radial-gradient(circle, rgba(167,139,250,0.9), rgba(99,102,241,0.3));
    animation: breathe 8s infinite ease-in-out;
}
@keyframes breathe {
    0%{transform:scale(0.8);}50%{transform:scale(1.2);}100%{transform:scale(0.8);}
}
</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.markdown('<div class="title">Breathe</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Slow down. You\'re safe here.</div>', unsafe_allow_html=True)
st.write("")

# =====================================================
# HOME SCREEN
# =====================================================
if st.session_state.screen == "home":

    st.markdown('<div class="orb"></div>', unsafe_allow_html=True)
    st.write("")

    # ---------- Mood Check (for suggestion) ----------
    st.subheader("How are you feeling today?")
    mood = st.selectbox(
        "",
        ["Select mood", "Stressed", "Anxious", "Overwhelmed", "Tired", "Sleepy", "Busy"]
    )

    if mood != "Select mood":
        st.session_state.user_mood = mood
        suggested = suggest_mode(mood)

        st.success(
            f"✨ Recommended for you → "
            f"{BREATHING_MODES[suggested]['emoji']} "
            f"{BREATHING_MODES[suggested]['title']}"
        )

        if st.button("Start Recommended"):
            st.session_state.mode = suggested
            st.session_state.screen = "mode"
            st.rerun()

    st.write("---")
    st.subheader("Or choose your own")

    # ---------- Mode Cards ----------
    for key, value in BREATHING_MODES.items():

        st.markdown(f"""
        <div class="mode-card">
        <h4>{value['emoji']} {key}</h4>
        <b>{value['title']}</b>
        <p>{value['short']}</p>
        </div>
        """, unsafe_allow_html=True)

        if st.button(f"Start {key}", key=f"btn_{key}"):
            st.session_state.mode = key
            st.session_state.screen = "mode"
            st.rerun()

# =====================================================
# MODE DETAIL SCREEN
# =====================================================
elif st.session_state.screen == "mode":

    mode = st.session_state.mode
    info = BREATHING_MODES[mode]

    st.subheader(f"{info['emoji']} {mode}")
    st.write(info["detail"])

    st.session_state.duration = st.selectbox(
        "Session Duration",
        [60, 180, 300],
        format_func=lambda x: f"{x//60} min"
    )

    if st.button("Begin Session"):
        pattern = get_pattern(mode)
        st.session_state.screen = "session"
        st.session_state.running = True
        st.session_state.session_start = time.time()
        st.session_state.phase_index = 0
        st.session_state.seconds_left = pattern[0][1]
        st.rerun()

    if st.button("⬅ Back"):
        st.session_state.screen = "home"
        st.rerun()

# =====================================================
# ACTIVE SESSION
# =====================================================
elif st.session_state.screen == "session":

    st.markdown('<div class="orb"></div>', unsafe_allow_html=True)

    pattern = get_pattern(st.session_state.mode)
    phase_name, _ = pattern[st.session_state.phase_index]

    st.subheader(phase_name)
    st.write(f"Mode: {st.session_state.mode}")

    col1, col2 = st.columns(2)

    with col1:
        if st.session_state.running:
            if st.button("Pause"):
                st.session_state.running = False
                st.rerun()
        else:
            if st.button("Resume"):
                st.session_state.running = True
                st.rerun()

    with col2:
        if st.button("Exit Session"):
            st.session_state.screen = "home"
            st.session_state.running = False
            st.rerun()

    # ---------- Breathing cycle ----------
    if st.session_state.running:

        time.sleep(1)
        st.session_state.seconds_left -= 1

        if st.session_state.seconds_left <= 0:
            st.session_state.phase_index = (
                st.session_state.phase_index + 1
            ) % len(pattern)
            st.session_state.seconds_left = pattern[
                st.session_state.phase_index
            ][1]

        if time.time() - st.session_state.session_start >= st.session_state.duration:
            st.session_state.screen = "complete"

        st.rerun()

# =====================================================
# COMPLETION
# =====================================================
elif st.session_state.screen == "complete":

    st.success("That was a good pause.")
    st.write("How do you feel now?")

    st.radio(
        "",
        ["🙂 Better", "😌 Calm", "😐 Same", "😔 Still stressed", "😴 Sleepy"]
    )

    if st.button("Done"):
        st.session_state.screen = "home"
        st.rerun()