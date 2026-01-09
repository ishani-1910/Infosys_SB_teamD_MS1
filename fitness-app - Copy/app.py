import streamlit as st
import json
import os
from dotenv import load_dotenv  # Import dotenv to manage environment variables

# ----------------------------
# LOAD ENVIRONMENT VARIABLES
# ----------------------------
# This loads the .env file variables (like GEMINI_API_KEY) into the environment
load_dotenv()

# IMPORT LOGIC MODULES
from engine.scheduler import create_weekly_schedule
from engine.nutrition import calculate_nutritional_needs
from engine.diet_generator import generate_diet_plan

# IMPORT DATABASE FUNCTIONS
from database import init_db, add_user, verify_user, save_plan, get_user_plans

# ----------------------------
# INITIALIZE DB ON STARTUP
# ----------------------------
init_db()

# ----------------------------
# PAGE CONFIGURATION
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
label, .stNumberInput label, .stSelectbox label, .stSlider label, .stMultiSelect label, .stTextInput label, .stRadio label {
    font-family: 'Oswald', sans-serif !important;
    text-transform: uppercase;
    font-size: 14px;
    letter-spacing: 0.5px;
    color: #000000 !important;
}

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

/* --- SELECTION CARDS (For Planner Hub) --- */
.selection-card {
    background-color: #FFFFFF;
    padding: 40px 30px;
    margin-bottom: 20px;
    border: 2px solid #000000;
    text-align: center;
    height: 100%;
}

.card-icon {
    font-size: 50px;
    margin-bottom: 20px;
    display: block;
}

.card-title {
    font-family: 'Oswald', sans-serif;
    font-size: 28px;
    font-weight: 700;
    text-transform: uppercase;
    margin-bottom: 15px;
    color: #000;
}

.card-desc {
    font-family: 'Roboto', sans-serif;
    font-size: 16px;
    color: #444;
    line-height: 1.5;
    margin-bottom: 30px;
}

/* MEAL CARD STYLES */
.meal-header {
    background-color: #f4f4f4;
    padding: 10px 15px;
    border-left: 5px solid #000;
    margin-bottom: 10px;
}
.meal-title {
    font-family: 'Oswald', sans-serif;
    font-size: 20px;
    color: #000;
    margin: 0;
}
.food-item {
    padding: 8px 0;
    border-bottom: 1px solid #eee;
    font-size: 15px;
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
            st.session_state.page = "planner"
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
            st.session_state.page = "planner"
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
            if st.button("JOIN / CREATE ACCOUNT", key="signin_cta", type="primary", use_container_width=True):
                st.session_state.page = "profile"
                st.session_state.auth_mode = 1 # Sign Up Mode
                st.rerun()
            
            st.markdown("<div class='login-text'>Already a member?</div>", unsafe_allow_html=True)
            if st.button("Log In", key="login_link", type="secondary", use_container_width=True):
                st.session_state.page = "profile"
                st.session_state.auth_mode = 0 # Login Mode
                st.rerun()
        else:
            st.success(f"Welcome back, {st.session_state.user}!")

    with right:
        # Check if file exists, otherwise show placeholder or ignore
        if os.path.exists("assets/hero.png"):
            st.image("assets/hero.png", use_container_width=True)
        else:
            st.markdown("", unsafe_allow_html=True)

# ======================================================
# PLANNER HUB (Selection Page)
# ======================================================
elif st.session_state.page == "planner":
    
    st.markdown("<h2 class='section-title' style='text-align: center;'>Choose Your Path</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #555; margin-bottom: 40px;'>Select the type of plan you want to generate today.</p>", unsafe_allow_html=True)

    c1, c_gap, c2 = st.columns([1, 0.1, 1])

    # --- WORKOUT PLAN CARD ---
    with c1:
        st.markdown("""
        <div class="selection-card">
            <div class="card-icon">🏋️</div>
            <div class="card-title">Create New<br>Workout Plan</div>
            <div class="card-desc">
                Generate a personalized weekly exercise routine based on your fitness goals, experience level, and available equipment.
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("CREATE WORKOUT PLAN", key="btn_workout_plan", type="primary", use_container_width=True):
            st.session_state.page = "scheduler"
            st.rerun()

    # --- DIET PLAN CARD ---
    with c2:
        st.markdown("""
        <div class="selection-card">
            <div class="card-icon">🥗</div>
            <div class="card-title">Create New<br>Diet Plan</div>
            <div class="card-desc">
                Get a customized meal plan tailored to your nutritional needs, dietary preferences, and calorie targets.
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("CREATE DIET PLAN", key="btn_diet_plan", type="primary", use_container_width=True):
            st.session_state.page = "diet"
            st.rerun()

# ======================================================
# WORKOUT SCHEDULER PAGE
# ======================================================
elif st.session_state.page == "scheduler":

    c_back, c_void = st.columns([1, 4]) 
    with c_back:
        if st.button("← BACK TO PLANNER", type="secondary", use_container_width=True):
            st.session_state.page = "planner"
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

        # Simple BMI calc for display
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
# DIET PLAN PAGE (AI Powered)
# ======================================================
elif st.session_state.page == "diet":
    
    c_back, c_void = st.columns([1, 4]) 
    with c_back:
        if st.button("← BACK TO PLANNER", type="secondary", use_container_width=True):
            st.session_state.page = "planner"
            st.rerun()

    st.markdown("<h2 class='section-title'>AI-Powered Diet Planner</h2>", unsafe_allow_html=True)
    st.markdown("Get a nutrition plan tailored to your metabolic needs and taste preferences.")

    with st.form("diet_form"):
        c1, c2 = st.columns(2)

        with c1:
            d_age = st.number_input("Age", 10, 90, 25)
            d_weight = st.number_input("Weight (kg)", 30.0, 200.0, 70.0)
            d_gender = st.radio("Gender", ["Male", "Female", "Other"], horizontal=True)
            d_goal = st.selectbox(
                "Goal",
                ["muscle_gain", "fat_loss", "general_fitness", "endurance", "mobility_flexibility"]
            )
            d_activity = st.selectbox(
                "Activity Level",
                ["sedentary", "lightly_active", "moderately_active", "very_active", "extra_active"]
            )

        with c2:
            d_height = st.number_input("Height (cm)", 120.0, 220.0, 170.0)
            d_type = st.selectbox("Diet Preference", ["Omnivore", "Vegetarian", "Vegan", "Paleo", "Keto", "Gluten-Free"])
            d_cuisine = st.text_input("Preferred Cuisine (e.g., Indian, Italian)", "General")
            d_meals = st.slider("Meals per day", 3, 6, 4)
            d_allergies = st.multiselect("Allergies / Exclusions", ["Nuts", "Dairy", "Shellfish", "Eggs", "Soy", "Gluten", "None"])

        st.markdown("<br>", unsafe_allow_html=True)
        submitted_diet = st.form_submit_button("GENERATE DIET PLAN", type="primary", use_container_width=True)

    if submitted_diet:
        # 1. Prepare Profiles
        nutri_profile = {
            "weight_kg": d_weight,
            "height_cm": d_height,
            "age": d_age,
            "gender": d_gender
        }
        
        gen_profile = {
            "diet_type": d_type,
            "cuisine": d_cuisine,
            "region": d_cuisine, # Mapping cuisine to region loosely
            "allergies": [] if "None" in d_allergies else d_allergies,
            "meals_per_day": d_meals
        }

        # 2. Calculate Targets
        with st.spinner("Calculating nutritional needs..."):
            targets = calculate_nutritional_needs(nutri_profile, d_goal, d_activity)
            
            st.success(f"Targets: {targets['calories']} kcal | P: {targets['macros']['protein']}g | C: {targets['macros']['carbs']}g | F: {targets['macros']['fats']}g")

        # 3. Generate Plan
        with st.spinner("AI Chef is crafting your menu..."):
            diet_plan = generate_diet_plan(targets, gen_profile)
        
        if "error" in diet_plan:
            st.error(diet_plan["error"])
            st.error(diet_plan.get("details", ""))
        else:
            st.session_state['latest_diet_plan'] = diet_plan
            
            # Display Summary
            summary = diet_plan.get("summary", {})
            st.markdown(f"### Plan Summary")
            st.info(f"{summary.get('note', 'Here is your personalized plan.')}")
            
            # Display Meals
            for meal in diet_plan.get("meals", []):
                st.markdown(f"""
                <div class="plan-card">
                    <div class="meal-header">
                        <h4 class="meal-title">{meal.get('meal_name', 'Meal')}</h4>
                    </div>
                """, unsafe_allow_html=True)
                
                for item in meal.get("food_items", []):
                    st.markdown(f"""
                    <div class="food-item">
                        <b>{item.get('item')}</b> ({item.get('quantity')})<br>
                        <span style="font-size: 13px; color: #666;">
                            {item.get('calories')} kcal | P: {item.get('protein')}g | C: {item.get('carbs')}g | F: {item.get('fats')}g
                        </span><br>
                        <i style="font-size: 13px; color: #444;">Prep: {item.get('prep_note')}</i>
                    </div>
                    """, unsafe_allow_html=True)
                
                st.markdown("</div>", unsafe_allow_html=True)

    if 'latest_diet_plan' in st.session_state and "error" not in st.session_state['latest_diet_plan']:
        st.markdown("---")
        if st.session_state.user:
            if st.button("SAVE DIET PLAN TO PROFILE", type="primary"):
                save_plan(st.session_state.user, st.session_state['latest_diet_plan'])
                st.success("Diet plan saved successfully!")
        else:
            st.warning("Sign in to save this plan.")

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
                    
                    # --- LOGIC TO DISTINGUISH WORKOUT VS DIET ---
                    # Workout plans are Lists of Days. Diet plans are Dicts with "meals" key.
                    
                    if isinstance(plan, list):
                        # WORKOUT PLAN RENDERER
                        st.caption("💪 WORKOUT SCHEDULE")
                        for day in plan:
                            st.markdown(f"**{day['day'].capitalize()} ({day['day_type'].capitalize()})**")
                            for ex in day['exercises']:
                                if isinstance(ex, dict):
                                    st.text(f"- {ex['name']}")
                                else:
                                    st.text(f"- {ex}")
                            st.divider()
                            
                    elif isinstance(plan, dict) and "meals" in plan:
                        # DIET PLAN RENDERER
                        st.caption("🥗 NUTRITION PLAN")
                        summary = plan.get("summary", {})
                        st.markdown(f"**Goal:** {summary.get('total_calories')} kcal | P: {summary.get('protein')}g")
                        
                        for meal in plan.get("meals", []):
                            st.markdown(f"**{meal.get('meal_name')}**")
                            for food in meal.get("food_items", []):
                                st.text(f"- {food.get('item')} ({food.get('quantity')})")
                            st.divider()
                    else:
                        st.warning("Unknown plan format.")

    # --- IF NOT LOGGED IN ---
    else:
        st.markdown("<h2 class='section-title'>Account Access</h2>", unsafe_allow_html=True)
        
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
                        st.session_state.user = new_user
                        st.rerun()
                    else:
                        st.error("Username already exists. Please choose another.")