"""
combined_planner.py
Renders the Combined Workout + Diet Planner page for RoutineX.
Called from app.py when st.session_state.page == "combined"
"""

import streamlit as st
import base64
import math
import time
from pathlib import Path

from engine.scheduler import generate_workout_plan
from engine.nutrition import calculate_nutritional_needs
from engine.diet_generator_weekly import generate_weekly_diet_plan


# ─────────────────────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────────────────────

def get_base64_image(image_path):
    try:
        with open(image_path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    except Exception:
        return None


def apply_dark_overlay_bg(image_name: str):
    """Try to load an asset and apply it as a blurred dark-overlay page background."""
    bg = None
    for ext in [".png", ".jpg", ".jpeg"]:
        p = Path(f"assets/{image_name}{ext}")
        if p.exists():
            bg = get_base64_image(p)
            break

    if bg:
        st.markdown(f"""
        <style>
        .stApp {{
            background-image: url("data:image/png;base64,{bg}");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }}
        .main .block-container {{
            background-color: rgba(8, 8, 20, 0.82);
            padding: 2rem 2.5rem;
            border-radius: 16px;
            backdrop-filter: blur(6px);
        }}
        </style>
        """, unsafe_allow_html=True)


COMBINED_CSS = """
<style>
/* ── TYPOGRAPHY ─────────────────────────────── */
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@600;800&family=DM+Sans:wght@300;400;500&display=swap');

/* override global text to white on dark overlay */
.stMarkdown, .stMarkdown p, .stMarkdown li,
.stMarkdown h1, .stMarkdown h2, .stMarkdown h3,
.stMarkdown h4, .stMarkdown strong, .stText,
.stCaption, .stCaption p,
div[data-testid="stText"] {
    color: #FFFFFF !important;
}

label, .stNumberInput label, .stSelectbox label,
.stSlider label, .stMultiSelect label,
.stTextInput label, .stTextArea label, .stRadio label {
    color: #E0E0FF !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 13px !important;
    text-transform: uppercase;
    letter-spacing: 0.6px;
}

div[role="radiogroup"] p,
div[role="radiogroup"] div,
div[role="radiogroup"] label {
    color: #FFFFFF !important;
}

/* ── BACK BUTTON ────────────────────────────── */
div.stButton > button[kind="secondary"] {
    color: #AAAACC !important;
    background: transparent !important;
    border: 1px solid rgba(255,255,255,0.25) !important;
    font-size: 13px !important;
    border-radius: 6px !important;
    padding: 6px 14px !important;
    transition: all 0.2s;
}
div.stButton > button[kind="secondary"]:hover {
    border-color: #FFFFFF !important;
    color: #FFFFFF !important;
}

/* ── PRIMARY CTA ────────────────────────────── */
div.stButton > button[kind="primary"],
div[data-testid="stFormSubmitButton"] > button {
    background: linear-gradient(135deg, #6C63FF 0%, #44D9E8 100%) !important;
    color: #FFFFFF !important;
    font-family: 'Syne', sans-serif !important;
    font-size: 17px !important;
    font-weight: 800 !important;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    border: none !important;
    border-radius: 10px !important;
    padding: 16px 30px !important;
    box-shadow: 0 6px 24px rgba(108, 99, 255, 0.35) !important;
    transition: all 0.25s !important;
}
div.stButton > button[kind="primary"]:hover,
div[data-testid="stFormSubmitButton"] > button:hover {
    box-shadow: 0 10px 32px rgba(108, 99, 255, 0.55) !important;
    transform: translateY(-2px);
}

/* ── INPUTS ─────────────────────────────────── */
.stNumberInput input,
.stSelectbox div[data-baseweb="select"],
div[data-baseweb="input"] > input,
.stTextArea textarea,
.stTextInput input {
    background-color: rgba(255,255,255,0.07) !important;
    border: 1px solid rgba(255,255,255,0.18) !important;
    color: #FFFFFF !important;
    border-radius: 8px !important;
}
ul[data-baseweb="menu"] li {
    background-color: #1A1A2E !important;
    color: #FFFFFF !important;
}

/* ── ALERTS / INFO ──────────────────────────── */
.stAlert, div[data-testid="stAlert"] {
    background-color: rgba(108,99,255,0.15) !important;
    border: 1px solid rgba(108,99,255,0.4) !important;
    border-radius: 10px !important;
    color: #FFFFFF !important;
}
.stAlert p, .stAlert div { color: #FFFFFF !important; }

/* ── SUCCESS / ERROR ────────────────────────── */
.stSuccess, .stSuccess p {
    background-color: rgba(16,185,129,0.2) !important;
    color: #FFFFFF !important;
    border-radius: 8px !important;
}
.stError, .stError p {
    background-color: rgba(239,68,68,0.2) !important;
    color: #FFFFFF !important;
}
.stWarning, .stWarning p {
    background-color: rgba(245,158,11,0.2) !important;
    color: #FFFFFF !important;
}

/* ── SPINNER TEXT FIX ────────────────────────── */
.stSpinner > div, .stSpinner div[data-testid="stMarkdownContainer"], 
.stSpinner p, div[data-testid="stSpinner"] p,
div[data-testid="stSpinner"] div {
    color: #FFFFFF !important;
}

/* ── EXPANDERS ──────────────────────────────── */
div[data-testid="stExpander"] {
    background: rgba(255,255,255,0.05) !important;
    border: 1px solid rgba(255,255,255,0.12) !important;
    border-radius: 10px !important;
    margin-bottom: 8px;
}
div[data-testid="stExpander"] details summary p {
    color: #FFFFFF !important;
    font-family: 'Syne', sans-serif !important;
    font-size: 15px !important;
}

/* ── TABS (RESULT SECTION) ──────────────────── */
button[data-baseweb="tab"] {
    color: #888899 !important;
    font-family: 'Syne', sans-serif !important;
    font-size: 15px !important;
    background: transparent !important;
    border: none !important;
}
button[data-baseweb="tab"][aria-selected="true"] {
    color: #FFFFFF !important;
    border-bottom: 3px solid #6C63FF !important;
}

/* ── BRANDED HEADER ─────────────────────────── */
.combo-header {
    font-family: 'Syne', sans-serif;
    font-size: 48px;
    font-weight: 800;
    background: linear-gradient(90deg, #6C63FF, #44D9E8, #F59E0B);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    line-height: 1.1;
    margin-bottom: 6px;
}
.combo-sub {
    font-family: 'DM Sans', sans-serif;
    font-size: 15px;
    color: #9999BB;
    margin-bottom: 32px;
}

/* ── SECTION DIVIDER ────────────────────────── */
.section-badge {
    display: inline-block;
    font-family: 'Syne', sans-serif;
    font-size: 11px;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 2px;
    padding: 4px 14px;
    border-radius: 20px;
    margin-bottom: 18px;
}
.badge-workout { background: rgba(108,99,255,0.25); color: #A599FF; border: 1px solid rgba(108,99,255,0.5); }
.badge-diet    { background: rgba(68,217,232,0.20); color: #44D9E8; border: 1px solid rgba(68,217,232,0.4); }
.badge-result  { background: rgba(245,158,11,0.20); color: #F59E0B; border: 1px solid rgba(245,158,11,0.4); }

/* ── PLAN CARDS (RESULTS) ───────────────────── */
.result-card {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 14px;
    padding: 20px 24px;
    margin-bottom: 14px;
}
.result-card h4 {
    font-family: 'Syne', sans-serif;
    font-size: 18px;
    color: #FFFFFF;
    margin-bottom: 12px;
    border-bottom: 1px solid rgba(255,255,255,0.1);
    padding-bottom: 8px;
}

/* Meal card per day */
.day-card {
    background: linear-gradient(135deg, rgba(108,99,255,0.08) 0%, rgba(68,217,232,0.05) 100%);
    border: 1px solid rgba(108,99,255,0.25);
    border-radius: 14px;
    padding: 18px 20px;
    margin-bottom: 16px;
}
.day-title {
    font-family: 'Syne', sans-serif;
    font-size: 24px;
    font-weight: 800;
    color: #FFFFFF;
    margin-bottom: 14px;
    display: flex;
    align-items: center;
    gap: 10px;
}
.meal-block {
    background: rgba(255,255,255,0.06);
    border-left: 3px solid #44D9E8;
    padding: 16px 18px;
    margin-bottom: 14px;
    border-radius: 0 10px 10px 0;
}
.meal-block-title {
    font-family: 'Syne', sans-serif;
    font-size: 18px;
    font-weight: 700;
    color: #FFFFFF;
    text-transform: uppercase;
    letter-spacing: 1.2px;
    margin-bottom: 12px;
}
.food-row {
    display: block;
    padding: 10px 0;
    border-bottom: 1px solid rgba(255,255,255,0.08);
    font-size: 15px;
    color: #FFFFFF;
}
.food-row:last-child { border-bottom: none; }
.food-row > div {
    color: #FFFFFF !important;
}
.food-row div[style*='font-weight:500'] {
    font-size: 16px !important;
    font-weight: 600 !important;
    color: #FFFFFF !important;
}
.food-row span[style*='color:#666'] {
    color: #B8B8D0 !important;
    font-size: 14px !important;
}
.food-row div[style*='color:#777'] {
    color: #B8B8D0 !important;
    font-size: 13px !important;
}
.food-macros {
    display: flex;
    flex-wrap: wrap;
    gap: 6px;
    font-size: 13px;
    color: #FFFFFF;
    margin-top: 8px;
}
.macro-pill {
    display: inline-block;
    padding: 5px 12px;
    border-radius: 14px;
    font-size: 13px;
    font-weight: 700;
    margin-right: 4px;
}
.pill-cal { background: rgba(245,158,11,0.3); color: #FCD34D; }
.pill-p   { background: rgba(108,99,255,0.3); color: #C4BFFF; }
.pill-c   { background: rgba(68,217,232,0.3); color: #7FE9D8; }
.pill-f   { background: rgba(239,68,68,0.3);  color: #FCA5A5; }

/* ── NAV brand override ─────────────────────── */
.brand { color: #FFFFFF !important; }
.tagline { color: #AAAACC !important; }

/* ── SLIDER VALUE LABEL ─────────────────────── */
.stSlider p { color: #FFFFFF !important; }

/* divider */
hr { border-color: rgba(255,255,255,0.1) !important; }
</style>
"""

DAY_EMOJIS = {
    "monday": "🌅", "tuesday": "🔥", "wednesday": "⚡",
    "thursday": "💪", "friday": "🚀", "saturday": "🌟", "sunday": "😌"
}


def _day_emoji(day_name: str) -> str:
    return DAY_EMOJIS.get(day_name.lower(), "📅")


# ─────────────────────────────────────────────────────────────
# RESULT RENDERERS
# ─────────────────────────────────────────────────────────────

def render_workout_results(plan_data: dict, user):
    schedule = plan_data.get("schedule", [])
    if not schedule:
        st.warning("No workout schedule generated.")
        return

    st.markdown('<span class="section-badge badge-workout">💪 Workout Plan</span>', unsafe_allow_html=True)
    st.markdown(f"<p style='color:#9999BB;font-size:14px;margin-bottom:16px;'>{plan_data.get('summary','')}</p>", unsafe_allow_html=True)

    num_months = math.ceil(len(schedule) / 4)
    tabs = st.tabs([f"Month {i+1}" for i in range(num_months)])

    for i, tab in enumerate(tabs):
        with tab:
            month_weeks = schedule[i * 4: i * 4 + 4]
            for week in month_weeks:
                wk_num = week.get("week_number", "?")
                focus = week.get("focus", "General Training")
                with st.expander(f"📅 Week {wk_num}: {focus}", expanded=False):
                    for day in week.get("workouts", []):
                        day_name = day.get("day", "Day")
                        day_focus = day.get("focus", "")
                        exercises = day.get("exercises", [])
                        st.markdown(f"**{day_name}** — _{day_focus}_")
                        if not exercises:
                            st.caption("Rest Day")
                        else:
                            for ex in exercises:
                                st.text(f"• {ex}")
                        st.divider()

    # Activate for check-in
    if user:
        from database_extended import save_workout_for_checkin
        from database_tracker import save_workout_plan
        st.markdown("---")
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.info("💡 Activate this workout to track daily progress in Mental Health › Daily Check-in")
            if st.button("✅ ACTIVATE FOR DAILY CHECK-IN", type="primary", use_container_width=True, key="activate_combo_workout"):
                goal_key = st.session_state.get("combo_goal", "Custom")
                months_key = st.session_state.get("combo_months", 1)
                plan_name = f"{goal_key} – {months_key} months"
                schedule = plan_data.get("schedule", [])
                # Old checkin system
                save_workout_for_checkin(
                    username=user,
                    workout_data=plan_data,
                    plan_name=plan_name,
                    duration_weeks=len(schedule)
                )
                # New tracker DB
                save_workout_plan(
                    username=user,
                    plan_name=plan_name,
                    goal=goal_key,
                    duration_months=months_key,
                    plan_data=plan_data,
                    set_active=True
                )
                st.success("🎉 Workout activated!")
    else:
        st.warning("⚠️ Log in to activate this workout for daily tracking.")


def render_diet_results(diet_plan: dict):
    if "error" in diet_plan:
        st.error(f"Diet plan error: {diet_plan['error']}")
        if "details" in diet_plan:
            st.info(f"Details: {diet_plan['details']}")
        return

    # Validate diet_plan structure
    if not isinstance(diet_plan, dict):
        st.error("Invalid diet plan format. Please regenerate the plan.")
        st.code(str(diet_plan), language="text")
        return
    
    if "days" not in diet_plan and "summary" not in diet_plan:
        st.error("Diet plan is missing required data. Please regenerate.")
        st.code(str(diet_plan), language="json")
        return

    st.markdown('<span class="section-badge badge-diet">🥗 Weekly Diet Plan</span>', unsafe_allow_html=True)

    summary = diet_plan.get("summary", {})
    cal = summary.get("total_calories_per_day", "—")
    prot = summary.get("protein_per_day", "—")
    carbs = summary.get("carbs_per_day", "—")
    fats = summary.get("fats_per_day", "—")

    st.markdown(f"""
    <div style='display:flex;gap:12px;flex-wrap:wrap;margin-bottom:20px;'>
        <span class='macro-pill pill-cal'>🔥 {cal} kcal/day</span>
        <span class='macro-pill pill-p'>🥩 Protein {prot}g</span>
        <span class='macro-pill pill-c'>🌾 Carbs {carbs}g</span>
        <span class='macro-pill pill-f'>🫒 Fats {fats}g</span>
    </div>
    <p style='color:#9999BB;font-size:14px;margin-bottom:20px;'>{summary.get("note", "")}</p>
    """, unsafe_allow_html=True)

    days = diet_plan.get("days", [])
    if not days:
        st.warning("No diet days returned.")
        return

    # Tabs per day
    day_names = [d.get("day", f"Day {i+1}") for i, d in enumerate(days)]
    day_tabs = st.tabs(day_names)

    for i, (dtab, day_data) in enumerate(zip(day_tabs, days)):
        with dtab:
            day_name = day_data.get("day", f"Day {i+1}")
            day_cal = day_data.get("total_calories", "—")
            emoji = _day_emoji(day_name)

            st.markdown(f"""
            <div style='display:flex;align-items:center;gap:12px;margin-bottom:16px;'>
                <span style='font-size:36px;'>{emoji}</span>
                <div>
                    <div class='day-title' style='margin-bottom:0;'>{day_name}</div>
                    <span class='macro-pill pill-cal' style='margin-top:4px;'>🔥 ~{day_cal} kcal</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

            for meal in day_data.get("meals", []):
                meal_name = meal.get("meal_name", "Meal")
                food_items = meal.get("food_items", [])

                # Build meal HTML
                items_html = ""
                for fi in food_items:
                    item_name = fi.get("item", "")
                    qty = fi.get("quantity", "")
                    fi_cal = fi.get("calories", 0)
                    fi_p = fi.get("protein", 0)
                    fi_c = fi.get("carbs", 0)
                    fi_f = fi.get("fats", 0)
                    prep = fi.get("prep_note", "")

                    items_html += f"""
                    <div class='food-row'>
                        <div>
                            <div style='font-weight:600;font-size:16px;color:#FFFFFF;'>{item_name} <span style='color:#B8B8D0;font-size:14px;'>({qty})</span></div>
                            <div class='food-macros'>
                                <span class='macro-pill pill-cal'>{fi_cal} kcal</span>
                                <span class='macro-pill pill-p'>P:{fi_p}g</span>
                                <span class='macro-pill pill-c'>C:{fi_c}g</span>
                                <span class='macro-pill pill-f'>F:{fi_f}g</span>
                            </div>
                            {f"<div style='font-size:13px;color:#B8B8D0;font-style:italic;margin-top:6px;'>{prep}</div>" if prep else ""}
                        </div>
                    </div>
                    """

                st.markdown(f"""
                <div class='meal-block'>
                    <div class='meal-block-title'>{meal_name}</div>
                    {items_html}
                </div>
                """, unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────
# MAIN RENDER FUNCTION (called from app.py)
# ─────────────────────────────────────────────────────────────

def render_combined_planner(user=None):
    # Background + CSS
    apply_dark_overlay_bg("workout")
    st.markdown(COMBINED_CSS, unsafe_allow_html=True)

    # Back button
    c_back, _ = st.columns([1, 5])
    with c_back:
        if st.button("← BACK", use_container_width=True):
            st.session_state.page = "planner"
            st.rerun()

    # Header
    st.markdown("""
    <div class='combo-header'>Workout + Diet<br>Generator</div>
    <div class='combo-sub'>Fill in once — get a full workout schedule & 7-day meal plan instantly.</div>
    """, unsafe_allow_html=True)

    # ── FORM ─────────────────────────────────────────────────
    with st.form("combo_form"):

        # ── SHARED / BODY SECTION ──────────────────────────
        st.markdown('<span class="section-badge badge-workout">👤 Your Profile</span>', unsafe_allow_html=True)
        r1c1, r1c2, r1c3 = st.columns(3)
        with r1c1:
            age    = st.number_input("Age", 10, 90, 25)
            weight = st.number_input("Weight (kg)", 30.0, 200.0, 70.0)
        with r1c2:
            height = st.number_input("Height (cm)", 100.0, 250.0, 170.0)
            gender = st.selectbox("Gender", ["Male", "Female", "Other"])
        with r1c3:
            goal = st.selectbox(
                "Primary Goal",
                ["Fat Loss", "Muscle Gain", "Strength", "Endurance", "Flexibility"]
            )
            experience = st.selectbox("Experience Level", ["Beginner", "Intermediate", "Advanced"])

        st.markdown("<br>", unsafe_allow_html=True)

        # ── WORKOUT-SPECIFIC ───────────────────────────────
        st.markdown('<span class="section-badge badge-workout">💪 Workout Settings</span>', unsafe_allow_html=True)
        w1, w2, w3 = st.columns(3)
        with w1:
            available_days  = st.slider("Days / Week Available", 1, 7, 4)
        with w2:
            duration_months = st.slider("Plan Duration (Months)", 1, 12, 3)
        with w3:
            medical_conditions = st.multiselect(
                "Medical Conditions",
                ["Diabetes", "Hypertension", "Asthma", "Back Pain", "None"],
                default=["None"]
            )
        injuries = st.multiselect(
            "Injuries",
            ["Knee", "Shoulder", "Lower Back", "None"],
            default=["None"]
        )
        additional_info = st.text_area(
            "Workout Preferences / Equipment",
            placeholder="E.g., 'Home gym only', 'I love swimming', 'Focus on upper body'…"
        )

        st.markdown("<br>", unsafe_allow_html=True)

        # ── DIET-SPECIFIC ──────────────────────────────────
        st.markdown('<span class="section-badge badge-diet">🥗 Diet Settings</span>', unsafe_allow_html=True)
        d1, d2, d3 = st.columns(3)
        with d1:
            activity_level = st.selectbox(
                "Activity Level",
                ["sedentary", "lightly_active", "moderately_active", "very_active", "extra_active"]
            )
            diet_type = st.selectbox(
                "Diet Type",
                ["Omnivore", "Vegetarian", "Vegan", "Paleo", "Keto", "Gluten-Free"]
            )
        with d2:
            cuisine    = st.text_input("Preferred Cuisine", "General")
            meals_per_day = st.slider("Meals Per Day", 3, 6, 4)
        with d3:
            # Map goal to diet goal key
            goal_map = {
                "Fat Loss":    "fat_loss",
                "Muscle Gain": "muscle_gain",
                "Strength":    "muscle_gain",
                "Endurance":   "endurance",
                "Flexibility": "general_fitness"
            }
            allergies = st.multiselect(
                "Allergies / Exclusions",
                ["Nuts", "Dairy", "Shellfish", "Eggs", "Soy", "Gluten", "None"],
                default=["None"]
            )

        st.markdown("<br>", unsafe_allow_html=True)

        # ── SUBMIT ─────────────────────────────────────────
        submitted = st.form_submit_button(
            "⚡ GENERATE WORKOUT + DIET PLAN",
            type="primary",
            use_container_width=True
        )

    # ── GENERATION ───────────────────────────────────────────
    if submitted:
        # Store for activate button later
        st.session_state["combo_goal"]   = goal
        st.session_state["combo_months"] = duration_months

        profile_workout = {
            "age":                age,
            "weight":             weight,
            "height":             height,
            "experience":         experience,
            "gender":             gender,
            "available_days":     available_days,
            "medical_conditions": [m for m in medical_conditions if m != "None"],
            "injuries":           [i for i in injuries if i != "None"],
        }

        diet_goal_key = goal_map.get(goal, "general_fitness")
        nutri_profile = {
            "weight_kg":  weight,
            "height_cm":  height,
            "age":        age,
            "gender":     gender,
        }
        gen_profile = {
            "diet_type":     diet_type,
            "cuisine":       cuisine,
            "region":        cuisine,
            "allergies":     [] if "None" in allergies else allergies,
            "meals_per_day": meals_per_day,
        }

        progress_col1, progress_col2 = st.columns(2)

        # ── WORKOUT ─────────────────────────────────────────
        with progress_col1:
            with st.spinner(f"🏋️ Designing {duration_months} months of workouts…"):
                workout_data = generate_workout_plan(
                    profile_workout, goal, duration_months, additional_info
                )

        # ── NUTRITION CALC ───────────────────────────────────
        with progress_col2:
            with st.spinner("🔬 Calculating nutritional targets…"):
                targets = calculate_nutritional_needs(nutri_profile, diet_goal_key, activity_level)

        # ── WEEKLY DIET ──────────────────────────────────────
        with st.spinner("🥗 AI Chef crafting your 7-day meal plan…"):
            diet_data = generate_weekly_diet_plan(targets, gen_profile)

        # Store results
        if "error" not in workout_data:
            st.session_state["combo_workout"] = workout_data
        else:
            st.session_state.pop("combo_workout", None)
            st.error(f"Workout generation failed: {workout_data.get('error')}")

        if "error" not in diet_data:
            st.session_state["combo_diet"] = diet_data
            st.session_state["combo_targets"] = targets
        else:
            st.session_state.pop("combo_diet", None)
            st.error(f"Diet generation failed: {diet_data.get('error')}")

        # Summary banner
        if "combo_workout" in st.session_state and "combo_diet" in st.session_state:
            weeks_total = len(st.session_state["combo_workout"].get("schedule", []))
            st.success(
                f"✅ Generated {weeks_total} weeks of workouts + a full 7-day meal plan! "
                f"({targets['calories']} kcal/day | P:{targets['macros']['protein']}g)"
            )

    # ── RESULTS ──────────────────────────────────────────────
    if "combo_workout" in st.session_state or "combo_diet" in st.session_state:
        st.markdown("---")
        st.markdown('<span class="section-badge badge-result">📋 Your Plans</span>', unsafe_allow_html=True)

        result_tab_workout, result_tab_diet = st.tabs(["💪 Workout Plan", "🥗 Weekly Diet Plan"])

        with result_tab_workout:
            if "combo_workout" in st.session_state:
                render_workout_results(st.session_state["combo_workout"], user)
            else:
                st.info("Workout plan not available.")

        with result_tab_diet:
            if "combo_diet" in st.session_state:
                render_diet_results(st.session_state["combo_diet"])
            else:
                st.info("Diet plan not available.")
