import streamlit as st
from engine.scheduler import create_weekly_schedule

# ----------------------------
# Page config
# ----------------------------
st.set_page_config(
    page_title="My Fitness AI Planner",
    page_icon="💪",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ----------------------------
# Custom CSS for aesthetic fonts and colors
# ----------------------------
st.markdown("""
<style>
/* Fonts and headings */
h1, h2, h3, h4 {
    font-family: 'Helvetica Neue', sans-serif;
}
body {
    background-color: #fdf6f0;
    color: #333333;
    font-family: 'Helvetica Neue', sans-serif;
}

/* Button style */
.stButton>button {
    background-color: #A3D2CA;
    color: #1B4332;
    font-weight: bold;
    border-radius: 10px;
    padding: 0.6em 1.2em;
    font-size: 16px;
}
.stButton>button:hover {
    background-color: #99c1b9;
}

/* Card-like container for plan */
.plan-card {
    background-color: #fff7f0; /* pastel peach */
    padding: 20px;
    margin-bottom: 18px;
    border-radius: 16px;
    box-shadow: 0 6px 12px rgba(0,0,0,0.08);
    border: 1px solid #f1e2d8;
}

/* Day heading */
.plan-card h3 {
    color: #2d2a26;           /* dark charcoal */
    font-size: 20px;
    font-weight: 700;
    margin-bottom: 12px;
    font-family: 'Inter', 'Segoe UI', sans-serif;
}

/* Exercise text */
.plan-card p,
.plan-card li {
    color: #3f3f46;           /* soft dark gray */
    font-size: 15px;
    line-height: 1.6;
    font-family: 'Inter', 'Segoe UI', sans-serif;
}
</style>
""", unsafe_allow_html=True)

# ----------------------------
# Navigation
# ----------------------------
pages = ["Home", "Generate Schedule"]
selected_page = st.sidebar.selectbox("Navigation", pages)

# ----------------------------
# Home Page
# ----------------------------
if selected_page == "Home":
    st.markdown("<h1 style='text-align:center; color:#1B4332;'>Welcome to Your 2026 Fitness Journey! 💪</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align:center; color:#333;'>Let's design your perfect weekly fitness plan personalized just for YOU. No guesswork — just safe, effective exercises based on your goal, experience, and health!</h3>", unsafe_allow_html=True)
    
    st.markdown("<div style='text-align:center; margin-top:30px;'>", unsafe_allow_html=True)
    if st.button("Let's Get Your Dream Schedule"):
        st.session_state.goto_form = True
    st.markdown("</div>", unsafe_allow_html=True)
    
# ----------------------------
# Generate Schedule Page
# ----------------------------
if selected_page == "Generate Schedule" or st.session_state.get("goto_form", False):

    st.markdown("<h2 style='text-align:center; color:#1B4332;'>Personalize Your Weekly Fitness Plan</h2>", unsafe_allow_html=True)

    # ----------------------------
    # User Inputs
    # ----------------------------
    with st.form("fitness_form"):
        col1, col2 = st.columns(2)

        with col1:
            goal = st.selectbox("Select Your Goal", ["muscle_gain", "fat_loss", "general_fitness", "endurance", "mobility_flexibility"])
            experience = st.selectbox("Experience Level", ["beginner", "intermediate", "advanced"])
            available_days = st.slider("Days per week", 3, 6, 5)
        
        with col2:
            medical_conditions = st.multiselect(
                "Medical Conditions (if any)",
                ["cardiac", "diabetes", "joint_issues", "asthma", "obesity_related", "hypertension", "none"]
            )
            injuries = st.multiselect(
                "Injuries (if any)",
                ["knee", "shoulder", "back", "ankle", "none"]
            )

        submitted = st.form_submit_button("Generate My Schedule")
    
    # ----------------------------
    # Generate & Display Plan
    # ----------------------------
    if submitted:
        # Clean "none" selections
        medical_conditions = [] if "none" in medical_conditions else medical_conditions
        injuries = [] if "none" in injuries else injuries

        schedule = create_weekly_schedule(goal, experience, medical_conditions, injuries, available_days)

        st.success("Here is your personalized weekly schedule!")

        for i, day in enumerate(schedule, 1):
            st.markdown(
                f"<div class='plan-card'><h3>Day {i}: {day['day_type'].capitalize()}</h3>",
                unsafe_allow_html=True
            )

            if not day["exercises"]:
                st.markdown("  - No exercises (all filtered for safety)")
            else:
                for ex in day["exercises"]:
                    if isinstance(ex, dict):
                        name = ex.get("name", "Exercise")
                        sets = ex.get("sets", "-")
                        reps = ex.get("reps", ex.get("time", "-"))
                    else:
                        # ex is a string (cardio / mobility / fallback)
                        name = ex
                        sets = "-"
                        reps = "-"

                    st.markdown(
                        f"  - **{name}** | Sets: {sets}, Reps/Time: {reps}"
                    )

            st.markdown("</div>", unsafe_allow_html=True)


