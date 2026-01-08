import streamlit as st
from engine.scheduler import create_weekly_schedule
# IMPORT DATABASE FUNCTIONS
# Ensure database.py is in the same folder
from database import init_db, add_user, verify_user, save_plan, get_user_plans

# ----------------------------
# INITIALIZE DB ON STARTUP
# ----------------------------
init_db()

# ----------------------------
# Page config
# ----------------------------
st.set_page_config(
    page_title="RoutineX",
    page_icon="💪",
    layout="wide"
)

# ----------------------------
# SESSION STATE INITIALIZATION
# ----------------------------
if "page" not in st.session_state:
    st.session_state.page = "home"
if "user" not in st.session_state:
    st.session_state.user = None  # Tracks logged in username
if "auth_mode" not in st.session_state:
    st.session_state.auth_mode = 0  # 0 = Login, 1 = Sign Up

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
    padding-top: 1rem !important;
    padding-bottom: 2rem !important;
}

header {visibility: hidden;}
footer {visibility: hidden;}

/* --- NAVIGATION BUTTONS (Secondary) --- */
div.stButton > button[kind="secondary"] {
    background-color: transparent !important;
    color: #333 !important;
    font-family: 'Playfair Display', serif !important;
    font-size: 18px !important;
    border: none !important;
    box-shadow: none !important;
    padding: 0px !important;
    transition: color 0.3s;
}

div.stButton > button[kind="secondary"]:hover {
    color: #000 !important;
    text-decoration: underline !important;
}

div.stButton > button[kind="secondary"]:focus {
    color: #000 !important;
    box-shadow: none !important;
    outline: none !important;
}

/* --- MAIN CTA BUTTONS (Primary) --- */
div.stButton > button[kind="primary"], div[data-testid="stFormSubmitButton"] > button {
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

div.stButton > button[kind="primary"]:hover, div[data-testid="stFormSubmitButton"] > button:hover {
    background-color: #333333 !important;
    color: #FFFFFF !important;
}

/* --- INPUT FIELDS --- */
/* Target generic labels */
label, .stNumberInput label, .stSelectbox label, .stSlider label, .stMultiSelect label, .stTextInput label, .stRadio label {
    font-family: 'Oswald', sans-serif !important;
    text-transform: uppercase;
    font-size: 14px;
    letter-spacing: 0.5px;
    color: #000000 !important;
}

/* FIX FOR RADIO BUTTON OPTIONS BEING WHITE */
/* This specifically targets the text inside the radio options */
div[role="radiogroup"] p, div[role="radiogroup"] div {
    color: #000000 !important;
    font-family: 'Oswald', sans-serif !important;
}

.stNumberInput input, 
.stSelectbox div[data-baseweb="select"], 
div[data-baseweb="input"] > input {
    color: #FFFFFF !important; /* White Text */
    background-color: #262730 !important; /* Dark Background */
    border-radius: 4px !important;
}

/* Dropdown menu items */
ul[data-baseweb="menu"] li {
    color: #FFFFFF !important;
    background-color: #262730 !important;
}

/* --- TEXT STYLES --- */
.brand {
    font-family: 'Playfair Display', serif;
    font-size: 48px;
    font-weight: 400;
    color: #111;
    letter-spacing: -1px;
    line-height: 1;
}

.tagline {
    font-family: 'Roboto', sans-serif;
    font-size: 12px;
    color: #333;
    letter-spacing: 0.5px;
    margin-top: 5px;
    margin-left: 2px;
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

.section-title {
    font-family: 'Oswald', sans-serif;
    font-size: 36px;
    font-weight: 500;
    text-transform: uppercase;
    color: #000;
    margin-bottom: 20px;
}

.cta-title {
    font-family: 'Oswald', sans-serif;
    font-size: 32px;
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

.login-text {
    font-family: 'Roboto', sans-serif;
    font-size: 14px;
    color: #444;
    margin-top: 15px;
    text-align: center;
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
# NAVBAR FUNCTION
# ----------------------------
def navbar():
    c1, c_space, c2, c3, c4, c5, c6 = st.columns([3, 1, 0.7, 0.7, 1, 0.7, 0.7])
    
    with c1:
        st.markdown("""
        <div class="brand">RoutineX</div>
        <div class="tagline">Plan. Train. Progress</div>
        """, unsafe_allow_html=True)
    
    with c2:
        if st.button("Home", key="nav_home", use_container_width=True):
            st.session_state.page = "home"
            st.rerun()
    with c3:
        if st.button("About", key="nav_about", use_container_width=True):
            st.session_state.page = "about"
            st.rerun()
    with c4:
        if st.button("Subscription", key="nav_sub", use_container_width=True):
            st.session_state.page = "subscription"
            st.rerun()
    with c5:
        if st.button("Planner", key="nav_planner", use_container_width=True):
            st.session_state.page = "scheduler"
            st.rerun()
    with c6:
        label = "Profile" if not st.session_state.user else f"{st.session_state.user}"
        if st.button(label, key="nav_profile", use_container_width=True):
            st.session_state.page = "profile"
            st.rerun()

    st.markdown("<div style='margin-bottom: 20px; border-bottom: 1px solid #eee;'></div>", unsafe_allow_html=True)

navbar()

# ======================================================
# HOME PAGE
# ======================================================
if st.session_state.page == "home":

    left, right = st.columns([1, 1], gap="large", vertical_alignment="top")

    with left:
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

        if st.button("LETS GENERATE MY PLAN", key="main_cta", type="primary", use_container_width=True):
            st.session_state.page = "scheduler"
            st.rerun()
        
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

        if st.session_state.user is None:
            # THIS BUTTON SETS AUTH_MODE TO 1 (SIGN UP)
            if st.button("JOIN / CREATE ACCOUNT", key="signin_cta", type="primary", use_container_width=True):
                st.session_state.page = "profile"
                st.session_state.auth_mode = 1 # Sign Up Mode
                st.rerun()
            
            # THIS LINK SETS AUTH_MODE TO 0 (LOGIN)
            st.markdown("<div class='login-text'>Already a member?</div>", unsafe_allow_html=True)
            if st.button("Log In", key="login_link", type="secondary", use_container_width=True):
                st.session_state.page = "profile"
                st.session_state.auth_mode = 0 # Login Mode
                st.rerun()
        else:
            st.success(f"Welcome back, {st.session_state.user}!")

    with right:
        st.image("assets/hero.png", use_container_width=True)

# ======================================================
# SCHEDULER PAGE
# ======================================================
elif st.session_state.page == "scheduler":

    c_back, c_void = st.columns([1, 4]) 
    with c_back:
        if st.button("← BACK TO HOME", type="primary", use_container_width=True):
            st.session_state.page = "home"
            st.rerun()

    st.markdown("<h2 class='section-title'>Personalize Your Weekly Fitness Plan</h2>", unsafe_allow_html=True)

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
        submitted = st.form_submit_button("GENERATE SCHEDULE", type="primary", use_container_width=True)

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
        
        st.session_state['latest_schedule'] = schedule

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

    if 'latest_schedule' in st.session_state:
        st.markdown("---")
        if st.session_state.user:
            if st.button("SAVE THIS PLAN TO PROFILE", type="primary"):
                save_plan(st.session_state.user, st.session_state['latest_schedule'])
                st.success("Plan saved successfully! Go to your Profile to view it.")
        else:
            st.warning("Sign in to save this plan to your profile.")

# ======================================================
# ABOUT PAGE
# ======================================================
elif st.session_state.page == "about":
    st.markdown("<h2 class='section-title'>About RoutineX</h2>", unsafe_allow_html=True)
    
    st.markdown("""
    <div style='font-size: 18px; line-height: 1.6; color: #333; margin-bottom: 30px;'>
        RoutineX is a smart fitness scheduler designed to keep you consistent, focused, and progressing. 
        Whether you are a beginner looking to get started or an advanced athlete optimizing your routine, 
        RoutineX builds personalized workout schedules based on your unique goals, availability, and experience.
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div style='background-color: #f0f0f0; padding: 20px; border-left: 6px solid #000000; border-radius: 4px;'>
        <span style='font-weight: bold; font-size: 16px; color: #000;'>NOTE:</span>
        <span style='font-size: 16px; color: #333;'> This project is an internship project as part of the Infosys Springboard internship.</span>
    </div>
    <br>
    """, unsafe_allow_html=True)

    if st.button("GO TO HOME", type="primary"):
        st.session_state.page = "home"
        st.rerun()

# ======================================================
# SUBSCRIPTION PAGE
# ======================================================
elif st.session_state.page == "subscription":
    st.markdown("<h2 class='section-title'>Subscription</h2>", unsafe_allow_html=True)
    st.markdown("""
    <div style='text-align: center; padding: 50px;'>
        <h1 style='font-family: Oswald; font-size: 60px; color: #ccc;'>COMING SOON</h1>
        <p style='font-size: 18px; color: #666;'>We are working hard to bring you premium features.</p>
    </div>
    """, unsafe_allow_html=True)

# ======================================================
# PROFILE PAGE
# ======================================================
elif st.session_state.page == "profile":
    
    # --- IF LOGGED IN ---
    if st.session_state.user:
        c1, c2 = st.columns([3, 1])
        with c1:
            st.markdown(f"<h2 class='section-title'>Hello, {st.session_state.user}</h2>", unsafe_allow_html=True)
        with c2:
            if st.button("LOGOUT", type="secondary"):
                st.session_state.user = None
                st.rerun()
        
        st.markdown("### Your Saved Plans")
        saved_plans = get_user_plans(st.session_state.user)
        
        if not saved_plans:
            st.info("You don't have any saved plans yet. Go to the Planner to create one!")
        else:
            for idx, item in enumerate(saved_plans):
                with st.expander(f"Plan created on {item['created_at']}"):
                    plan = item['plan']
                    for day in plan:
                        st.markdown(f"**{day['day'].capitalize()} ({day['day_type'].capitalize()})**")
                        for ex in day['exercises']:
                            if isinstance(ex, dict):
                                st.text(f"- {ex['name']}")
                            else:
                                st.text(f"- {ex}")
                        st.divider()

    # --- IF NOT LOGGED IN ---
    else:
        st.markdown("<h2 class='section-title'>Account Access</h2>", unsafe_allow_html=True)
        
        # USE A RADIO BUTTON INSTEAD OF TABS TO ENSURE CORRECT FORM IS SHOWN
        # This listens to the st.session_state.auth_mode set by the Home page buttons
        mode_select = st.radio(
            "Choose Action", 
            ["Login", "Create Account"], 
            index=st.session_state.auth_mode,
            horizontal=True
        )

        st.markdown("<br>", unsafe_allow_html=True)

        # --- LOGIN FORM ---
        if mode_select == "Login":
            st.subheader("Welcome Back")
            with st.form("login_form"):
                username = st.text_input("Username")
                password = st.text_input("Password", type="password")
                submit = st.form_submit_button("LOGIN", type="primary")
                
                if submit:
                    if verify_user(username, password):
                        st.session_state.user = username
                        st.success("Login successful!")
                        st.rerun()
                    else:
                        st.error("Invalid username or password")

        # --- SIGN UP FORM ---
        else:
            st.subheader("New User Registration")
            st.markdown("Create an account to save your plans.")
            with st.form("signup_form"):
                new_user = st.text_input("Choose Username")
                new_pass = st.text_input("Choose Password", type="password")
                submit_signup = st.form_submit_button("CREATE ACCOUNT", type="primary")
                
                if submit_signup:
                    if len(new_pass) < 4:
                        st.warning("Password must be at least 4 characters")
                    elif add_user(new_user, new_pass):
                        st.success(f"Account created for {new_user}! Logging you in...")
                        # AUTO LOGIN AFTER SIGNUP
                        st.session_state.user = new_user
                        st.rerun()
                    else:
                        st.error("Username already exists. Please choose another.")