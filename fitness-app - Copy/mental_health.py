import streamlit as st
import time
import os

# --- IMPORTS ---
from agent_interface import show_agent_page
from daily_checkin import show_daily_checkin

def render_mental_health_page():
    # --------------------------------------------------------
    # 1. STATE MANAGEMENT
    # --------------------------------------------------------
    if "mental_view" not in st.session_state:
        st.session_state.mental_view = "home"

    # --------------------------------------------------------
    # 2. CSS STYLING (Global Index Strategy)
    # --------------------------------------------------------
    st.markdown("""
    <style>
    /* 1. Base Button Styling (Rounded, Shadow, Big Text) */
    div.stButton > button {
        width: 100%;
        height: 70px;
        border-radius: 15px;
        border: none;
        font-size: 20px;
        font-weight: 700;
        color: #2c3e50; /* Dark text */
        margin-bottom: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        transition: transform 0.1s;
    }
    div.stButton > button:hover {
        transform: scale(1.02);
    }
    
    /* 2. THE COLOR FIX */
    /* We target the buttons by their Order on the screen. */
    
    /* Button #1 is "Back to Planner" -> Make it transparent */
    div.stButton:nth-of-type(1) > button {
        background-color: transparent !important;
        border: 1px solid #ddd !important;
        color: #888 !important;
        height: auto !important;
        font-size: 14px !important;
        box-shadow: none !important;
    }

    /* Button #2: Daily Check-in -> PURPLE */
    div.stButton:nth-of-type(2) > button {
        background-color: #E0BBE4 !important; /* Lavender */
        border-left: 10px solid #957dad !important;
    }

    /* Button #3: Breathing -> YELLOW */
    div.stButton:nth-of-type(3) > button {
        background-color: #FFF2CC !important; /* Pastel Yellow */
        border-left: 10px solid #e3cf86 !important;
    }

    /* Button #4: Mind Reset -> TEAL/GREEN */
    div.stButton:nth-of-type(4) > button {
        background-color: #a8d5ba !important; /* Sage */
        border-left: 10px solid #7eb592 !important;
    }

    /* Button #5: Talk -> PINK */
    div.stButton:nth-of-type(5) > button {
        background-color: #FFC1CC !important; /* Pink */
        border-left: 10px solid #d48593 !important;
    }
    </style>
    """, unsafe_allow_html=True)

    # --------------------------------------------------------
    # 3. HOME VIEW (The Menu)
    # --------------------------------------------------------
    if st.session_state.mental_view == "home":
        # 1. Back Button (Global Index 1)
        c_back, c_void = st.columns([1, 4]) 
        with c_back:
            if st.button("← BACK TO PLANNER", key="nav_back"):
                st.session_state.page = "planner"
                st.rerun()

        col_left, col_right = st.columns([1, 1], gap="large")

        with col_left:
            st.markdown("""
            <div style="margin-bottom: 20px;">
                <h1 style="font-size: 48px; color: #333; margin: 0;">Mental Health<br>Matters</h1>
                <p style="font-size: 18px; color: #666;">Select a tool below.</p>
            </div>
            """, unsafe_allow_html=True)
            
            # 2. Daily Check-in (Global Index 2)
            if st.button("Daily check-in", key="btn_checkin", use_container_width=True):
                st.session_state.mental_view = "checkin"
                st.rerun()
            
            # 3. Breathing (Global Index 3)
            if st.button("Breathing & calm", key="btn_breath", use_container_width=True):
                st.session_state.mental_view = "breathing"
                st.rerun()
            
            # 4. Mind Reset (Global Index 4)
            if st.button("Mind Reset", key="btn_reset", use_container_width=True):
                st.session_state.mental_view = "reset"
                st.rerun()

            # 5. Talk (Global Index 5)
            if st.button("Talk to AI", key="btn_talk", use_container_width=True):
                st.session_state.mental_view = "talk"
                st.rerun()

        with col_right:
            if os.path.exists("assets/mental_health.png"):
                st.image("assets/mental_health.png", use_container_width=True)
            elif os.path.exists("assets/hero.png"):
                st.image("assets/hero.png", use_container_width=True)

    # --------------------------------------------------------
    # 4. SUB-PAGES
    # --------------------------------------------------------
    else:
        # Simple Back Button for sub-pages
        if st.button("← MENU", key="sub_nav_back"):
            st.session_state.mental_view = "home"
            st.rerun()
        
        st.divider()

        # --- VIEW: DAILY CHECK-IN ---
        if st.session_state.mental_view == "checkin":
            show_daily_checkin()

        # --- VIEW: BREATHING (INTEGRATED) ---
        elif st.session_state.mental_view == "breathing":
            # This block dynamically runs your breathetab.py file
            file_path = "breathetab.py"
            
            if os.path.exists(file_path):
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        file_content = f.read()
                        
                    # We must remove 'st.set_page_config' because it can only be run once per app
                    file_content = file_content.replace("st.set_page_config", "# st.set_page_config")
                    
                    # Execute the code from breathetab.py inside this script
                    exec(file_content, globals())
                    
                except Exception as e:
                    st.error(f"Error loading breathing exercise: {e}")
            else:
                st.error(f"Could not find {file_path}. Please make sure it is in the same folder.")

        # --- VIEW: MIND RESET ---
        elif st.session_state.mental_view == "reset":
            file_path = "tab_mind_reset.py"
            
            if os.path.exists(file_path):
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        file_content = f.read()
                    
                    # 1. Remove set_page_config (it causes error if run twice)
                    file_content = file_content.replace("st.set_page_config", "# st.set_page_config")
                    
                    # 2. Execute the file definitions
                    exec(file_content, globals())
                    
                    # 3. Explicitly call the main function from that file
                    # We check if 'render_app' exists in globals after the exec
                    if "render_app" in globals():
                        globals()["render_app"]()
                    else:
                        st.error("Could not find 'render_app()' in tab_mind_reset.py")
                        
                except Exception as e:
                    st.error(f"Error loading Mind Reset: {e}")
            else:
                st.error(f"Could not find {file_path}. Please make sure it is in the same folder.")

        # --- VIEW: TALK ---
        elif st.session_state.mental_view == "talk":
            show_agent_page()