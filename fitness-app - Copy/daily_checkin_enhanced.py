import streamlit as st
from datetime import datetime, timedelta
from database_extended import (
    get_active_workout,
    save_daily_checkin,
    get_daily_checkin,
    get_checkin_history,
    get_streak_count
)

def show_daily_checkin_enhanced():
    """
    Enhanced Daily Check-in with colorful, modern aesthetic
    """
    
    # Hide all Streamlit default elements and code
    st.markdown("""
    <style>
        /* Hide Streamlit branding and code */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        
        /* Modern Gradient Background */
        .stApp {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 25%, #f093fb 50%, #4facfe 75%, #00f2fe 100%);
            background-size: 400% 400%;
            animation: gradientShift 15s ease infinite;
        }
        
        @keyframes gradientShift {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }
        
        /* Main container with glassmorphism */
        .main .block-container {
            background: rgba(255, 255, 255, 0.15);
            backdrop-filter: blur(20px);
            border-radius: 30px;
            padding: 2.5rem;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
            border: 1px solid rgba(255, 255, 255, 0.2);
        }
        
        /* Header styles */
        h1, h2, h3, h4, h5, h6 {
            color: white !important;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.2);
            font-weight: 700 !important;
        }
        
        /* Paragraph text */
        p, div, span, label {
            color: white !important;
            font-weight: 500 !important;
        }
        
        /* Card containers */
        .glass-card {
            background: rgba(255, 255, 255, 0.2);
            border-radius: 20px;
            padding: 25px;
            margin: 15px 0;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.3);
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }
        
        .glass-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 8px 30px rgba(0, 0, 0, 0.15);
        }
        
        /* Buttons */
        .stButton button {
            background: linear-gradient(135deg, #ff6b6b 0%, #ee5a6f 100%) !important;
            color: white !important;
            border: none !important;
            border-radius: 50px !important;
            padding: 15px 40px !important;
            font-size: 18px !important;
            font-weight: 700 !important;
            box-shadow: 0 8px 25px rgba(238, 90, 111, 0.4) !important;
            transition: all 0.3s ease !important;
        }
        
        .stButton button:hover {
            transform: translateY(-3px) !important;
            box-shadow: 0 12px 35px rgba(238, 90, 111, 0.5) !important;
        }
        
        /* Checkboxes */
        [data-testid="stCheckbox"] {
            background: rgba(255, 255, 255, 0.15);
            padding: 15px;
            border-radius: 15px;
            margin: 10px 0;
            backdrop-filter: blur(5px);
            border: 1px solid rgba(255, 255, 255, 0.2);
        }
        
        /* Text input and textarea */
        .stTextInput input, .stTextArea textarea {
            background: rgba(255, 255, 255, 0.2) !important;
            border: 2px solid rgba(255, 255, 255, 0.3) !important;
            border-radius: 15px !important;
            color: white !important;
            font-weight: 500 !important;
        }
        
        .stTextInput input::placeholder, .stTextArea textarea::placeholder {
            color: rgba(255, 255, 255, 0.7) !important;
        }
        
        /* Select slider */
        .stSlider {
            padding: 15px;
            background: rgba(255, 255, 255, 0.15);
            border-radius: 15px;
            backdrop-filter: blur(5px);
        }
        
        /* Expander */
        [data-testid="stExpander"] {
            background: rgba(255, 255, 255, 0.15) !important;
            border-radius: 15px !important;
            border: 1px solid rgba(255, 255, 255, 0.2) !important;
            backdrop-filter: blur(10px) !important;
        }
        
        /* Info, success, warning boxes */
        .stAlert {
            background: rgba(255, 255, 255, 0.2) !important;
            border-radius: 15px !important;
            backdrop-filter: blur(10px) !important;
            border: 1px solid rgba(255, 255, 255, 0.3) !important;
            color: white !important;
        }
        
        /* Dataframe */
        [data-testid="stDataFrame"] {
            background: rgba(255, 255, 255, 0.2) !important;
            border-radius: 15px !important;
            backdrop-filter: blur(10px) !important;
        }
        
        /* Dividers */
        hr {
            border-color: rgba(255, 255, 255, 0.3) !important;
            margin: 30px 0 !important;
        }
        
        /* Hide code blocks */
        .stCodeBlock, pre, code {
            display: none !important;
        }
    </style>
    """, unsafe_allow_html=True)
    
    if not st.session_state.user:
        st.markdown("""
        <div class="glass-card" style="text-align: center;">
            <h2>⚠️ Login Required</h2>
            <p style="font-size: 18px;">Please log in to track your daily progress</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("🔐 Go to Login", type="primary", use_container_width=True):
            st.session_state.page = "profile"
            st.rerun()
        return
    
    username = st.session_state.user
    today = datetime.now().strftime("%Y-%m-%d")
    
    # Load today's check-in data if exists
    existing_checkin = get_daily_checkin(username, today)
    
    # Initialize form state
    if 'checkin_form_data' not in st.session_state or st.session_state.get('checkin_date') != today:
        if existing_checkin:
            st.session_state.checkin_form_data = existing_checkin
        else:
            st.session_state.checkin_form_data = {
                "workout_completed": False,
                "water_intake": False,
                "meditation": False,
                "sleep_quality": 3,
                "notes": ""
            }
        st.session_state.checkin_date = today
    
    # Page Header with animated emoji
    st.markdown("""
    <div style="text-align: center; margin-bottom: 30px;">
        <h1 style="font-size: 3.5rem; margin: 0; animation: float 3s ease-in-out infinite;">📋</h1>
        <h2 style="margin: 10px 0;">Daily Check-In</h2>
        <p style="font-size: 1.2rem; opacity: 0.9;">{}</p>
    </div>
    
    <style>
        @keyframes float {{
            0%, 100% {{ transform: translateY(0px); }}
            50% {{ transform: translateY(-10px); }}
        }}
    </style>
    """.format(datetime.now().strftime('%A, %B %d, %Y')), unsafe_allow_html=True)
    
    # Get data for stats
    streak = get_streak_count(username)
    history = get_checkin_history(username, limit=7)
    
    if history:
        total = len(history) * 3
        completed = sum([
            (1 if h['workout_completed'] else 0) + 
            (1 if h['water_intake'] else 0) + 
            (1 if h['meditation'] else 0)
            for h in history
        ])
        pct = int((completed / total * 100)) if total > 0 else 0
    else:
        pct = 0
    
    status_color = "#4facfe" if existing_checkin else "#feca57"
    status_icon = "✅" if existing_checkin else "📝"
    status_text = "Checked in today!" if existing_checkin else "Not checked in yet"
    
    # Display stats in pure HTML to avoid empty boxes
    st.markdown(f"""
    <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 15px; margin-bottom: 30px;">
        <div class="glass-card" style="text-align: center; background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);">
            <h3 style="margin: 0;">🔥 Streak</h3>
            <p style="font-size: 2.5rem; margin: 10px 0; font-weight: 700;">{streak}</p>
            <p style="margin: 0; font-size: 0.9rem;">day{'s' if streak != 1 else ''}</p>
        </div>
        
        <div class="glass-card" style="text-align: center; background: linear-gradient(135deg, {status_color} 0%, #00f2fe 100%);">
            <h3 style="margin: 0;">{status_icon} Status</h3>
            <p style="font-size: 1.3rem; margin: 10px 0; font-weight: 600;">{status_text}</p>
        </div>
        
        <div class="glass-card" style="text-align: center; background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);">
            <h3 style="margin: 0;">📊 Weekly Rate</h3>
            <p style="font-size: 2.5rem; margin: 10px 0; font-weight: 700;">{pct}%</p>
            <p style="margin: 0; font-size: 0.9rem;">completion</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Active Workout Section
    active_workout = get_active_workout(username)
    
    if active_workout:
        with st.expander("💪 Today's Workout Plan", expanded=True):
            st.markdown(f"**{active_workout['plan_name']}**")
            st.caption(f"Started: {active_workout['created_at'][:10]}")
            
            # Display today's exercises
            workout_data = active_workout['workout_data']
            
            # Calculate which week and day we're in
            start_date = datetime.strptime(active_workout['created_at'][:10], "%Y-%m-%d")
            days_elapsed = (datetime.now() - start_date).days
            week_num = days_elapsed // 7
            day_of_week = datetime.now().weekday()  # 0 = Monday
            
            st.markdown(f"**Week {week_num + 1}, Day {day_of_week + 1}**")
            
            # Try to find today's workout from the schedule
            exercises_found = False
            
            if 'schedule' in workout_data and isinstance(workout_data['schedule'], list):
                # Check if we have data for the current week
                if week_num < len(workout_data['schedule']):
                    week_data = workout_data['schedule'][week_num]
                    
                    # The week_data should have 'workouts' which is a list of daily workouts
                    if isinstance(week_data, dict) and 'workouts' in week_data:
                        workouts = week_data['workouts']
                        
                        # Find today's workout by matching day name
                        day_names = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
                        today_name = day_names[day_of_week]
                        
                        for day_workout in workouts:
                            if isinstance(day_workout, dict):
                                day_key = day_workout.get('day', '').lower()
                                
                                # Match today's day
                                if today_name in day_key:
                                    exercises = day_workout.get('exercises', [])
                                    
                                    if exercises and len(exercises) > 0:
                                        exercises_found = True
                                        st.markdown("**Today's Exercises:**")
                                        for ex in exercises:
                                            # Just display the exercise text
                                            st.markdown(f"• {ex}")
                                    else:
                                        st.info("🌟 Rest day - Recovery is important!")
                                        exercises_found = True
                                    break
            
            if not exercises_found:
                st.info("💡 Check your Profile → Workouts tab to see your full workout schedule!")
    else:
        st.info("💡 **No active workout yet!** Go to Planner → Generate a workout plan, then click 'Activate for Daily Check-in'")
    
    st.markdown("---")
    
    # Daily Habits Check-in
    st.markdown("### ✅ Today's Habits")
    
    # Create two columns for layout
    col1, col2 = st.columns(2)
    
    with col1:
        workout_done = st.checkbox(
            "💪 Completed Workout",
            value=st.session_state.checkin_form_data['workout_completed'],
            key="check_workout"
        )
        
        water = st.checkbox(
            "💧 Drank 8+ Glasses of Water",
            value=st.session_state.checkin_form_data['water_intake'],
            key="check_water"
        )
        
        meditation = st.checkbox(
            "🧘 Meditated (10+ min)",
            value=st.session_state.checkin_form_data['meditation'],
            key="check_meditation"
        )
    
    with col2:
        st.markdown("**😴 Sleep Quality**")
        sleep = st.select_slider(
            "How well did you sleep?",
            options=[1, 2, 3, 4, 5],
            value=st.session_state.checkin_form_data.get('sleep_quality', 3),
            format_func=lambda x: ["😫 Terrible", "😕 Poor", "😐 Okay", "🙂 Good", "😴 Excellent"][x-1],
            label_visibility="collapsed"
        )
        
        # Visual sleep indicator
        sleep_emojis = ["😫", "😕", "😐", "🙂", "😴"]
        st.markdown(f"<div style='text-align: center; font-size: 64px; margin-top: 10px;'>{sleep_emojis[sleep-1]}</div>", 
                   unsafe_allow_html=True)
    
    # Notes
    st.markdown("### 📝 Today's Notes")
    notes = st.text_area(
        "How are you feeling?",
        value=st.session_state.checkin_form_data.get('notes', ''),
        height=120,
        placeholder="Optional: Reflect on your day, note any achievements, or write about challenges...",
        label_visibility="collapsed"
    )
    
    # Save Button
    col_save1, col_save2, col_save3 = st.columns([1, 2, 1])
    with col_save2:
        if st.button("💾 SAVE CHECK-IN", type="primary", use_container_width=True):
            save_daily_checkin(
                username=username,
                date=today,
                workout_done=1 if workout_done else 0,
                water=1 if water else 0,
                meditation=1 if meditation else 0,
                sleep=sleep,
                notes=notes
            )
            
            # Update session state
            st.session_state.checkin_form_data = {
                "workout_completed": workout_done,
                "water_intake": water,
                "meditation": meditation,
                "sleep_quality": sleep,
                "notes": notes
            }
            
            st.success("✅ Check-in saved successfully!")
            st.balloons()
            st.rerun()
    
    # Weekly Progress
    st.markdown("---")
    st.markdown("### 📊 Weekly Progress")
    
    if history:
        # Create a progress table
        import pandas as pd
        
        df_data = []
        for entry in reversed(history):
            df_data.append({
                "Date": entry['date'],
                "💪 Workout": "✅" if entry['workout_completed'] else "❌",
                "💧 Water": "✅" if entry['water_intake'] else "❌",
                "🧘 Meditation": "✅" if entry['meditation'] else "❌",
                "😴 Sleep": ["😫", "😕", "😐", "🙂", "😴"][entry['sleep_quality']-1] if entry['sleep_quality'] else "—"
            })
        
        if df_data:
            df = pd.DataFrame(df_data)
            st.dataframe(df, use_container_width=True, hide_index=True)
            
            # Statistics in HTML to avoid rendering issues
            workout_count = sum([1 for h in history if h['workout_completed']])
            water_count = sum([1 for h in history if h['water_intake']])
            meditation_count = sum([1 for h in history if h['meditation']])
            
            st.markdown(f"""
            <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 15px; margin-top: 20px;">
                <div class="glass-card" style="text-align: center;">
                    <h3>💪 Workouts</h3>
                    <p style="font-size: 2rem; margin: 10px 0;">{workout_count}/{len(history)}</p>
                </div>
                
                <div class="glass-card" style="text-align: center;">
                    <h3>💧 Water</h3>
                    <p style="font-size: 2rem; margin: 10px 0;">{water_count}/{len(history)}</p>
                </div>
                
                <div class="glass-card" style="text-align: center;">
                    <h3>🧘 Meditation</h3>
                    <p style="font-size: 2rem; margin: 10px 0;">{meditation_count}/{len(history)}</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="glass-card" style="text-align: center;">
            <h3>🌱 Start Your Journey</h3>
            <p>Start checking in daily to see your progress here!</p>
            <p style="font-size: 1.2rem; margin-top: 15px;">Your journey begins with the first step. 💪</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Motivational footer
    st.markdown("""
    <div class="glass-card" style="text-align: center; background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%); margin-top: 30px;">
        <p style="margin: 0; font-size: 1.3rem; font-weight: 700;">
            ✨ "The secret of getting ahead is getting started." ✨
        </p>
        <p style="margin-top: 10px; font-size: 1rem; opacity: 0.9;">
            Keep showing up. Consistency is key! 🔑
        </p>
    </div>
    """, unsafe_allow_html=True)