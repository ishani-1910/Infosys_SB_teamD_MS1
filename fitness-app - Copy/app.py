import streamlit as st
import json
import os
from dotenv import load_dotenv

# ----------------------------
# LOAD ENVIRONMENT VARIABLES
# ----------------------------
load_dotenv(override=True)

# IMPORT LOGIC MODULES
from engine.scheduler import generate_workout_plan
from engine.nutrition import calculate_nutritional_needs
from engine.diet_generator import generate_diet_plan

# NEW: IMPORT MENTAL HEALTH MODULE
from mental_health import render_mental_health_page

# IMPORT DATABASE FUNCTIONS
from database import init_db, add_user, verify_user, save_plan, get_user_plans, delete_plan
from database_extended import (
    save_workout_for_checkin,
    get_active_workout,
    get_canvas_entries,
    get_wins,
    delete_canvas_entry,
    delete_wins
)

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
    st.session_state.user = None
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

/* --- FIX: FORCE OUTPUT TEXT TO BLACK --- */
/* This solves the "Invisible White Font" issue in the Workout Plan */
div[data-testid="stText"], .stMarkdown p, .stMarkdown li, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
    color: #000000 !important;
}

/* --- TABS STYLING (FIXED VISIBILITY) --- */
button[data-baseweb="tab"] {
    font-family: 'Oswald', sans-serif !important;
    font-size: 20px !important;
    font-weight: 500 !important;
    color: #888888 !important; /* Grey for inactive tabs */
    background-color: transparent !important;
    border: none !important;
}

button[data-baseweb="tab"][aria-selected="true"] {
    color: #000000 !important; /* Black for ACTIVE tab */
    border-bottom: 3px solid #000000 !important; /* Underline for active */
    font-weight: 700 !important;
}

button[data-baseweb="tab"]:hover {
    color: #000000 !important;
    background-color: #F0F0F0 !important;
}

/* --- EXPANDER STYLING --- */
div[data-testid="stExpander"] details summary p {
    font-family: 'Oswald', sans-serif !important;
    font-size: 18px !important;
    color: #000000 !important;
    font-weight: 500 !important;
}

div[data-testid="stExpander"] details summary:hover p,
div[data-testid="stExpander"] details summary:focus p {
    color: #000000 !important;
}

div[data-testid="stExpander"] {
    border: 1px solid #E0E0E0 !important;
    border-radius: 4px !important;
    background-color: #FFFFFF !important;
    color: #000000 !important;
}

/* --- BUTTONS --- */
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
label, .stNumberInput label, .stSelectbox label, .stSlider label, .stMultiSelect label, .stTextInput label, .stRadio label, .stTextArea label {
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

/* Keep inputs White Text on Dark Background */
.stNumberInput input, 
.stSelectbox div[data-baseweb="select"], 
div[data-baseweb="input"] > input,
.stTextArea textarea {
    color: #FFFFFF !important; 
    background-color: #262730 !important; 
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

.plan-card p, .plan-card li, .plan-card div, .plan-card span, .plan-card strong {
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
    
    # --- TWO COLUMN HERO SECTION ---
    left, right = st.columns([1.2, 1], gap="large", vertical_alignment="top")

    with left:
        # --- MAIN HERO TEXT ---
        st.markdown("""
        <div style='margin-bottom: 40px;'>
            <h1 style='
                font-family: "Oswald", sans-serif;
                font-size: 64px;
                font-weight: 700;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
                margin: 0;
                line-height: 1.1;
            '>Transform Your<br>Life Today</h1>
            <p style='
                font-family: "Roboto", sans-serif;
                font-size: 18px;
                color: #555;
                margin-top: 20px;
                line-height: 1.8;
            '>
                RoutineX is your personal guide to wellness, fitness, and mental clarity. 
                Get personalized workout schedules, nutrition plans, and mental health support —
                all tailored to your unique goals and lifestyle.
            </p>
            <div style='
                background: linear-gradient(135deg, #667eea 0%, #f093fb 100%);
                padding: 15px 25px;
                border-radius: 10px;
                display: inline-block;
                margin-top: 20px;
            '>
                <p style='
                    font-family: "Playfair Display", serif;
                    font-size: 16px;
                    color: #FFFFFF;
                    margin: 0;
                    font-style: italic;
                '>"The only person you are destined to become is the person you decide to be."</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

        if st.button("START YOUR JOURNEY", key="main_cta", type="primary", use_container_width=True):
            st.session_state.page = "planner"
            st.rerun()

    with right:
        # --- RIGHT SIDE: INSPIRATIONAL IMAGE ---
        st.markdown("""
        <div style='
            background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
            border-radius: 20px;
            padding: 40px;
            text-align: center;
            box-shadow: 0 15px 40px rgba(102, 126, 234, 0.3);
        '>
            <img src='https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?w=600' 
                 style='
                    width: 100%;
                    height: 400px;
                    object-fit: cover;
                    border-radius: 15px;
                    box-shadow: 0 10px 30px rgba(0,0,0,0.2);
                 ' />
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)

    # --- DISCOVER YOUR PATH (FULL WIDTH) ---
    st.markdown("""
    <h2 style='
        text-align: center;
        font-family: "Oswald", sans-serif;
        font-size: 48px;
        color: #1a1a2e;
        margin: 60px 0 40px 0;
        font-weight: 700;
    '>Discover Your Path</h2>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3, gap="medium")

    with col1:
        st.markdown("""
        <div style='
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            padding: 40px 30px;
            border-radius: 20px;
            text-align: center;
            box-shadow: 0 10px 30px rgba(245, 87, 108, 0.3);
            height: 280px;
            display: flex;
            flex-direction: column;
            justify-content: center;
        '>
            <div style='font-size: 60px; margin-bottom: 20px;'>💪</div>
            <h3 style='
                font-family: "Oswald", sans-serif;
                font-size: 26px;
                color: #FFFFFF;
                margin: 0 0 15px 0;
                font-weight: 600;
            '>Fitness Journey</h3>
            <p style='
                color: rgba(255,255,255,0.95);
                font-size: 16px;
                line-height: 1.6;
                margin: 0;
            '>Personalized workout plans designed for your goals and fitness level</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div style='
            background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
            padding: 40px 30px;
            border-radius: 20px;
            text-align: center;
            box-shadow: 0 10px 30px rgba(0, 242, 254, 0.3);
            height: 280px;
            display: flex;
            flex-direction: column;
            justify-content: center;
        '>
            <div style='font-size: 60px; margin-bottom: 20px;'>🥗</div>
            <h3 style='
                font-family: "Oswald", sans-serif;
                font-size: 26px;
                color: #FFFFFF;
                margin: 0 0 15px 0;
                font-weight: 600;
            '>Nutrition Mastery</h3>
            <p style='
                color: rgba(255,255,255,0.95);
                font-size: 16px;
                line-height: 1.6;
                margin: 0;
            '>Customized meal plans that fuel your body and hit your macros</p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div style='
            background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
            padding: 40px 30px;
            border-radius: 20px;
            text-align: center;
            box-shadow: 0 10px 30px rgba(168, 237, 234, 0.3);
            height: 280px;
            display: flex;
            flex-direction: column;
            justify-content: center;
        '>
            <div style='font-size: 60px; margin-bottom: 20px;'>🧘</div>
            <h3 style='
                font-family: "Oswald", sans-serif;
                font-size: 26px;
                color: #1a1a2e;
                margin: 0 0 15px 0;
                font-weight: 600;
            '>Mental Wellness</h3>
            <p style='
                color: #2d2d2d;
                font-size: 16px;
                line-height: 1.6;
                margin: 0;
            '>Mindfulness practices and mental health support for balance</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)

    # --- WHY CHOOSE ROUTINEX (FULL WIDTH) ---
    st.markdown("""
    <h2 style='
        text-align: center;
        font-family: "Oswald", sans-serif;
        font-size: 48px;
        color: #1a1a2e;
        margin: 60px 0 40px 0;
        font-weight: 700;
    '>Why Choose RoutineX?</h2>
    """, unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4, gap="medium")

    with col1:
        st.markdown("""
        <div style='
            background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%);
            padding: 30px 20px;
            border-radius: 15px;
            text-align: center;
            box-shadow: 0 8px 20px rgba(252, 182, 159, 0.3);
            height: 220px;
            display: flex;
            flex-direction: column;
            justify-content: center;
        '>
            <div style='font-size: 48px; margin-bottom: 15px;'>🎯</div>
            <h3 style='
                font-family: "Oswald", sans-serif;
                font-size: 22px;
                color: #1a1a2e;
                margin: 0 0 10px 0;
                font-weight: 600;
            '>Personalized</h3>
            <p style='
                color: #2d2d2d;
                font-size: 15px;
                margin: 0;
                line-height: 1.5;
            '>Tailored to your unique goals and lifestyle</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div style='
            background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
            padding: 30px 20px;
            border-radius: 15px;
            text-align: center;
            box-shadow: 0 8px 20px rgba(168, 237, 234, 0.3);
            height: 220px;
            display: flex;
            flex-direction: column;
            justify-content: center;
        '>
            <div style='font-size: 48px; margin-bottom: 15px;'>📊</div>
            <h3 style='
                font-family: "Oswald", sans-serif;
                font-size: 22px;
                color: #1a1a2e;
                margin: 0 0 10px 0;
                font-weight: 600;
            '>Track Progress</h3>
            <p style='
                color: #2d2d2d;
                font-size: 15px;
                margin: 0;
                line-height: 1.5;
            '>Monitor your journey and celebrate wins</p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div style='
            background: linear-gradient(135deg, #ff9a9e 0%, #fecfef 100%);
            padding: 30px 20px;
            border-radius: 15px;
            text-align: center;
            box-shadow: 0 8px 20px rgba(255, 154, 158, 0.3);
            height: 220px;
            display: flex;
            flex-direction: column;
            justify-content: center;
        '>
            <div style='font-size: 48px; margin-bottom: 15px;'>🧠</div>
            <h3 style='
                font-family: "Oswald", sans-serif;
                font-size: 22px;
                color: #1a1a2e;
                margin: 0 0 10px 0;
                font-weight: 600;
            '>Holistic</h3>
            <p style='
                color: #2d2d2d;
                font-size: 15px;
                margin: 0;
                line-height: 1.5;
            '>Mind-body connection for total wellness</p>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown("""
        <div style='
            background: linear-gradient(135deg, #fbc2eb 0%, #a6c1ee 100%);
            padding: 30px 20px;
            border-radius: 15px;
            text-align: center;
            box-shadow: 0 8px 20px rgba(166, 193, 238, 0.3);
            height: 220px;
            display: flex;
            flex-direction: column;
            justify-content: center;
        '>
            <div style='font-size: 48px; margin-bottom: 15px;'>⚡</div>
            <h3 style='
                font-family: "Oswald", sans-serif;
                font-size: 22px;
                color: #1a1a2e;
                margin: 0 0 10px 0;
                font-weight: 600;
            '>Science-Backed</h3>
            <p style='
                color: #2d2d2d;
                font-size: 15px;
                margin: 0;
                line-height: 1.5;
            '>Based on proven fitness principles</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)

    # --- USER ACCOUNT SECTION (CENTERED) ---
    if st.session_state.user is None:
        st.markdown("""
        <div style='
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 50px 40px;
            border-radius: 20px;
            text-align: center;
            margin: 60px auto 40px auto;
            max-width: 700px;
            box-shadow: 0 15px 40px rgba(102, 126, 234, 0.3);
        '>
            <h3 style='
                font-family: "Oswald", sans-serif;
                font-size: 36px;
                color: #FFFFFF;
                margin: 0 0 15px 0;
                font-weight: 700;
            '>Join the Community</h3>
            <p style='
                color: rgba(255,255,255,0.95);
                font-size: 18px;
                margin: 0 0 30px 0;
                line-height: 1.6;
            '>Create an account to save your plans, track progress, and unlock premium features</p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            subcol1, subcol2 = st.columns(2, gap="small")
            with subcol1:
                if st.button("CREATE ACCOUNT", key="signin_cta", type="primary", use_container_width=True):
                    st.session_state.page = "profile"
                    st.session_state.auth_mode = 1
                    st.rerun()
            with subcol2:
                if st.button("LOG IN", key="login_link", type="secondary", use_container_width=True):
                    st.session_state.page = "profile"
                    st.session_state.auth_mode = 0
                    st.rerun()
    else:
        st.markdown(f"""
        <div style='
            background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
            padding: 30px;
            border-radius: 15px;
            text-align: center;
            margin: 60px auto 40px auto;
            max-width: 600px;
            box-shadow: 0 8px 25px rgba(168, 237, 234, 0.3);
        '>
            <p style='
                font-family: "Oswald", sans-serif;
                font-size: 24px;
                color: #1a1a2e;
                margin: 0;
                font-weight: 600;
            '>✨ Welcome back, {st.session_state.user}!</p>
        </div>
        """, unsafe_allow_html=True)
    
    # --- FINAL MOTIVATIONAL QUOTE ---
    st.markdown("""
    <div style='
        text-align: center;
        padding: 40px;
        margin: 40px 0;
    '>
        <p style='
            font-family: "Playfair Display", serif;
            font-size: 28px;
            color: #667eea;
            font-style: italic;
            margin: 0;
            line-height: 1.5;
        '>"Take care of your body. It's the only place you have to live."</p>
        <p style='
            font-family: "Roboto", sans-serif;
            font-size: 14px;
            color: #666;
            margin-top: 15px;
            letter-spacing: 1px;
        '>— Jim Rohn</p>
    </div>
    """, unsafe_allow_html=True)

# ======================================================
# PLANNER HUB (Selection Page)
# ======================================================
elif st.session_state.page == "planner":
    
    st.markdown("<h2 class='section-title' style='text-align: center;'>Choose Your Path</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #555; margin-bottom: 40px;'>Select the type of plan you want to generate today.</p>", unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)

    # --- WORKOUT PLAN CARD ---
    with c1:
        # Display workout image from assets folder
        try:
            st.image("assets/workout.png", use_container_width=True)
        except:
            try:
                st.image("assets/workout.jpg", use_container_width=True)
            except:
                # Fallback to emoji if image not found
                st.markdown("""
                <div class="selection-card">
                    <div class="card-icon">🏋️</div>
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="selection-card" style="margin-top: -20px;">
            <div class="card-title">Workout<br>Plan</div>
            <div class="card-desc">
                Generate a personalized weekly exercise routine based on your fitness goals.
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("CREATE WORKOUT", key="btn_workout_plan", type="primary", use_container_width=True):
            st.session_state.page = "scheduler"
            st.rerun()

    # --- DIET PLAN CARD ---
    with c2:
        # Display diet plan image from assets folder
        try:
            st.image("assets/dietplan1.png", use_container_width=True)
        except:
            try:
                st.image("assets/dietplan1.jpg", use_container_width=True)
            except:
                # Fallback to emoji if image not found
                st.markdown("""
                <div class="selection-card">
                    <div class="card-icon">🥗</div>
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="selection-card" style="margin-top: -20px;">
            <div class="card-title">Diet<br>Plan</div>
            <div class="card-desc">
                Get a customized meal plan tailored to your nutritional needs.
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("CREATE DIET", key="btn_diet_plan", type="primary", use_container_width=True):
            st.session_state.page = "diet"
            st.rerun()
            
    # --- MENTAL HEALTH CARD ---
    with c3:
        # Display mental health image from assets folder
        try:
            st.image("assets/mental2.png", use_container_width=True)
        except:
            try:
                st.image("assets/mental2.jpg", use_container_width=True)
            except:
                # Fallback to emoji if image not found
                st.markdown("""
                <div class="selection-card">
                    <div class="card-icon">🧠</div>
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="selection-card" style="margin-top: -20px;">
            <div class="card-title">Mental<br>Wellness</div>
            <div class="card-desc">
                Track mood, manage stress, and find clarity with guided tools.
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("OPEN MIND SPACE", key="btn_mental_plan", type="primary", use_container_width=True):
            st.session_state.page = "mental"
            st.rerun()


# ======================================================
# WORKOUT SCHEDULER (AI UPGRADED)
# ======================================================
# ======================================================
# WORKOUT SCHEDULER (AI UPGRADED & LOOP FIXED)
# ======================================================
elif st.session_state.page == "scheduler":

    # Load and display background image
    import base64
    from pathlib import Path
    
    def get_base64_image(image_path):
        """Convert image to base64 for CSS background"""
        try:
            with open(image_path, "rb") as img_file:
                return base64.b64encode(img_file.read()).decode()
        except:
            return None
    
    # Try to load the workout image
    bg_image = None
    for ext in ['.png', '.jpg', '.jpeg']:
        img_path = Path(f"assets/workout{ext}")
        if img_path.exists():
            bg_image = get_base64_image(img_path)
            break
    
    # Apply background styling if image is found
    if bg_image:
        st.markdown(f"""
        <style>
        .stApp {{
            background-image: url("data:image/png;base64,{bg_image}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        
        /* Dark overlay for better readability */
        .main .block-container {{
            background-color: rgba(0, 0, 0, 0.75);
            padding: 2rem;
            border-radius: 10px;
        }}
        
        /* MAKE ROUTINEX BRAND WHITE */
        .brand {{
            color: #FFFFFF !important;
        }}
        
        .tagline {{
            color: #FFFFFF !important;
        }}
        
        /* ALL TEXT WHITE AND BOLD */
        .stMarkdown, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3, .stMarkdown h4, .stMarkdown h5, .stMarkdown h6, .stMarkdown p, .stMarkdown li, .stMarkdown span, .stText {{
            color: #FFFFFF !important;
            font-weight: bold !important;
        }}
        
        /* Navigation buttons white */
        div.stButton > button[kind="secondary"] {{
            color: #FFFFFF !important;
            background-color: transparent !important;
            border: 2px solid #FFFFFF !important;
            font-weight: bold !important;
        }}
        
        div.stButton > button[kind="secondary"]:hover {{
            background-color: rgba(255, 255, 255, 0.2) !important;
            color: #FFFFFF !important;
        }}
        
        /* Primary buttons - keep black background but white when hovered */
        div.stButton > button[kind="primary"] {{
            background-color: #FFFFFF !important;
            color: #000000 !important;
            font-weight: bold !important;
        }}
        
        div.stButton > button[kind="primary"]:hover {{
            background-color: #CCCCCC !important;
        }}
        
        /* Form submit button */
        div[data-testid="stFormSubmitButton"] > button {{
            background-color: #FFFFFF !important;
            color: #000000 !important;
            font-weight: bold !important;
        }}
        
        /* Labels white and bold */
        label, .stNumberInput label, .stSelectbox label, .stSlider label, .stMultiSelect label, .stTextArea label, .stTextInput label {{
            color: #FFFFFF !important;
            font-weight: bold !important;
        }}
        
        /* MAKE INPUT FIELDS MORE COMPACT */
        .stNumberInput {{
            max-width: 300px !important;
        }}
        
        .stSelectbox {{
            max-width: 300px !important;
        }}
        
        .stMultiSelect {{
            max-width: 400px !important;
        }}
        
        .stTextArea {{
            max-width: 600px !important;
        }}
        
        /* Info/Alert boxes */
        .stAlert {{
            background-color: rgba(255, 255, 255, 0.2) !important;
            border: 2px solid #FFFFFF !important;
        }}
        
        .stAlert p, .stAlert div {{
            color: #FFFFFF !important;
            font-weight: bold !important;
        }}
        
        /* Dividers */
        hr {{
            border-color: rgba(255, 255, 255, 0.5) !important;
        }}
        
        /* Expander text white */
        div[data-testid="stExpander"] {{
            background-color: rgba(0, 0, 0, 0.5) !important;
            border: 1px solid #FFFFFF !important;
        }}
        
        div[data-testid="stExpander"] details summary p {{
            color: #FFFFFF !important;
            font-weight: bold !important;
        }}
        
        div[data-testid="stExpander"] details[open] {{
            background-color: rgba(0, 0, 0, 0.7) !important;
        }}
        
        /* Success/Error/Warning messages */
        .stSuccess, .stSuccess p {{
            color: #FFFFFF !important;
            background-color: rgba(40, 167, 69, 0.8) !important;
            font-weight: bold !important;
        }}
        
        .stError, .stError p {{
            color: #FFFFFF !important;
            background-color: rgba(220, 53, 69, 0.8) !important;
            font-weight: bold !important;
        }}
        
        .stWarning, .stWarning p {{
            color: #FFFFFF !important;
            background-color: rgba(255, 193, 7, 0.8) !important;
            font-weight: bold !important;
        }}
        
        /* Radio and checkbox labels */
        div[role="radiogroup"] p, div[role="radiogroup"] div, div[role="radiogroup"] label {{
            color: #FFFFFF !important;
            font-weight: bold !important;
        }}
        
        /* Caption text */
        .stCaption, .stCaption p {{
            color: #FFFFFF !important;
            font-weight: bold !important;
        }}
        
        /* Spinner text */
        .stSpinner > div {{
            color: #FFFFFF !important;
        }}
        
        /* Slider labels and values */
        .stSlider p {{
            color: #FFFFFF !important;
            font-weight: bold !important;
        }}
        
        /* Input field placeholder and text - keep as is for readability */
        .stNumberInput input, .stSelectbox div[data-baseweb="select"], div[data-baseweb="input"] > input, .stTextArea textarea {{
            color: #FFFFFF !important;
            background-color: rgba(38, 39, 48, 0.9) !important;
            border: 1px solid #FFFFFF !important;
        }}
        
        /* Dropdown menu items */
        ul[data-baseweb="menu"] li {{
            color: #FFFFFF !important;
            background-color: #262730 !important;
        }}
        
        /* Tab styling - make white */
        button[data-baseweb="tab"] {{
            color: #CCCCCC !important;
        }}
        
        button[data-baseweb="tab"][aria-selected="true"] {{
            color: #FFFFFF !important;
            border-bottom: 3px solid #FFFFFF !important;
            font-weight: 700 !important;
        }}
        </style>
        """, unsafe_allow_html=True)

    # --- Header ---
    c_back, c_void = st.columns([1, 4]) 
    with c_back:
        if st.button("← BACK", use_container_width=True):
            st.session_state.page = "planner"
            st.rerun()

    st.markdown("## 🏋️ AI Workout Creator")
    st.info("Define your timeline. The AI will generate a unique plan for every single week.")

    # --- Input Form ---
    with st.form("fitness_form"):
        c1, c2 = st.columns(2)

        with c1:
            age = st.number_input("Age", 10, 90, 25)
            weight = st.number_input("Weight (kg)", 30.0, 200.0, 70.0)
            goal = st.selectbox(
                "Goal",
                ["Fat Loss", "Muscle Gain", "Strength", "Endurance", "Flexibility"]
            )
            experience = st.selectbox("Experience Level", ["Beginner", "Intermediate", "Advanced"])
            gender = st.selectbox("Gender", ["Male", "Female", "Other"])

        with c2:
            height = st.number_input("Height (cm)", 100.0, 250.0, 170.0)
            available_days = st.slider("Days/Week Available", 1, 7, 4)
            
            # --- Duration Slider ---
            # Note: 3 months will now trigger 3 separate AI calls to ensure detail
            duration_months = st.slider("Duration (Months)", 1, 12, 3)
            
            medical_conditions = st.multiselect("Medical Conditions", ["Diabetes", "Hypertension", "Asthma", "Back Pain", "None"], default=["None"])
            injuries = st.multiselect("Injuries", ["Knee", "Shoulder", "Lower Back", "None"], default=["None"])

        st.markdown("---")
        additional_info = st.text_area(
            "Additional Preferences", 
            placeholder="E.g., 'I have a home gym', 'I prefer swimming', 'I want to focus on legs'..."
        )

        generate_btn = st.form_submit_button("GENERATE DETAILED PLAN", type="primary", use_container_width=True)

    # --- Generation Logic ---
    if generate_btn:
        profile = {
            "age": age, "weight": weight, "height": height,
            "experience": experience, "gender": gender,
            "available_days": available_days,
            "medical_conditions": [m for m in medical_conditions if m != "None"],
            "injuries": [i for i in injuries if i != "None"]
        }

        # Progress Indicator (Since we loop per month, it might take a few seconds)
        with st.spinner(f"Generating {duration_months} months of workouts (Designing week by week)..."):
            plan_data = generate_workout_plan(profile, goal, duration_months, additional_info)

        if "error" in plan_data:
            st.error(plan_data["error"])
        else:
            st.session_state['latest_schedule'] = plan_data
            st.success(f"Success! Generated {len(plan_data.get('schedule', []))} weeks of training.")
            
            # --- ACTIVATION BUTTON FOR DAILY CHECK-IN ---
            if st.session_state.user:
                st.markdown("---")
                col1, col2, col3 = st.columns([1, 2, 1])
                with col2:
                    st.info("💡 Activate this workout to track your daily progress in Mental Health > Daily Check-in")
                    if st.button("✅ ACTIVATE FOR DAILY CHECK-IN", type="primary", use_container_width=True):
                        # Save workout for check-in tracking
                        save_workout_for_checkin(
                            username=st.session_state.user,
                            workout_data=plan_data,
                            plan_name=f"{goal} - {duration_months} months",
                            duration_weeks=len(plan_data.get('schedule', []))
                        )
                        st.success("🎉 Workout activated! Go to Mental Health > Daily Check-in to track your progress.")
                        time.sleep(2)
                        st.rerun()
            else:
                st.warning("⚠️ Please log in to activate this workout for daily tracking")

    # --- Display Logic (Smart Monthly Grouping) ---
    if 'latest_schedule' in st.session_state and "error" not in st.session_state['latest_schedule']:
        data = st.session_state['latest_schedule']
        schedule = data.get("schedule", [])
        
        st.subheader("📋 Your Master Plan")
        st.caption(data.get('summary', ''))

        if not schedule:
            st.warning("No schedule data generated.")
        else:
            # Calculate how many months we need to display based on total weeks
            import math
            # Assuming roughly 4 weeks per month for display purposes
            num_display_months = math.ceil(len(schedule) / 4)
            
            # Create the Horizontal Tabs
            tabs = st.tabs([f"Month {i+1}" for i in range(num_display_months)])

            # Fill each tab
            for i, tab in enumerate(tabs):
                with tab:
                    # Slice the master list for this month (e.g., 0-4, 4-8)
                    start_idx = i * 4
                    end_idx = start_idx + 4
                    month_weeks = schedule[start_idx:end_idx]

                    if not month_weeks:
                        st.info("End of schedule.")
                    
                    for week in month_weeks:
                        week_num = week.get("week_number", "?")
                        focus = week.get("focus", "General Training")
                        
                        # Expandable Week
                        with st.expander(f"📅 Week {week_num}: {focus}", expanded=False):
                            workouts = week.get("workouts", [])
                            for day in workouts:
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

# ======================================================
# DIET PLAN PAGE (AI Powered)
# ======================================================
elif st.session_state.page == "diet":
    
    # Load and display background image
    import base64
    from pathlib import Path
    
    def get_base64_image(image_path):
        """Convert image to base64 for CSS background"""
        try:
            with open(image_path, "rb") as img_file:
                return base64.b64encode(img_file.read()).decode()
        except:
            return None
    
    # Try to load the dietplan image
    bg_image = None
    for ext in ['.png', '.jpg', '.jpeg']:
        img_path = Path(f"assets/dietplan{ext}")
        if img_path.exists():
            bg_image = get_base64_image(img_path)
            break
    
    # Apply background styling if image is found
    if bg_image:
        st.markdown(f"""
        <style>
        .stApp {{
            background-image: url("data:image/png;base64,{bg_image}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        
        /* Dark overlay for better readability */
        .main .block-container {{
            background-color: rgba(0, 0, 0, 0.75);
            padding: 2rem;
            border-radius: 10px;
        }}
        
        /* MAKE ROUTINEX BRAND WHITE */
        .brand {{
            color: #FFFFFF !important;
        }}
        
        .tagline {{
            color: #FFFFFF !important;
        }}
        
        /* ALL TEXT WHITE AND BOLD */
        .stMarkdown, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3, .stMarkdown h4, .stMarkdown h5, .stMarkdown h6, .stMarkdown p, .stMarkdown li, .stMarkdown span, .stText {{
            color: #FFFFFF !important;
            font-weight: bold !important;
        }}
        
        /* Navigation buttons white */
        div.stButton > button[kind="secondary"] {{
            color: #FFFFFF !important;
            background-color: transparent !important;
            border: 2px solid #FFFFFF !important;
            font-weight: bold !important;
        }}
        
        div.stButton > button[kind="secondary"]:hover {{
            background-color: rgba(255, 255, 255, 0.2) !important;
            color: #FFFFFF !important;
        }}
        
        /* Primary buttons */
        div.stButton > button[kind="primary"] {{
            background-color: #FFFFFF !important;
            color: #000000 !important;
            font-weight: bold !important;
        }}
        
        div.stButton > button[kind="primary"]:hover {{
            background-color: #CCCCCC !important;
        }}
        
        /* Form submit button */
        div[data-testid="stFormSubmitButton"] > button {{
            background-color: #FFFFFF !important;
            color: #000000 !important;
            font-weight: bold !important;
        }}
        
        /* Labels white and bold */
        label, .stNumberInput label, .stSelectbox label, .stSlider label, .stMultiSelect label, .stTextArea label, .stTextInput label, .stRadio label {{
            color: #FFFFFF !important;
            font-weight: bold !important;
        }}
        
        /* MAKE INPUT FIELDS MORE COMPACT */
        .stNumberInput {{
            max-width: 300px !important;
        }}
        
        .stSelectbox {{
            max-width: 300px !important;
        }}
        
        .stMultiSelect {{
            max-width: 400px !important;
        }}
        
        .stTextInput {{
            max-width: 400px !important;
        }}
        
        /* Info/Alert boxes */
        .stAlert {{
            background-color: rgba(255, 255, 255, 0.2) !important;
            border: 2px solid #FFFFFF !important;
        }}
        
        .stAlert p, .stAlert div {{
            color: #FFFFFF !important;
            font-weight: bold !important;
        }}
        
        /* Dividers */
        hr {{
            border-color: rgba(255, 255, 255, 0.5) !important;
        }}
        
        /* Success/Error/Warning messages */
        .stSuccess, .stSuccess p {{
            color: #FFFFFF !important;
            background-color: rgba(40, 167, 69, 0.8) !important;
            font-weight: bold !important;
        }}
        
        .stError, .stError p {{
            color: #FFFFFF !important;
            background-color: rgba(220, 53, 69, 0.8) !important;
            font-weight: bold !important;
        }}
        
        .stWarning, .stWarning p {{
            color: #FFFFFF !important;
            background-color: rgba(255, 193, 7, 0.8) !important;
            font-weight: bold !important;
        }}
        
        /* Radio buttons */
        div[role="radiogroup"] p, div[role="radiogroup"] div, div[role="radiogroup"] label {{
            color: #FFFFFF !important;
            font-weight: bold !important;
        }}
        
        /* Caption text */
        .stCaption, .stCaption p {{
            color: #FFFFFF !important;
            font-weight: bold !important;
        }}
        
        /* Spinner text */
        .stSpinner > div {{
            color: #FFFFFF !important;
        }}
        
        /* Slider labels and values */
        .stSlider p {{
            color: #FFFFFF !important;
            font-weight: bold !important;
        }}
        
        /* Input fields */
        .stNumberInput input, .stSelectbox div[data-baseweb="select"], div[data-baseweb="input"] > input, .stTextArea textarea {{
            color: #FFFFFF !important;
            background-color: rgba(38, 39, 48, 0.9) !important;
            border: 1px solid #FFFFFF !important;
        }}
        
        /* Dropdown menu items */
        ul[data-baseweb="menu"] li {{
            color: #FFFFFF !important;
            background-color: #262730 !important;
        }}
        
        /* Plan card styling for diet results */
        .plan-card {{
            background-color: rgba(0, 0, 0, 0.6) !important;
            border: 1px solid #FFFFFF !important;
            padding: 20px !important;
            border-radius: 8px !important;
            margin-bottom: 15px !important;
        }}
        
        .meal-header {{
            background-color: rgba(255, 255, 255, 0.2) !important;
            border-left: 5px solid #FFFFFF !important;
        }}
        
        .meal-title {{
            color: #FFFFFF !important;
        }}
        
        .food-item {{
            color: #FFFFFF !important;
            border-bottom: 1px solid rgba(255, 255, 255, 0.3) !important;
        }}
        
        .food-item b {{
            color: #FFFFFF !important;
        }}
        
        .food-item span, .food-item i {{
            color: #DDDDDD !important;
        }}
        </style>
        """, unsafe_allow_html=True)
    
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
        nutri_profile = {
            "weight_kg": d_weight,
            "height_cm": d_height,
            "age": d_age,
            "gender": d_gender
        }
        
        gen_profile = {
            "diet_type": d_type,
            "cuisine": d_cuisine,
            "region": d_cuisine,
            "allergies": [] if "None" in d_allergies else d_allergies,
            "meals_per_day": d_meals
        }

        with st.spinner("Calculating nutritional needs..."):
            targets = calculate_nutritional_needs(nutri_profile, d_goal, d_activity)
            st.success(f"Targets: {targets['calories']} kcal | P: {targets['macros']['protein']}g | C: {targets['macros']['carbs']}g | F: {targets['macros']['fats']}g")

        with st.spinner("AI Chef is crafting your menu..."):
            diet_plan = generate_diet_plan(targets, gen_profile)
        
        if "error" in diet_plan:
            st.error(diet_plan["error"])
            st.error(diet_plan.get("details", ""))
        else:
            st.session_state['latest_diet_plan'] = diet_plan
            
            summary = diet_plan.get("summary", {})
            st.markdown(f"### Plan Summary")
            st.info(f"{summary.get('note', 'Here is your personalized plan.')}")
            
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
# MENTAL HEALTH PAGE (NEW)
# ======================================================
elif st.session_state.page == "mental":
    render_mental_health_page()

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
        
        st.markdown("---")
        
        # --- TABBED INTERFACE ---
        tab1, tab2, tab3, tab4 = st.tabs(["📋 Diet Plans", "💪 Workouts", "📝 Canvas Entries", "🏆 Daily Wins"])
        
        # TAB 1: DIET PLANS (existing functionality)
        with tab1:
            st.markdown("### Your Saved Diet Plans")
            saved_plans = get_user_plans(st.session_state.user)
            
            if not saved_plans:
                st.info("You don't have any saved diet plans yet. Go to Diet Planner to create one!")
            else:
                for idx, item in enumerate(saved_plans):
                    plan_id = item.get("id")
                    
                    with st.expander(f"Plan created on {item['created_at']}"):
                        # Delete button
                        col_del_1, col_del_2 = st.columns([6, 1])
                        with col_del_2:
                            if st.button("DELETE", key=f"del_{plan_id}", type="primary"):
                                delete_plan(plan_id)
                                st.rerun()
                        
                        plan = item['plan']
                        
                        if isinstance(plan, dict) and "meals" in plan:
                            # DIET PLAN RENDERER
                            st.caption("🥗 NUTRITION PLAN")
                            summary = plan.get("summary", {})
                            
                            plan_html = "<div class='plan-card'>"
                            plan_html += f"<p><strong>Goal:</strong> {summary.get('total_calories')} kcal | P: {summary.get('protein')}g</p><hr>"
                            
                            for meal in plan.get("meals", []):
                                plan_html += f"<h3>{meal.get('meal_name')}</h3><ul>"
                                for food in meal.get("food_items", []):
                                    item_food = food.get('item')
                                    qty = food.get('quantity')
                                    plan_html += f"<li><strong>{item_food}</strong> ({qty})</li>"
                                plan_html += "</ul><br>"
                            plan_html += "</div>"
                            
                            st.markdown(plan_html, unsafe_allow_html=True)
                        else:
                            st.info("This plan format is not a diet plan")
        
        # TAB 2: WORKOUTS (NEW)
        with tab2:
            st.markdown("### Your Active Workout")
            active_workout = get_active_workout(st.session_state.user)
            
            if not active_workout:
                st.info("No active workout. Generate a workout plan and activate it for daily check-in tracking!")
            else:
                st.success(f"✅ **{active_workout['plan_name']}**")
                st.caption(f"Activated on: {active_workout['created_at']}")
                st.caption(f"Duration: {active_workout['duration_weeks']} weeks")
                
                # Display the workout schedule
                workout_data = active_workout['workout_data']
                schedule = workout_data.get('schedule', [])
                
                if schedule:
                    st.markdown("#### 📋 Your Schedule")
                    
                    import math
                    num_display_months = math.ceil(len(schedule) / 4)
                    tabs = st.tabs([f"Month {i+1}" for i in range(num_display_months)])
                    
                    for i, tab in enumerate(tabs):
                        with tab:
                            start_idx = i * 4
                            end_idx = start_idx + 4
                            month_weeks = schedule[start_idx:end_idx]
                            
                            for week in month_weeks:
                                week_num = week.get("week_number", "?")
                                focus = week.get("focus", "General Training")
                                
                                with st.expander(f"📅 Week {week_num}: {focus}", expanded=False):
                                    workouts = week.get("workouts", [])
                                    for day in workouts:
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
        
        # TAB 3: CANVAS ENTRIES (NEW)
        with tab3:
            st.markdown("### 📝 Your Journal Entries")
            entries = get_canvas_entries(st.session_state.user, limit=20)
            
            if not entries:
                st.info("No journal entries yet. Visit Mental Health > Mind Reset to write your thoughts!")
            else:
                for entry in entries:
                    with st.expander(f"📖 {entry['created_at']} - {entry.get('mood', 'No mood')}"):
                        st.write(entry['content'])
                        
                        col1, col2 = st.columns([5, 1])
                        with col2:
                            if st.button("🗑️", key=f"del_canvas_{entry['id']}"):
                                delete_canvas_entry(entry['id'])
                                st.rerun()
        
        # TAB 4: WINS (NEW)
        with tab4:
            st.markdown("### 💎 Daily Wins")
            wins = get_wins(st.session_state.user, limit=20)
            
            if not wins:
                st.info("No wins logged yet. Visit Mental Health > Mind Reset to log your daily wins!")
            else:
                for win in wins:
                    with st.expander(f"🏆 {win['created_at']}"):
                        if win['win1']:
                            st.markdown(f"**1.** {win['win1']}")
                        if win['win2']:
                            st.markdown(f"**2.** {win['win2']}")
                        if win['win3']:
                            st.markdown(f"**3.** {win['win3']}")
                        
                        col1, col2 = st.columns([5, 1])
                        with col2:
                            if st.button("🗑️", key=f"del_win_{win['id']}"):
                                delete_wins(win['id'])
                                st.rerun()
    
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