"""
smart_checkin.py
RoutineX Smart Daily Assistant — full daily diary, weight tracker,
weekly review with AI insights, progress charts, to-do list.
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from datetime import datetime, date, timedelta
import json
import os

from database_tracker import (
    init_tracker_db,
    # goals
    save_goal, get_active_goal,
    # diary
    upsert_diary, get_diary_entry, get_diary_last_n, get_diary_range,
    # weight
    log_weight, get_weight_history, get_latest_weight,
    # weekly
    save_weekly_review, get_weekly_reviews, get_latest_weekly_review, get_weekly_stats,
    # workout plans
    get_active_workout_plan,
    # diet plans
    get_active_diet_plan,
    # todos
    add_todo, get_todos, toggle_todo, delete_todo,
    # wins
    save_wins, get_wins,
    # streak
    get_streak,
)


# ─────────────────────────────────────────────────────────────
# CONSTANTS
# ─────────────────────────────────────────────────────────────

MOOD_MAP = {
    1: ("😫", "Terrible", "#ef4444"),
    2: ("😕", "Bad",      "#f97316"),
    3: ("😐", "Meh",      "#eab308"),
    4: ("🙂", "Good",     "#22c55e"),
    5: ("😁", "Amazing",  "#6366f1"),
}

DAYS = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]


# ─────────────────────────────────────────────────────────────
# CSS
# ─────────────────────────────────────────────────────────────

CHECKIN_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=Syne:wght@700;800&display=swap');

/* ── ROOT ───────────────────────────────── */
.stApp {
    background: #0d0d1a !important;
    font-family: 'Plus Jakarta Sans', sans-serif;
}
.main .block-container {
    background: transparent !important;
    padding: 1.5rem 2rem !important;
    max-width: 1200px;
}

/* ── ALL TEXT ───────────────────────────── */
.stMarkdown, .stMarkdown p, .stMarkdown li,
.stMarkdown h1, .stMarkdown h2, .stMarkdown h3,
.stMarkdown h4, .stMarkdown span, .stText,
div[data-testid="stText"], .stCaption p {
    color: #e2e2f0 !important;
}
label, .stNumberInput label, .stSelectbox label,
.stSlider label, .stTextArea label, .stTextInput label,
.stCheckbox label, .stRadio label {
    color: #a0a0c0 !important;
    font-size: 12px !important;
    font-weight: 600 !important;
    text-transform: uppercase;
    letter-spacing: 0.8px;
}
div[role="radiogroup"] p, div[role="radiogroup"] label { color:#e2e2f0 !important; }

/* ── INPUTS ─────────────────────────────── */
.stNumberInput input,
.stSelectbox div[data-baseweb="select"],
div[data-baseweb="input"] > input,
.stTextArea textarea,
.stTextInput input {
    background: rgba(255,255,255,0.05) !important;
    border: 1px solid rgba(255,255,255,0.12) !important;
    color: #e2e2f0 !important;
    border-radius: 10px !important;
}
ul[data-baseweb="menu"] li { background:#1a1a2e !important; color:#e2e2f0 !important; }

/* ── CHECKBOXES ─────────────────────────── */
[data-testid="stCheckbox"] { padding: 8px 0 !important; }

/* ── BUTTONS ────────────────────────────── */
div.stButton > button[kind="secondary"] {
    background: rgba(255,255,255,0.06) !important;
    border: 1px solid rgba(255,255,255,0.15) !important;
    color: #a0a0c0 !important;
    border-radius: 8px !important;
    font-size: 12px !important;
    padding: 6px 14px !important;
}
div.stButton > button[kind="secondary"]:hover {
    border-color:#6366f1 !important; color:#fff !important;
}
div.stButton > button[kind="primary"],
div[data-testid="stFormSubmitButton"] > button {
    background: linear-gradient(135deg,#6366f1,#8b5cf6) !important;
    color:#fff !important;
    border:none !important;
    border-radius:10px !important;
    font-family:'Syne',sans-serif !important;
    font-weight:700 !important;
    font-size:15px !important;
    letter-spacing:0.5px;
    padding:12px 24px !important;
    box-shadow: 0 4px 20px rgba(99,102,241,0.4) !important;
    transition: all 0.2s !important;
}
div.stButton > button[kind="primary"]:hover,
div[data-testid="stFormSubmitButton"] > button:hover {
    box-shadow: 0 8px 30px rgba(99,102,241,0.6) !important;
    transform: translateY(-1px);
}

/* ── TABS ───────────────────────────────── */
button[data-baseweb="tab"] {
    color: #555577 !important;
    font-family:'Plus Jakarta Sans',sans-serif !important;
    font-weight:600 !important;
    font-size:14px !important;
    background:transparent !important; border:none !important;
}
button[data-baseweb="tab"][aria-selected="true"] {
    color:#a5b4fc !important;
    border-bottom: 3px solid #6366f1 !important;
}

/* ── EXPANDERS ──────────────────────────── */
div[data-testid="stExpander"] {
    background:rgba(255,255,255,0.03) !important;
    border:1px solid rgba(255,255,255,0.08) !important;
    border-radius:12px !important; margin-bottom:8px;
}
div[data-testid="stExpander"] details summary p {
    color:#c4c4e0 !important; font-weight:600 !important;
}

/* ── ALERTS ─────────────────────────────── */
.stAlert,[data-testid="stAlert"] {
    background:rgba(99,102,241,0.12) !important;
    border:1px solid rgba(99,102,241,0.3) !important;
    border-radius:10px !important; color:#e2e2f0 !important;
}
.stAlert p,.stAlert div { color:#e2e2f0 !important; }
.stSuccess,.stSuccess p { background:rgba(34,197,94,0.15) !important; color:#fff !important; border-radius:8px !important; }
.stError,.stError p { background:rgba(239,68,68,0.15) !important; color:#fff !important; }
.stWarning,.stWarning p { background:rgba(234,179,8,0.15) !important; color:#fff !important; }

/* ── SLIDER ─────────────────────────────── */
.stSlider p { color:#a0a0c0 !important; }

/* ── CARDS ───────────────────────────────── */
.dash-card {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 16px;
    padding: 20px 22px;
    margin-bottom: 16px;
}
.dash-card-accent {
    background: linear-gradient(135deg, rgba(99,102,241,0.12), rgba(139,92,246,0.08));
    border: 1px solid rgba(99,102,241,0.25);
    border-radius: 16px;
    padding: 20px 22px;
    margin-bottom: 16px;
}
.metric-card {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 14px;
    padding: 18px 16px;
    text-align: center;
}
.metric-value {
    font-family:'Syne',sans-serif;
    font-size: 32px;
    font-weight: 800;
    color: #a5b4fc;
    line-height: 1;
    margin-bottom: 4px;
}
.metric-label {
    font-size: 11px;
    color: #6b6b8d;
    text-transform: uppercase;
    letter-spacing: 1px;
    font-weight: 600;
}

/* ── PAGE HEADER ────────────────────────── */
.page-title {
    font-family:'Syne',sans-serif;
    font-size:40px; font-weight:800;
    background:linear-gradient(90deg,#a5b4fc,#c4b5fd,#f0abfc);
    -webkit-background-clip:text; -webkit-text-fill-color:transparent;
    background-clip:text; line-height:1.1; margin-bottom:4px;
}
.page-sub {
    font-size:14px; color:#555577; margin-bottom:28px;
}

/* ── SECTION LABEL ──────────────────────── */
.sec-label {
    display:inline-block;
    font-size:10px; font-weight:700; text-transform:uppercase;
    letter-spacing:2px; padding:3px 12px; border-radius:20px;
    background:rgba(99,102,241,0.2); color:#a5b4fc;
    border:1px solid rgba(99,102,241,0.4); margin-bottom:14px;
}

/* ── WORKOUT DAY CARD ───────────────────── */
.workout-day {
    background:rgba(99,102,241,0.07);
    border-left:3px solid #6366f1;
    padding:10px 14px; border-radius:0 10px 10px 0;
    margin-bottom:8px;
}
.workout-day-name { font-weight:700; color:#a5b4fc; font-size:14px; margin-bottom:4px; }
.exercise-item { color:#c4c4e0; font-size:13px; padding:2px 0; }

/* ── TODO ITEM ──────────────────────────── */
.todo-done { text-decoration:line-through; color:#444466 !important; }

/* ── MOOD BUTTON ROW ────────────────────── */
.mood-btn { cursor:pointer; text-align:center; transition:transform 0.15s; }
.mood-btn:hover { transform:scale(1.1); }

/* ── PROGRESS BAR ───────────────────────── */
.prog-bar-outer {
    background:rgba(255,255,255,0.06);
    border-radius:8px; height:10px; overflow:hidden; margin:6px 0;
}
.prog-bar-inner {
    height:100%; border-radius:8px;
    background:linear-gradient(90deg,#6366f1,#a855f7);
    transition:width 0.5s ease;
}

/* ── NAV OVERRIDE ───────────────────────── */
.brand { color:#FFFFFF !important; }
.tagline { color:#9999bb !important; }

hr { border-color:rgba(255,255,255,0.06) !important; }
</style>
"""


# ─────────────────────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────────────────────

def _today():
    return date.today().isoformat()


def _week_monday(d=None):
    d = d or date.today()
    return (d - timedelta(days=d.weekday())).isoformat()


def _make_gauge(value, max_val, title, color="#6366f1"):
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        domain={"x":[0,1],"y":[0,1]},
        title={"text":title,"font":{"color":"#a0a0c0","size":13}},
        gauge={
            "axis":{"range":[0,max_val],"tickcolor":"#444"},
            "bar":{"color":color},
            "bgcolor":"rgba(255,255,255,0.04)",
            "bordercolor":"rgba(255,255,255,0.08)",
            "steps":[{"range":[0,max_val],"color":"rgba(255,255,255,0.03)"}],
        },
        number={"font":{"color":"#e2e2f0","size":22}}
    ))
    fig.update_layout(
        height=160, margin=dict(t=30,b=0,l=10,r=10),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Plus Jakarta Sans")
    )
    return fig


def _dark_line(df, x, y, title, color="#818cf8", yrange=None):
    fig = px.line(df, x=x, y=y, title=title, markers=True,
                  color_discrete_sequence=[color])
    fig.update_traces(line_width=2.5, marker_size=7,
                      marker_color=color,
                      marker_line_color="rgba(0,0,0,0.5)",
                      marker_line_width=1.5)
    fig.update_layout(
        height=260, paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(255,255,255,0.02)",
        font=dict(family="Plus Jakarta Sans", color="#a0a0c0"),
        title_font_color="#c4c4e0",
        xaxis=dict(showgrid=False, zeroline=False, color="#555577"),
        yaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.05)",
                   zeroline=False, color="#555577",
                   range=yrange),
        margin=dict(t=40,b=20,l=10,r=10),
    )
    return fig


# ─────────────────────────────────────────────────────────────
# AI WEEKLY REVIEW GENERATOR
# ─────────────────────────────────────────────────────────────

def generate_ai_weekly_review(username, stats, goal, latest_weight, start_weight, target_weight, target_date_str):
    """Call Gemini to produce a short weekly summary + suggestion."""
    try:
        import google.generativeai as genai
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            return "Keep up the great work this week!", "Stay consistent with your plan."
        genai.configure(api_key=api_key)

        weight_delta = ""
        if latest_weight and start_weight:
            delta = latest_weight - start_weight
            weight_delta = f"Current weight: {latest_weight} kg (started at {start_weight} kg, delta: {delta:+.1f} kg)."

        goal_info = ""
        if goal:
            goal_info = (f"Goal: {goal.get('description','')}, "
                         f"Target weight: {goal.get('target_weight','N/A')} kg by {target_date_str}.")

        prompt = f"""
You are a supportive fitness coach reviewing a user's weekly data.
Be concise, warm, motivating. Use 2-3 sentences max per section.

WEEKLY DATA:
- Days logged: {stats.get('days_logged',0)}/7
- Avg Mood: {stats.get('avg_mood','N/A')}/5
- Avg Energy: {stats.get('avg_energy','N/A')}/5
- Avg Sleep: {stats.get('avg_sleep','N/A')} hrs
- Avg Water: {stats.get('avg_water','N/A')} glasses
- Workouts completed: {stats.get('workouts_completed',0)} days
- Diet followed: {stats.get('days_diet_followed',0)} days
{weight_delta}
{goal_info}

OUTPUT (JSON only, no markdown):
{{
  "summary": "2-3 sentence summary of the week",
  "suggestion": "1-2 specific actionable next-step recommendations",
  "on_track": true or false
}}
"""
        model = genai.GenerativeModel('gemini-2.5-flash')
        resp = model.generate_content(prompt)
        txt = resp.text.strip().strip("```json").strip("```").strip()
        data = json.loads(txt)
        return data.get("summary",""), data.get("suggestion",""), data.get("on_track",True)
    except Exception:
        return ("Great effort this week! Keep logging your progress.", "Stay consistent — every day counts.", True)


# ─────────────────────────────────────────────────────────────
# SUB-SECTIONS
# ─────────────────────────────────────────────────────────────

def render_today_diary(username):
    today = _today()
    today_fmt = date.today().strftime("%A, %B %d %Y")
    existing = get_diary_entry(username, today)

    st.markdown(f"""
    <div class='dash-card-accent'>
        <div style='font-family:Syne,sans-serif;font-size:13px;color:#6366f1;
                    text-transform:uppercase;letter-spacing:2px;margin-bottom:4px;'>Today's Entry</div>
        <div style='font-family:Syne,sans-serif;font-size:26px;font-weight:800;color:#e2e2f0;'>
            {today_fmt}
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── MOOD ROW ──
    st.markdown("<div class='sec-label'>😊 How are you feeling?</div>", unsafe_allow_html=True)
    mood_cols = st.columns(5)
    cur_mood = st.session_state.get("diary_mood", existing.get("mood") if existing else None)
    for i, (score, (emoji, label, color)) in enumerate(MOOD_MAP.items()):
        with mood_cols[i]:
            selected = cur_mood == score
            border = f"3px solid {color}" if selected else "1px solid rgba(255,255,255,0.1)"
            bg = f"rgba{tuple(int(color.lstrip('#')[j:j+2],16) for j in (0,2,4))}26".replace("(","rgba(").replace(",26)",",.15)") if selected else "rgba(255,255,255,0.03)"
            st.markdown(f"""
            <div style='text-align:center;padding:12px 6px;border-radius:14px;
                        border:{border};background:{bg};cursor:pointer;'>
                <div style='font-size:28px;'>{emoji}</div>
                <div style='font-size:11px;color:{color};font-weight:700;margin-top:4px;'>{label}</div>
            </div>""", unsafe_allow_html=True)
            if st.button(label, key=f"mood_{score}", use_container_width=True):
                st.session_state["diary_mood"] = score
                st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    # ── VITALS + ACTIVITIES ──
    v1, v2, v3, v4 = st.columns(4)
    with v1:
        sleep_h = st.number_input("😴 Sleep (hrs)", 0.0, 12.0,
                                   float(existing.get("sleep_hours") or 7.0) if existing else 7.0,
                                   step=0.5, key="diary_sleep")
    with v2:
        water_g = st.number_input("💧 Water (glasses)", 0, 20,
                                   int(existing.get("water_glasses") or 8) if existing else 8,
                                   key="diary_water")
    with v3:
        energy = st.slider("⚡ Energy Level", 1, 5,
                            int(existing.get("energy_level") or 3) if existing else 3,
                            key="diary_energy")
    with v4:
        stress = st.slider("😤 Stress Level", 1, 5,
                            int(existing.get("stress_level") or 3) if existing else 3,
                            key="diary_stress")

    c1, c2, c3 = st.columns(3)
    with c1:
        workout_done = st.checkbox("💪 Completed Workout",
                                    value=bool(existing.get("workout_done")) if existing else False,
                                    key="diary_workout_done")
    with c2:
        diet_followed = st.checkbox("🥗 Followed Diet Plan",
                                     value=bool(existing.get("diet_followed")) if existing else False,
                                     key="diary_diet")
    with c3:
        steps = st.number_input("👟 Steps (optional)", 0, 50000,
                                 int(existing.get("steps_count") or 0) if existing else 0,
                                 step=500, key="diary_steps")

    # ── JOURNAL ENTRY ──
    st.markdown("<div class='sec-label'>📝 Daily Journal</div>", unsafe_allow_html=True)
    journal = st.text_area(
        "Reflect on your day — thoughts, wins, struggles…",
        value=existing.get("journal_text","") if existing else "",
        height=120, key="diary_journal",
        placeholder="Today I felt… I'm proud that… Tomorrow I want to…"
    )

    # ── WORKOUT NOTES ──
    if workout_done:
        workout_notes = st.text_input("🏋️ Workout notes (optional)",
                                       value=existing.get("workout_notes","") if existing else "",
                                       key="diary_workout_notes")
    else:
        workout_notes = ""

    # ── SAVE ──
    if st.button("💾 SAVE TODAY'S ENTRY", type="primary", use_container_width=True):
        mood_val = st.session_state.get("diary_mood")
        if not mood_val:
            st.warning("Please select a mood before saving.")
        else:
            upsert_diary(
                username, today,
                mood=mood_val,
                mood_label=MOOD_MAP[mood_val][1],
                energy_level=energy,
                sleep_hours=sleep_h,
                water_glasses=water_g,
                workout_done=1 if workout_done else 0,
                workout_notes=workout_notes,
                diet_followed=1 if diet_followed else 0,
                journal_text=journal,
                stress_level=stress,
                steps_count=steps,
            )
            st.success("✅ Entry saved!")
            st.rerun()

    # ── ACTIVE PLANS PREVIEW ──
    st.markdown("---")
    st.markdown("<div class='sec-label'>📋 Your Active Plans</div>", unsafe_allow_html=True)

    wp = get_active_workout_plan(username)
    dp = get_active_diet_plan(username)

    pw, pd_ = st.columns(2)
    with pw:
        if wp:
            schedule = wp["plan_data"].get("schedule", [])
            # figure out which week
            plan_start = datetime.strptime(wp["created_at"][:10], "%Y-%m-%d").date()
            days_elapsed = (date.today() - plan_start).days
            week_idx = min(days_elapsed // 7, len(schedule) - 1)
            today_dow = date.today().weekday()  # 0=Mon

            if schedule and week_idx >= 0:
                current_week = schedule[week_idx]
                workouts_today = [d for d in current_week.get("workouts", [])
                                  if d.get("day","").lower()[:3] == date.today().strftime("%a").lower()]
                today_workout = workouts_today[0] if workouts_today else None

                st.markdown(f"""
                <div class='dash-card'>
                    <div style='font-size:11px;color:#6366f1;text-transform:uppercase;letter-spacing:1px;'>Active Workout</div>
                    <div style='font-size:18px;font-weight:700;color:#e2e2f0;margin:6px 0;'>{wp['plan_name']}</div>
                    <div style='font-size:12px;color:#6b6b8d;'>Week {week_idx+1} of {len(schedule)}</div>
                </div>
                """, unsafe_allow_html=True)

                if today_workout:
                    st.markdown(f"**Today:** _{today_workout.get('focus','')}_ ")
                    for ex in today_workout.get("exercises", [])[:5]:
                        st.markdown(f"<div class='exercise-item'>• {ex}</div>", unsafe_allow_html=True)
                else:
                    st.caption("Rest day today 🛌")
        else:
            st.markdown("""
            <div class='dash-card' style='text-align:center;padding:30px;'>
                <div style='font-size:30px;margin-bottom:8px;'>🏋️</div>
                <div style='color:#555577;font-size:13px;'>No active workout plan.<br>Generate one in the Planner!</div>
            </div>
            """, unsafe_allow_html=True)

    with pd_:
        if dp:
            st.markdown(f"""
            <div class='dash-card'>
                <div style='font-size:11px;color:#22c55e;text-transform:uppercase;letter-spacing:1px;'>Active Diet</div>
                <div style='font-size:18px;font-weight:700;color:#e2e2f0;margin:6px 0;'>{dp['plan_name']}</div>
                <div style='font-size:12px;color:#6b6b8d;'>~{dp.get('calories','-')} kcal/day · {dp.get('goal','-')}</div>
            </div>
            """, unsafe_allow_html=True)
            # Show today's meals from weekly plan
            plan_data = dp["plan_data"]
            today_dow_name = date.today().strftime("%A")
            days_data = plan_data.get("days", [])
            today_meals = next((d for d in days_data if d.get("day","").lower() == today_dow_name.lower()), None)
            if today_meals:
                for meal in today_meals.get("meals", [])[:3]:
                    st.markdown(f"**{meal.get('meal_name','')}:** "
                                + ", ".join(fi.get("item","") for fi in meal.get("food_items",[])[:2]))
        else:
            st.markdown("""
            <div class='dash-card' style='text-align:center;padding:30px;'>
                <div style='font-size:30px;margin-bottom:8px;'>🥗</div>
                <div style='color:#555577;font-size:13px;'>No active diet plan.<br>Generate one in the Planner!</div>
            </div>
            """, unsafe_allow_html=True)

    # ── TO-DO ──
    st.markdown("---")
    st.markdown("<div class='sec-label'>✅ Today's To-Do</div>", unsafe_allow_html=True)

    todos = get_todos(username, today)
    for todo in todos:
        tc1, tc2 = st.columns([8, 1])
        with tc1:
            done = st.checkbox(
                todo["task_text"],
                value=bool(todo["is_done"]),
                key=f"todo_{todo['id']}"
            )
            if done != bool(todo["is_done"]):
                toggle_todo(todo["id"], done)
                st.rerun()
        with tc2:
            if st.button("✕", key=f"del_todo_{todo['id']}"):
                delete_todo(todo["id"])
                st.rerun()

    new_task = st.text_input("Add a task…", key="new_todo_input",
                              placeholder="e.g. 30 min run, Drink 3L water…")
    if st.button("➕ Add Task", key="add_todo_btn"):
        if new_task.strip():
            add_todo(username, today, new_task.strip())
            st.rerun()


# ─────────────────────────────────────────────────────────────

def render_weight_tracker(username):
    st.markdown("<div class='sec-label'>⚖️ Weight Tracker</div>", unsafe_allow_html=True)

    goal = get_active_goal(username)
    history = get_weight_history(username)
    latest = get_latest_weight(username)

    # ── LOG WEIGHT ──
    with st.form("weight_form"):
        wc1, wc2, wc3 = st.columns([2, 2, 1])
        with wc1:
            w_date = st.date_input("Date", value=date.today())
        with wc2:
            w_val = st.number_input("Weight (kg)", 30.0, 300.0,
                                     float(latest["weight_kg"]) if latest else 70.0,
                                     step=0.1)
        with wc3:
            w_notes = st.text_input("Notes", placeholder="Morning, post-workout…")
        submitted_w = st.form_submit_button("📌 LOG WEIGHT", type="primary", use_container_width=True)

    if submitted_w:
        log_weight(username, w_date.isoformat(), w_val, w_notes)
        st.success(f"✅ Logged {w_val} kg on {w_date}")
        st.rerun()

    # ── CHART ──
    if history:
        df_w = pd.DataFrame(history)
        df_w["log_date"] = pd.to_datetime(df_w["log_date"])

        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=df_w["log_date"], y=df_w["weight_kg"],
            mode="lines+markers",
            line=dict(color="#818cf8", width=2.5),
            marker=dict(size=8, color="#6366f1",
                        line=dict(color="#0d0d1a", width=2)),
            name="Weight",
            hovertemplate="%{x|%b %d}: <b>%{y} kg</b><extra></extra>"
        ))

        # Goal target line
        if goal and goal.get("target_weight"):
            fig.add_hline(
                y=goal["target_weight"],
                line_dash="dot", line_color="#22c55e",
                annotation_text=f"Target: {goal['target_weight']} kg",
                annotation_font_color="#22c55e"
            )

        fig.update_layout(
            title="Weight Progress",
            height=300,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(255,255,255,0.02)",
            font=dict(family="Plus Jakarta Sans", color="#a0a0c0"),
            title_font_color="#c4c4e0",
            xaxis=dict(showgrid=False, zeroline=False, color="#555577"),
            yaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.05)",
                       zeroline=False, color="#555577"),
            margin=dict(t=40, b=20, l=10, r=10),
            legend=dict(font=dict(color="#a0a0c0"))
        )
        st.plotly_chart(fig, use_container_width=True)

        # Goal progress meter
        if goal and goal.get("start_weight") and goal.get("target_weight"):
            sw = goal["start_weight"]
            tw = goal["target_weight"]
            cw = history[-1]["weight_kg"]
            total_needed = abs(sw - tw)
            achieved = abs(sw - cw)
            pct = min(100, round((achieved / total_needed) * 100)) if total_needed > 0 else 100

            # Days remaining
            days_left = ""
            if goal.get("target_date"):
                td = date.fromisoformat(goal["target_date"])
                dl = (td - date.today()).days
                days_left = f"{dl} days left" if dl > 0 else "Target date reached!"

            st.markdown(f"""
            <div class='dash-card-accent' style='margin-top:16px;'>
                <div style='display:flex;justify-content:space-between;align-items:center;margin-bottom:10px;'>
                    <div>
                        <div style='font-size:11px;color:#6b6b8d;text-transform:uppercase;letter-spacing:1px;'>Goal Progress</div>
                        <div style='font-size:20px;font-weight:700;color:#e2e2f0;margin-top:4px;'>{goal.get('description','')}</div>
                    </div>
                    <div style='text-align:right;'>
                        <div style='font-size:28px;font-weight:800;color:#a5b4fc;'>{pct}%</div>
                        <div style='font-size:11px;color:#6b6b8d;'>{days_left}</div>
                    </div>
                </div>
                <div class='prog-bar-outer'>
                    <div class='prog-bar-inner' style='width:{pct}%;'></div>
                </div>
                <div style='display:flex;justify-content:space-between;font-size:12px;color:#6b6b8d;margin-top:6px;'>
                    <span>Start: {sw} kg</span>
                    <span>Current: {cw} kg</span>
                    <span>Target: {tw} kg</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

    # ── GOAL SETTER ──
    st.markdown("---")
    st.markdown("<div class='sec-label'>🎯 Set / Update Goal</div>", unsafe_allow_html=True)

    with st.expander("Update My Goal", expanded=(goal is None)):
        with st.form("goal_form"):
            gc1, gc2 = st.columns(2)
            with gc1:
                g_type = st.selectbox("Goal Type", ["Weight Loss","Muscle Gain","Endurance","Strength","Flexibility"])
                g_desc = st.text_input("Describe your goal", placeholder="e.g. Lose 2 kg in 2 months")
                g_start_w = st.number_input("Starting Weight (kg)", 30.0, 300.0,
                                             float(latest["weight_kg"]) if latest else 70.0, step=0.1)
            with gc2:
                g_target_w = st.number_input("Target Weight (kg)", 30.0, 300.0,
                                              float(goal["target_weight"]) if goal and goal.get("target_weight") else 65.0,
                                              step=0.1)
                g_start_d = st.date_input("Goal Start Date", value=date.today())
                g_target_d = st.date_input("Target Date", value=date.today() + timedelta(days=60))
            submitted_g = st.form_submit_button("🎯 SAVE GOAL", type="primary", use_container_width=True)

        if submitted_g:
            save_goal(username, g_type.lower().replace(" ","_"), g_desc,
                      g_start_w, g_target_w, g_start_d.isoformat(), g_target_d.isoformat())
            st.success("✅ Goal saved!")
            st.rerun()


# ─────────────────────────────────────────────────────────────

def render_weekly_review(username):
    st.markdown("<div class='sec-label'>📊 Weekly Progress Review</div>", unsafe_allow_html=True)

    week_start = _week_monday()
    week_end = (date.fromisoformat(week_start) + timedelta(days=6)).isoformat()
    stats = get_weekly_stats(username, week_start)

    if not stats:
        st.info("No diary entries this week yet. Start logging daily to see your weekly review!")
        return

    # ── KPI ROW ──
    k1, k2, k3, k4, k5 = st.columns(5)
    metrics = [
        (k1, f"{stats.get('avg_mood','—')}/5",   "Avg Mood",     "#818cf8"),
        (k2, f"{stats.get('avg_energy','—')}/5",  "Avg Energy",   "#f472b6"),
        (k3, f"{stats.get('avg_sleep','—')} hrs",  "Avg Sleep",    "#34d399"),
        (k4, f"{stats.get('workouts_completed',0)}/7","Workouts",  "#fb923c"),
        (k5, f"{stats.get('days_diet_followed',0)}/7","Diet Days", "#a78bfa"),
    ]
    for col, val, lbl, color in metrics:
        with col:
            st.markdown(f"""
            <div class='metric-card'>
                <div class='metric-value' style='color:{color};'>{val}</div>
                <div class='metric-label'>{lbl}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── MOOD + ENERGY CHART ──
    entries = stats.get("entries", [])
    if entries:
        df_e = pd.DataFrame(entries)
        df_e["entry_date"] = pd.to_datetime(df_e["entry_date"])

        fig = go.Figure()
        if "mood" in df_e.columns:
            fig.add_trace(go.Scatter(
                x=df_e["entry_date"], y=df_e["mood"],
                name="Mood", mode="lines+markers",
                line=dict(color="#818cf8",width=2),
                marker=dict(size=8,color="#6366f1")
            ))
        if "energy_level" in df_e.columns:
            fig.add_trace(go.Scatter(
                x=df_e["entry_date"], y=df_e["energy_level"],
                name="Energy", mode="lines+markers",
                line=dict(color="#f472b6",width=2,dash="dot"),
                marker=dict(size=8,color="#ec4899")
            ))
        fig.update_layout(
            title="Mood & Energy This Week",
            height=260, paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(255,255,255,0.02)",
            font=dict(family="Plus Jakarta Sans",color="#a0a0c0"),
            title_font_color="#c4c4e0",
            xaxis=dict(showgrid=False,zeroline=False,color="#555577"),
            yaxis=dict(range=[0,6],showgrid=True,gridcolor="rgba(255,255,255,0.05)",
                       zeroline=False,color="#555577"),
            margin=dict(t=40,b=20,l=10,r=10),
            legend=dict(font=dict(color="#a0a0c0"))
        )
        st.plotly_chart(fig, use_container_width=True)

    # ── AI REVIEW BUTTON ──
    if st.button("🤖 Generate AI Weekly Review", type="primary", use_container_width=True, key="gen_review"):
        goal = get_active_goal(username)
        lw = get_latest_weight(username)
        latest_w = lw["weight_kg"] if lw else None
        start_w = goal["start_weight"] if goal else None
        target_w = goal["target_weight"] if goal else None
        target_d = goal.get("target_date","") if goal else ""

        # Weight change vs previous week
        prev_ws = (date.fromisoformat(week_start) - timedelta(days=7)).isoformat()
        prev_we = (date.fromisoformat(week_start) - timedelta(days=1)).isoformat()
        prev_entries = get_diary_range(username, prev_ws, prev_we)
        w_change = 0.0

        with st.spinner("🤖 AI is analysing your week…"):
            summary, suggestion, on_track = generate_ai_weekly_review(
                username, stats, goal, latest_w, start_w, target_w, target_d
            )

        save_weekly_review(
            username, week_start, week_end,
            stats.get("avg_mood"), stats.get("avg_energy"),
            stats.get("avg_sleep"), stats.get("avg_water"),
            stats.get("workouts_completed",0), stats.get("days_diet_followed",0),
            w_change, summary, suggestion
        )

        track_color = "#22c55e" if on_track else "#f59e0b"
        track_label = "On Track ✅" if on_track else "Needs Attention ⚠️"
        st.markdown(f"""
        <div class='dash-card-accent' style='margin-top:16px;'>
            <div style='display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:14px;'>
                <div style='font-family:Syne,sans-serif;font-size:20px;font-weight:800;color:#e2e2f0;'>
                    AI Weekly Review
                </div>
                <span style='background:{track_color}22;color:{track_color};
                             border:1px solid {track_color}55;border-radius:20px;
                             padding:3px 12px;font-size:12px;font-weight:700;'>{track_label}</span>
            </div>
            <div style='color:#c4c4e0;font-size:14px;line-height:1.7;margin-bottom:14px;'>
                {summary}
            </div>
            <div style='background:rgba(99,102,241,0.08);border-radius:10px;padding:14px;'>
                <div style='font-size:11px;color:#6366f1;text-transform:uppercase;letter-spacing:1px;margin-bottom:6px;'>
                    💡 Recommendation
                </div>
                <div style='color:#c4c4e0;font-size:14px;line-height:1.6;'>{suggestion}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # ── PAST REVIEWS ──
    past = get_weekly_reviews(username, limit=8)
    if past:
        st.markdown("---")
        st.markdown("<div class='sec-label'>📚 Past Weekly Reviews</div>", unsafe_allow_html=True)
        for rev in past:
            ws = rev["week_start"]
            we = rev["week_end"]
            with st.expander(f"Week of {ws} → {we}"):
                pr1, pr2, pr3 = st.columns(3)
                pr1.metric("Mood", f"{rev.get('avg_mood','—')}/5")
                pr2.metric("Workouts", f"{rev.get('workouts_completed','—')}")
                pr3.metric("Diet Days", f"{rev.get('days_diet_followed','—')}")
                if rev.get("ai_summary"):
                    st.markdown(f"**Summary:** {rev['ai_summary']}")
                if rev.get("ai_suggestion"):
                    st.info(f"💡 {rev['ai_suggestion']}")


# ─────────────────────────────────────────────────────────────

def render_progress_charts(username):
    st.markdown("<div class='sec-label'>📈 Progress Dashboard</div>", unsafe_allow_html=True)

    diary = get_diary_last_n(username, 30)
    if not diary:
        st.info("Log at least a few days to see charts here.")
        return

    df = pd.DataFrame(diary)
    df["entry_date"] = pd.to_datetime(df["entry_date"])
    df = df.sort_values("entry_date")

    # ── STREAK + TOTAL ──
    streak = get_streak(username)
    m1, m2, m3, m4 = st.columns(4)
    m1.markdown(f"""<div class='metric-card'><div class='metric-value'>{streak}🔥</div><div class='metric-label'>Day Streak</div></div>""", unsafe_allow_html=True)
    m2.markdown(f"""<div class='metric-card'><div class='metric-value'>{len(diary)}</div><div class='metric-label'>Days Logged</div></div>""", unsafe_allow_html=True)

    if "workout_done" in df.columns:
        total_workouts = int(df["workout_done"].sum())
        m3.markdown(f"""<div class='metric-card'><div class='metric-value' style='color:#fb923c;'>{total_workouts}💪</div><div class='metric-label'>Workouts Done</div></div>""", unsafe_allow_html=True)
    if "diet_followed" in df.columns:
        diet_days = int(df["diet_followed"].sum())
        m4.markdown(f"""<div class='metric-card'><div class='metric-value' style='color:#34d399;'>{diet_days}🥗</div><div class='metric-label'>Diet Days</div></div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── MULTI-CHART ──
    ch1, ch2 = st.columns(2)
    with ch1:
        if "mood" in df.columns:
            fig = _dark_line(df, "entry_date", "mood", "Mood Over Time", "#818cf8", [0,6])
            st.plotly_chart(fig, use_container_width=True)
    with ch2:
        if "sleep_hours" in df.columns:
            fig = _dark_line(df, "entry_date", "sleep_hours", "Sleep Hours", "#34d399")
            st.plotly_chart(fig, use_container_width=True)

    ch3, ch4 = st.columns(2)
    with ch3:
        if "energy_level" in df.columns:
            fig = _dark_line(df, "entry_date", "energy_level", "Energy Level", "#f472b6", [0,6])
            st.plotly_chart(fig, use_container_width=True)
    with ch4:
        if "water_glasses" in df.columns:
            fig = _dark_line(df, "entry_date", "water_glasses", "Water Glasses", "#60a5fa")
            st.plotly_chart(fig, use_container_width=True)

    # ── WEIGHT CHART ──
    wh = get_weight_history(username, 30)
    if wh:
        st.markdown("---")
        dfw = pd.DataFrame(wh)
        dfw["log_date"] = pd.to_datetime(dfw["log_date"])
        fig = _dark_line(dfw, "log_date", "weight_kg", "Weight Progress (kg)", "#a78bfa")
        goal = get_active_goal(username)
        if goal and goal.get("target_weight"):
            fig.add_hline(y=goal["target_weight"], line_dash="dot", line_color="#22c55e",
                          annotation_text=f"Target {goal['target_weight']} kg",
                          annotation_font_color="#22c55e")
        st.plotly_chart(fig, use_container_width=True)

    # ── WORKOUT ADHERENCE BAR ──
    if "workout_done" in df.columns:
        st.markdown("---")
        df["week"] = df["entry_date"].dt.strftime("Week %W")
        weekly_w = df.groupby("week")["workout_done"].sum().reset_index()
        weekly_w.columns = ["Week","Workouts"]
        fig = px.bar(weekly_w, x="Week", y="Workouts", title="Weekly Workout Adherence",
                     color_discrete_sequence=["#6366f1"])
        fig.update_layout(
            height=220, paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(255,255,255,0.02)",
            font=dict(family="Plus Jakarta Sans",color="#a0a0c0"),
            title_font_color="#c4c4e0",
            xaxis=dict(showgrid=False,color="#555577"),
            yaxis=dict(showgrid=True,gridcolor="rgba(255,255,255,0.05)",
                       color="#555577",range=[0,8]),
            margin=dict(t=40,b=20,l=10,r=10)
        )
        st.plotly_chart(fig, use_container_width=True)


# ─────────────────────────────────────────────────────────────

def render_history_diary(username):
    st.markdown("<div class='sec-label'>📖 Diary History</div>", unsafe_allow_html=True)

    diary = get_diary_last_n(username, 30)
    if not diary:
        st.info("No diary entries yet. Start logging today!")
        return

    for entry in diary:
        ed = entry["entry_date"]
        mood_score = entry.get("mood")
        mood_emoji = MOOD_MAP.get(mood_score, (None,))[0] if mood_score else "—"
        mood_label = MOOD_MAP.get(mood_score, ("","Unknown"))[1] if mood_score else "—"

        with st.expander(f"{mood_emoji} {ed}  ·  {mood_label}  ·  Sleep {entry.get('sleep_hours','—')}h  ·  💧{entry.get('water_glasses','—')}"):
            d1, d2, d3, d4 = st.columns(4)
            d1.metric("Energy", f"{entry.get('energy_level','—')}/5")
            d2.metric("Stress", f"{entry.get('stress_level','—')}/5")
            d3.metric("Workout", "✅" if entry.get("workout_done") else "❌")
            d4.metric("Diet", "✅" if entry.get("diet_followed") else "❌")
            if entry.get("journal_text"):
                st.markdown(f"> {entry['journal_text']}")
            if entry.get("workout_notes"):
                st.caption(f"🏋️ {entry['workout_notes']}")
            if entry.get("steps_count"):
                st.caption(f"👟 {entry['steps_count']:,} steps")


# ─────────────────────────────────────────────────────────────
# MAIN ENTRY POINT
# ─────────────────────────────────────────────────────────────

def show_smart_checkin(username):
    init_tracker_db()
    st.markdown(CHECKIN_CSS, unsafe_allow_html=True)

    # ── HEADER ──
    streak = get_streak(username)
    st.markdown(f"""
    <div style='display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:8px;'>
        <div>
            <div class='page-title'>Daily Assistant</div>
            <div class='page-sub'>Your personal health manager — track, review, improve.</div>
        </div>
        <div style='text-align:right;'>
            <div style='font-family:Syne,sans-serif;font-size:32px;font-weight:800;color:#f97316;'>
                {streak}🔥
            </div>
            <div style='font-size:11px;color:#555577;text-transform:uppercase;letter-spacing:1px;'>day streak</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── TABS ──
    tab_today, tab_weight, tab_weekly, tab_charts, tab_history = st.tabs([
        "📝 Today",
        "⚖️ Weight",
        "📊 Weekly Review",
        "📈 Progress",
        "📖 History",
    ])

    with tab_today:
        render_today_diary(username)

    with tab_weight:
        render_weight_tracker(username)

    with tab_weekly:
        render_weekly_review(username)

    with tab_charts:
        render_progress_charts(username)

    with tab_history:
        render_history_diary(username)
