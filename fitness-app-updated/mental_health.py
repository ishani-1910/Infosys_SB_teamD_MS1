import streamlit as st
import time
import os

# --- IMPORTS ---
from agent_interface import show_agent_page
from smart_checkin import show_smart_checkin

def render_mental_health_page():
    # --------------------------------------------------------
    # 1. STATE MANAGEMENT
    # --------------------------------------------------------
    if "mental_view" not in st.session_state:
        st.session_state.mental_view = "home"

    # --------------------------------------------------------
    # 1.5 BACKGROUND IMAGE FOR MENTAL HEALTH PAGE
    # --------------------------------------------------------
    import base64
    from pathlib import Path
    
    def get_base64_image(image_path):
        """Convert image to base64 for CSS background"""
        try:
            with open(image_path, "rb") as img_file:
                return base64.b64encode(img_file.read()).decode()
        except:
            return None
    
    # Try to load the mental health background image
    bg_image = None
    for ext in ['.png', '.jpg', '.jpeg']:
        img_path = Path(f"assets/mental{ext}")
        if img_path.exists():
            bg_image = get_base64_image(img_path)
            break

    # --------------------------------------------------------
    # 2. CSS STYLING (Cheerful Colors + White Bold Text)
    # --------------------------------------------------------
    if bg_image:
        st.markdown(f"""
        <style>
        /* Background Image */
        .stApp {{
            background-image: url("data:image/png;base64,{bg_image}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        
        /* Dark overlay for better readability */
        .main .block-container {{
            background-color: rgba(0, 0, 0, 0.70);
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
        
        /* Base Button Styling - ONLY for mental health feature buttons */
        button[key="btn_checkin"],
        button[key="btn_breath"],
        button[key="btn_reset"],
        button[key="btn_talk"] {{
            width: 100% !important;
            height: 90px !important;
            border-radius: 15px !important;
            font-size: 26px !important;
            font-weight: 600 !important;
            margin-bottom: 15px !important;
            box-shadow: 0 4px 10px rgba(0,0,0,0.25) !important;
            transition: all 0.2s ease !important;
            text-align: left !important;
            padding: 20px !important;
            border: 3px solid rgba(255,255,255,0.7) !important;
        }}
        
        button[key="btn_checkin"]:hover,
        button[key="btn_breath"]:hover,
        button[key="btn_reset"]:hover,
        button[key="btn_talk"]:hover {{
            transform: translateY(-2px) !important;
            box-shadow: 0 6px 14px rgba(0,0,0,0.35) !important;
            border-color: rgba(255,255,255,1) !important;
        }}
        
        /* Back button - Keep simple */
        button[key="nav_back"] {{
            background-color: transparent !important;
            border: 2px solid #FFFFFF !important;
            color: #FFFFFF !important;
            height: 45px !important;
            font-size: 16px !important;
            box-shadow: none !important;
        }}

        /* Daily Check-in - Soft Purple */
        button[key="btn_checkin"] {{
            background-color: #E9D5FF !important;
            background-image: none !important;
            color: #1F1F1F !important;
        }}

        /* Breathing & Calm - Soft Yellow */
        button[key="btn_breath"] {{
            background-color: #FEF3C7 !important;
            background-image: none !important;
            color: #1F1F1F !important;
        }}

        /* Mind Reset - Soft Teal */
        button[key="btn_reset"] {{
            background-color: #A7F3D0 !important;
            background-image: none !important;
            color: #1F1F1F !important;
        }}

        /* Talk to AI - Soft Pink */
        button[key="btn_talk"] {{
            background-color: #FBCFE8 !important;
            background-image: none !important;
            color: #1F1F1F !important;
        }}
        
        /* Dividers */
        hr {{
            border-color: rgba(255, 255, 255, 0.5) !important;
        }}
        </style>
        """, unsafe_allow_html=True)
    else:
        # Fallback styling without background image
        st.markdown("""
        <style>
        /* Base Button Styling - ONLY for mental health feature buttons */
        button[key="btn_checkin"],
        button[key="btn_breath"],
        button[key="btn_reset"],
        button[key="btn_talk"] {{
            width: 100% !important;
            height: 90px !important;
            border-radius: 15px !important;
            font-size: 26px !important;
            font-weight: 600 !important;
            margin-bottom: 15px !important;
            box-shadow: 0 4px 10px rgba(0,0,0,0.25) !important;
            transition: all 0.2s ease !important;
            text-align: left !important;
            padding: 20px !important;
            border: 3px solid rgba(100,100,100,0.4) !important;
        }}
        
        button[key="btn_checkin"]:hover,
        button[key="btn_breath"]:hover,
        button[key="btn_reset"]:hover,
        button[key="btn_talk"]:hover {{
            transform: translateY(-2px) !important;
            box-shadow: 0 6px 14px rgba(0,0,0,0.35) !important;
        }}
        
        /* Back button */
        button[key="nav_back"] {{
            background-color: transparent !important;
            border: 1px solid #ddd !important;
            color: #888 !important;
            height: 45px !important;
            font-size: 14px !important;
            box-shadow: none !important;
        }}

        /* Daily Check-in - Soft Purple */
        button[key="btn_checkin"] {{
            background-color: #E9D5FF !important;
            background-image: none !important;
            color: #1F1F1F !important;
        }}

        /* Breathing & Calm - Soft Yellow */
        button[key="btn_breath"] {{
            background-color: #FEF3C7 !important;
            background-image: none !important;
            color: #1F1F1F !important;
        }}

        /* Mind Reset - Soft Teal */
        button[key="btn_reset"] {{
            background-color: #A7F3D0 !important;
            background-image: none !important;
            color: #1F1F1F !important;
        }}

        /* Talk to AI - Soft Pink */
        button[key="btn_talk"] {{
            background-color: #FBCFE8 !important;
            background-image: none !important;
            color: #1F1F1F !important;
        }}
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
            <div style="margin-bottom: 30px;">
                <h1 style="font-size: 48px; color: #FFFFFF; margin: 0; font-weight: bold;">Mental Health<br>Matters</h1>
                <p style="font-size: 20px; color: #FFFFFF; font-weight: bold; margin-top: 10px;">Your mental wellness journey starts here</p>
                <p style="font-size: 16px; color: #FFFFFF; font-weight: normal; margin-top: 15px;">Choose your wellness tool</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Create a narrower column for buttons
            btn_col1, btn_col2 = st.columns([3, 1])
            
            with btn_col1:
                # 2. Daily Check-in (Global Index 2)
                if st.button("📝 Daily check-in", key="btn_checkin", use_container_width=True):
                    st.session_state.mental_view = "checkin"
                    st.rerun()
                
                # 3. Breathing (Global Index 3)
                if st.button("🌬️ Breathing & calm", key="btn_breath", use_container_width=True):
                    st.session_state.mental_view = "breathing"
                    st.rerun()
                
                # 4. Mind Reset (Global Index 4)
                if st.button("🧘 Mind Reset", key="btn_reset", use_container_width=True):
                    st.session_state.mental_view = "reset"
                    st.rerun()

                # 5. Talk (Global Index 5)
                if st.button("💬 Talk ⭐", key="btn_talk", use_container_width=True):
                    st.session_state.mental_view = "talk"
                    st.rerun()

        with col_right:
            # Right side with the illustration
            pass

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
            show_smart_checkin(username=st.session_state.get("user", "guest"))

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
