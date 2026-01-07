import streamlit as st
from engine.scheduler import create_weekly_schedule

# ----------------------------
# Page config
# ----------------------------
st.set_page_config(
    page_title="My Fitness AI Planner",
    page_icon="💪",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ----------------------------
# Session state
# ----------------------------
if "page" not in st.session_state:
    st.session_state.page = "home"

# ----------------------------
# CSS (STREAMLIT-SAFE)
# ----------------------------
st.markdown("""
<style>

/* -------- GLOBAL -------- */
.stApp {
    background-color: #F6F1EB;
    color: #2F2A25;
}

/* -------- NAVBAR -------- */
.navbar {
    background-color: #E8DED4;
    padding: 8px 24px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 1px solid rgba(0,0,0,0.08);
}

/* Navbar left */
.nav-left {
    display: flex;
    gap: 20px;
}

.nav-link {
    color: #2F2A25;
    font-size: 14px;
    font-weight: 500;
    cursor: pointer;
}

.nav-link:hover {
    text-decoration: underline;
}

/* Navbar right avatar */
.user-avatar {
    width: 32px;
    height: 32px;
    border-radius: 50%;
    background-color: #CBB6A2;
    color: #2F2A25;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: bold;
}

/* -------- HERO -------- */
.hero h1 {
    color: #2F2A25;
}

.hero h3 {
    color: #5A524C;
}

/* -------- BUTTONS -------- */
.stButton > button {
    background-color: #CBB6A2;
    color: #2F2A25;
    font-weight: 600;
    border-radius: 10px;
    padding: 0.7em 1.4em;
    font-size: 16px;
    border: none;
}

.stButton > button:hover {
    background-color: #B9A189;
}

/* -------- INFO BOX -------- */
.stAlert {
    background-color: #EFE6DC !important;
    color: #2F2A25 !important;
    border-radius: 12px;
}

/* -------- PLAN CARDS -------- */
.plan-card {
    background-color: #FFF9F4;
    padding: 20px;
    margin-bottom: 18px;
    border-radius: 16px;
    border: 1px solid #E6D8CC;
}

.plan-card h3 {
    color: #2F2A25 !important;
    font-size: 20px;
    font-weight: 700;
}

.plan-card p,
.plan-card li,
.plan-card strong {
    color: #3B342F !important;
    font-size: 15px;
}

/* -------- FOOTER -------- */
.footer {
    margin-top: 120px;
    text-align: center;
    font-size: 13px;
    color: #5A524C;
}

</style>
""", unsafe_allow_html=True)


# ----------------------------
# BMI Helper
# ----------------------------
def calculate_bmi(weight_kg, height_cm):
    height_m = height_cm / 100
    bmi = round(weight_kg / (height_m ** 2), 1)

    if bmi < 18.5:
        status = "Underweight"
    elif bmi < 25:
        status = "Healthy"
    elif bmi < 30:
        status = "Overweight"
    else:
        status = "Obese"

    return bmi, status

# ============================
# HOME PAGE
# ============================
if st.session_state.page == "home":

    # NAV BAR (NORMAL FLOW — WORKS)
    st.markdown("""
    <div class="navbar">
        <div class="nav-left">
            <div class="nav-link">About</div>
            <div class="nav-link">Sign In</div>
        </div>
        <div class="user-avatar">U</div>
    </div>
    """, unsafe_allow_html=True)

    # HERO
    st.markdown("""
    <div class="hero">
        <h1>Welcome to Your Fitness Planner 💪</h1>
        <h3 style="font-weight:400;">Personalized workouts. Simple. Safe. Effective.</h3>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("Generate My Plan"):
            st.session_state.page = "scheduler"
            st.rerun()

    # FOOTER
    st.markdown(
        "<div class='footer'>Made with ❤️ in India</div>",
        unsafe_allow_html=True
    )

# ============================
# SCHEDULER PAGE (SCROLLABLE)
# ============================
elif st.session_state.page == "scheduler":

    col_left, col_right = st.columns([6, 1])
    with col_right:
        if st.button("⬅ Back"):
            st.session_state.page = "home"
            st.rerun()

    st.markdown(
        "<h2 style='text-align:center; color:#1B4332;'>Create Your Weekly Fitness Plan</h2>",
        unsafe_allow_html=True
    )

    with st.form("fitness_form"):
        col1, col2 = st.columns(2)

        with col1:
            age = st.number_input("Age", 10, 80, step=1)
            weight = st.number_input("Weight (kg)", 30.0, 200.0, step=0.5)
            height = st.number_input("Height (cm)", 120.0, 220.0, step=1.0)
            goal = st.selectbox(
                "Goal",
                ["muscle_gain", "fat_loss", "general_fitness", "endurance", "mobility_flexibility"]
            )

        with col2:
            experience = st.selectbox("Experience Level", ["beginner", "intermediate", "advanced"])
            available_days = st.slider("Days per week", 3, 6, 5)
            medical_conditions = st.multiselect(
                "Medical Conditions",
                ["cardiac", "diabetes", "joint_issues", "asthma", "hypertension", "none"]
            )
            injuries = st.multiselect(
                "Injuries",
                ["knee", "shoulder", "back", "ankle", "none"]
            )

        submitted = st.form_submit_button("Generate Schedule")

    if submitted:
        medical_conditions = [] if "none" in medical_conditions else medical_conditions
        injuries = [] if "none" in injuries else injuries

        bmi, bmi_status = calculate_bmi(weight, height)

        st.info(
            f"""
            **Age:** {age}  
            **Weight:** {weight} kg  
            **Height:** {height} cm  
            **BMI:** **{bmi}** ({bmi_status})
            """
        )

        schedule = create_weekly_schedule(
            goal, experience, medical_conditions, injuries, available_days
        )

        for i, day in enumerate(schedule, 1):
            st.markdown(
                f"<div class='plan-card'><h3>Day {i}: {day['day_type'].capitalize()}</h3>",
                unsafe_allow_html=True
            )

            if not day["exercises"]:
                st.markdown("- Rest / Recovery Day")
            else:
                for ex in day["exercises"]:
                    if isinstance(ex, dict):
                        st.markdown(
                            f"- **{ex['name']}** | Sets: {ex.get('sets')} | Reps/Time: {ex.get('reps', ex.get('time'))}"
                        )
                    else:
                        st.markdown(f"- **{ex}**")

            st.markdown("</div>", unsafe_allow_html=True)
