import streamlit as st
from engine.scheduler import create_weekly_schedule

# ----------------------------
# Page config
# ----------------------------
st.set_page_config(
    page_title="RoutineX",
    page_icon="💪",
    layout="wide"
)

# ----------------------------
# ROUTING STATE
# ----------------------------
if "page" not in st.session_state:
    st.session_state.page = "home"

# ----------------------------
# CSS & FONTS
# ----------------------------
st.markdown("""
<style>
/* IMPORT FONTS */
@import url('https://fonts.googleapis.com/css2?family=Oswald:wght@500;700&family=Playfair+Display:wght@400;600&family=Roboto:wght@300;400&display=swap');

/* GLOBAL RESET */
.stApp {
    background-color: #FFFFFF;
    color: #000000;
    font-family: 'Roboto', sans-serif;
}

/* REMOVE DEFAULT STREAMLIT TOP PADDING */
.block-container {
    padding-top: 2rem !important;
    padding-bottom: 2rem !important;
}

header {visibility: hidden;}
footer {visibility: hidden;}

/* NAVBAR STYLING */
.navbar {
    background-color: #FFFFFF;
    padding: 10px 0px;
    margin-bottom: 10px;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.brand-container {
    line-height: 1;
}

.brand {
    font-family: 'Playfair Display', serif;
    font-size: 54px;
    font-weight: 400;
    color: #111;
    letter-spacing: -1px;
}

.tagline {
    font-family: 'Roboto', sans-serif;
    font-size: 12px;
    color: #333;
    letter-spacing: 0.5px;
    margin-top: 5px;
    margin-left: 2px;
}

.nav-links {
    display: flex;
    gap: 40px;
    font-family: 'Playfair Display', serif;
    font-size: 18px;
    color: #333;
}

.nav-links div {
    cursor: pointer;
    transition: color 0.3s;
}

.nav-links div:hover {
    color: #000;
    text-decoration: underline;
}

/* HERO SECTION */
.hero-container {
    padding-top: 20px;
    padding-right: 40px;
}

.hero-title {
    font-family: 'Oswald', sans-serif;
    font-size: 72px;
    font-weight: 700;
    line-height: 0.95;
    text-transform: uppercase;
    color: #000;
    margin-bottom: 20px;
    letter-spacing: 1px;
}

.hero-desc {
    font-family: 'Roboto', sans-serif;
    font-size: 16px;
    line-height: 1.6;
    color: #222;
    margin-bottom: 30px;
    max-width: 90%;
}

/* SECONDARY CTA SECTION */
.cta-section {
    margin-top: 40px;
    padding-top: 30px;
    border-top: 1px solid #EAEAEA;
}

.cta-title {
    font-family: 'Oswald', sans-serif;
    font-size: 32px; /* Smaller than main title */
    font-weight: 500;
    line-height: 1.1;
    text-transform: uppercase;
    color: #111;
    margin-bottom: 10px;
}

.cta-desc {
    font-family: 'Roboto', sans-serif;
    font-size: 14px;
    color: #555;
    margin-bottom: 20px;
}

.login-link {
    font-family: 'Roboto', sans-serif;
    font-size: 14px;
    color: #444;
    margin-top: 15px;
    text-align: center;
}

.login-link a {
    color: #000;
    font-weight: 600;
    text-decoration: underline;
}

/* BUTTON STYLING */
div.stButton > button, div[data-testid="stFormSubmitButton"] > button {
    background-color: #000000 !important;
    color: #FFFFFF !important;
    font-family: 'Oswald', sans-serif !important;
    font-size: 20px !important;
    font-weight: 500 !important;
    text-transform: uppercase !important;
    padding: 16px 30px !important;
    border-radius: 0px !important;
    border: none !important;
    box-shadow: none !important;
    letter-spacing: 1px !important;
    width: 100%;
}

div.stButton > button:hover, div[data-testid="stFormSubmitButton"] > button:hover {
    background-color: #333333 !important;
    color: #FFFFFF !important;
}

/* INPUT LABELS - FORCED BLACK */
label, .stNumberInput label, .stSelectbox label, .stSlider label, .stMultiSelect label {
    font-family: 'Oswald', sans-serif !important;
    text-transform: uppercase;
    font-size: 14px;
    letter-spacing: 0.5px;
    color: #000000 !important;
}

.stNumberInput input, .stSelectbox div[data-baseweb="select"] {
    color: #000000 !important; 
}

/* PLAN CARDS */
.plan-card {
    background-color: #FFFFFF;
    padding: 25px;
    margin-bottom: 20px;
    border: 1px solid #E0E0E0;
    box-shadow: 0 4px 12px rgba(0,0,0,0.05);
}

.plan-card h3 {
    font-family: 'Oswald', sans-serif;
    text-transform: uppercase;
    margin-bottom: 15px;
    font-size: 24px;
    color: #000000 !important;
}

.plan-card p, .plan-card li {
    color: #333333 !important;
}

</style>
""", unsafe_allow_html=True)

# ----------------------------
# NAVBAR
# ----------------------------
st.markdown("""
<div class="navbar">
    <div class="brand-container">
        <div class="brand">RoutineX</div>
        <div class="tagline">Plan. Train. Progress</div>
    </div>
    <div class="nav-links">
        <div>Home</div>
        <div>About</div>
        <div>Subscription</div>
        <div>Planner</div>
        <div>Profile</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ======================================================
# HOME PAGE
# ======================================================
if st.session_state.page == "home":

    left, right = st.columns([1, 1], gap="large", vertical_alignment="top")

    with left:
        # MAIN HERO SECTION
        st.markdown("""
        <div class="hero-container">
            <div class="hero-title">
                Build Your<br>Best Routine
            </div>
            <div class="hero-desc">
                RoutineX is a smart fitness scheduler designed to keep you
                consistent, focused, and progressing. Get personalized workout
                schedules based on your goals, availability, and experience —
                so every session has purpose.
            </div>
        </div>
        """, unsafe_allow_html=True)

        if st.button("LETS GENERATE MY PLAN", key="main_cta", use_container_width=True):
            st.session_state.page = "scheduler"
            st.rerun()
        
        # SECONDARY CTA / SIGN UP SECTION
        st.markdown("""
        <div class="cta-section">
            <div class="cta-title">
                Let RoutineX Be Your<br>Personal Guide
            </div>
            <div class="cta-desc">
                Track everything with RoutineX. Create an account to save your plans, track progress, and unlock premium features.
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Sign In Button (Placeholder logic)
        if st.button("SIGN IN", key="signin_cta", use_container_width=True):
            st.info("Sign In functionality would open here.")

        # Login Link Text
        st.markdown("""
        <div class="login-link">
            Already a member? <a href="#">Log In</a>
        </div>
        """, unsafe_allow_html=True)

    with right:
        st.image("assets/hero.png", use_container_width=True)

# ======================================================
# SCHEDULER PAGE
# ======================================================
if st.session_state.page == "scheduler":

    c_back, c_void = st.columns([1, 4]) 
    with c_back:
        if st.button("← BACK TO HOME", use_container_width=True):
            st.session_state.page = "home"
            st.rerun()

    st.markdown("<h2 style='font-family: Oswald; text-transform: uppercase; font-size: 36px; margin-top: 10px; color: black;'>Personalize Your Weekly Fitness Plan</h2>", unsafe_allow_html=True)

    with st.form("fitness_form"):
        c1, c2 = st.columns(2)

        with c1:
            age = st.number_input("Age", 10, 80, 22)
            weight = st.number_input("Weight (kg)", 30.0, 200.0, 60.0)
            goal = st.selectbox(
                "Goal",
                ["muscle_gain", "fat_loss", "general_fitness", "endurance", "mobility_flexibility"]
            )
            experience = st.selectbox(
                "Experience Level",
                ["beginner", "intermediate", "advanced"]
            )

        with c2:
            height = st.number_input("Height (cm)", 120.0, 220.0, 165.0)
            available_days = st.slider("Days per week", 3, 6, 5)
            medical_conditions = st.multiselect(
                "Medical Conditions",
                ["cardiac", "diabetes", "joint_issues", "asthma", "hypertension", "none"]
            )
            injuries = st.multiselect(
                "Injuries",
                ["knee", "shoulder", "back", "ankle", "none"]
            )

        st.markdown("<br>", unsafe_allow_html=True)
        
        submitted = st.form_submit_button("GENERATE SCHEDULE", use_container_width=True)

    if submitted:
        medical_conditions = [] if "none" in medical_conditions else medical_conditions
        injuries = [] if "none" in injuries else injuries

        bmi = weight / ((height / 100) ** 2)
        if bmi < 18.5:
            bmi_status = "Underweight"
        elif bmi < 25:
            bmi_status = "Healthy"
        elif bmi < 30:
            bmi_status = "Overweight"
        else:
            bmi_status = "Obese"

        st.info(f"**BMI:** {bmi:.1f} — {bmi_status}")

        schedule = create_weekly_schedule(
            goal, experience, medical_conditions, injuries, available_days
        )

        for i, day in enumerate(schedule, 1):
            st.markdown(
                f"<div class='plan-card'><h3>Day {i}: {day['day_type'].capitalize()}</h3>",
                unsafe_allow_html=True
            )

            if not day["exercises"]:
                st.markdown("- No exercises (filtered for safety)")
            else:
                for ex in day["exercises"]:
                    if isinstance(ex, dict):
                        st.markdown(
                            f"- **{ex['name']}** | Sets: {ex.get('sets','-')}, Reps/Time: {ex.get('reps', ex.get('time','-'))}"
                        )
                    else:
                        st.markdown(f"- **{ex}**")

            st.markdown("</div>", unsafe_allow_html=True)