import streamlit as st
import os
import time
from datetime import datetime
from dotenv import load_dotenv
import google.generativeai as genai
from googleapiclient.discovery import build

# NEW: Import from main database
from database_extended import (
    save_canvas_entry,
    get_canvas_entries,
    save_wins,
    get_wins
)

# --- 1. CONFIGURATION & SETUP ---
load_dotenv()

# API KEYS
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

# --- 2. CSS & AESTHETICS (The "Mind Reset" Visual Engine) ---
def inject_vibrant_css():
    st.markdown("""
    <style>
        /* IMPORT FONTS */
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;700&family=Space+Grotesk:wght@400;700&display=swap');

        /* ANIMATED BACKGROUND GRADIENT */
        .stApp {
            background: linear-gradient(-45deg, #ee7752, #e73c7e, #23a6d5, #23d5ab);
            background-size: 400% 400%;
            animation: gradient 15s ease infinite;
        }

        @keyframes gradient {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }

        /* GLASS CARD STYLING */
        .glass-card {
            background: rgba(255, 255, 255, 0.1);
            border-radius: 20px;
            box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            border: 1px solid rgba(255, 255, 255, 0.18);
            padding: 25px;
            margin-bottom: 25px;
            color: white;
            transition: transform 0.3s ease;
        }
        
        .glass-card:hover {
            transform: translateY(-5px);
            border: 1px solid rgba(255, 255, 255, 0.5);
        }

        /* TYPOGRAPHY */
        h1, h2, h3 { font-family: 'Space Grotesk', sans-serif !important; color: white !important; text-shadow: 0 2px 4px rgba(0,0,0,0.3); }
        p, div { font-family: 'Outfit', sans-serif !important; }

        /* INPUT FIELDS (Neon Style) */
        .stTextInput input, .stTextArea textarea {
            background-color: rgba(0, 0, 0, 0.3) !important;
            color: #fff !important;
            border: 2px solid rgba(255, 255, 255, 0.2) !important;
            border-radius: 12px !important;
        }
        .stTextInput input:focus, .stTextArea textarea:focus {
            border-color: #00f2ff !important;
            box-shadow: 0 0 15px rgba(0, 242, 255, 0.5) !important;
        }

        /* CUSTOM BUTTONS */
        .stButton button {
            background: linear-gradient(90deg, #FF0080 0%, #7928CA 100%);
            border: none;
            color: white;
            font-weight: bold;
            border-radius: 30px;
            padding: 8px 20px;
            transition: all 0.3s ease;
        }
        .stButton button:hover {
            box-shadow: 0 0 20px #FF0080;
            transform: scale(1.05);
        }

        /* GEMINI QUOTE TEXT */
        .quote-text {
            font-size: 22px;
            font-weight: 300;
            font-style: italic;
            background: -webkit-linear-gradient(eee, #fff);
            -webkit-background-clip: text;
            -webkit-text-fill-color: white;
        }
    </style>
    """, unsafe_allow_html=True)

# --- 3. LOGIC ---
def get_gemini_affirmation():
    if not GEMINI_API_KEY: return "Discipline is freedom."
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        prompt = "One short, stoic, powerful sentence about focus. Max 12 words."
        response = model.generate_content(prompt)
        return response.text.strip()
    except: return "The obstacle is the way."

def get_youtube_vibe(mood_query, custom_url=None):
    if custom_url and len(custom_url) > 5:
        if "v=" in custom_url: return custom_url.split("v=")[1].split("&")[0]
        elif "youtu.be/" in custom_url: return custom_url.split("youtu.be/")[1].split("?")[0]
        return custom_url
    if not YOUTUBE_API_KEY: return None
    try:
        youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)
        req = youtube.search().list(part="snippet", q=mood_query, type="video", maxResults=1)
        res = req.execute()
        if res['items']: return res['items'][0]['id']['videoId']
    except: return None

# --- 4. UI COMPONENTS ---

def render_sidebar():
    """Vault now pulls from main database"""
    with st.sidebar:
        st.header("🗄️ The Vault")
        
        if not st.session_state.user:
            st.warning("⚠️ Log in to see your saved content")
            return
        
        tab_journal, tab_wins = st.tabs(["📖 Journal", "🏆 Wins"])
        
        with tab_journal:
            entries = get_canvas_entries(st.session_state.user, limit=10)
            if not entries: 
                st.info("Pages are blank.")
            for e in entries:
                with st.expander(f"{e['created_at']} ({e.get('mood', 'Neutral')})"):
                    st.write(e['content'])

        with tab_wins:
            wins = get_wins(st.session_state.user, limit=10)
            if not wins:
                st.info("No wins logged yet.")
            for w in wins:
                with st.expander(f"{w['created_at']}"):
                    text = ""
                    if w.get('win1'): text += f"• {w['win1']}\n"
                    if w.get('win2'): text += f"• {w['win2']}\n"
                    if w.get('win3'): text += f"• {w['win3']}"
                    st.write(text)

def render_vibe_check():
    st.markdown("### 🎧 Vibe Check")
    
    # Mood Slider
    if 'current_mood' not in st.session_state:
        st.session_state['current_mood'] = "🌊 Deep Focus"
        
    mood = st.select_slider("Frequency:", 
        options=["🌊 Deep Focus", "⚡ High Energy", "🌌 Cosmic Chill", "🔥 Gym Mode"],
        value=st.session_state['current_mood'])
    st.session_state['current_mood'] = mood

    # Custom Link
    with st.expander("🔗 Custom URL"):
        custom_url = st.text_input("Paste Link", label_visibility="collapsed")

    queries = {
        "🌊 Deep Focus": "lofi girl live",
        "⚡ High Energy": "phonk drift mix",
        "🌌 Cosmic Chill": "ambient space travel 4k",
        "🔥 Gym Mode": "aggressive workout motivation music"
    }
    
    vid_id = get_youtube_vibe(queries[mood], custom_url) or "jfKfPfyJRdk"
    
    st.markdown(f"""
    <div class="glass-card" style="padding: 0; overflow: hidden;">
        <iframe width="100%" height="280" src="https://www.youtube.com/embed/{vid_id}?autoplay=1&mute=0&controls=1" frameborder="0" allowfullscreen></iframe>
    </div>
    """, unsafe_allow_html=True)

def burn_callback():
    """Callback to handle burn animation and clearing"""
    if st.session_state.get("burn_input_widget", ""):
        # Clear the text BEFORE rerun
        st.session_state.burn_input_widget = ""
        st.session_state.show_burn_animation = True

def render_incinerator():
    st.markdown("### 🗑️ Incinerator")
    
    with st.container():
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.caption("Write stressing thoughts. Burn them forever.")
        
        # Initialize the widget's state
        if "burn_input_widget" not in st.session_state:
            st.session_state.burn_input_widget = ""
        
        # Show burn animation if flag is set
        if st.session_state.get("show_burn_animation", False):
            bar = st.progress(0)
            status = st.empty()
            for i in range(50):
                time.sleep(0.01)
                bar.progress(i*2)
            status.write("✨ Gone.")
            time.sleep(0.5)
            st.session_state.show_burn_animation = False
            st.rerun()
            
        # The Text Area - controlled by its key only
        st.text_area("Dump Zone", 
                     height=100, 
                     key="burn_input_widget", 
                     label_visibility="collapsed")
        
        col1, col2, col3 = st.columns([1,1,1])
        with col2:
            # Button with callback - callback runs BEFORE widget is rendered on next rerun
            st.button("🔥 BURN IT", 
                     type="primary", 
                     on_click=burn_callback,
                     disabled=not st.session_state.get("burn_input_widget", ""))
            
        st.markdown('</div>', unsafe_allow_html=True)

def render_mindset():
    st.markdown("### 🧠 Mindset")
    
    c1, c2 = st.columns([3, 1])
    with c1:
        if st.button("✨ New Thought"):
            with st.spinner("."):
                st.session_state['affirmation'] = get_gemini_affirmation()
    
    with st.expander("Override"):
        manual = st.text_input("Custom Quote", label_visibility="collapsed")
        if manual: st.session_state['affirmation'] = manual

    if 'affirmation' in st.session_state:
        st.markdown(f"""
        <div class="glass-card" style="border-left: 4px solid #00f2ff; padding: 15px;">
            <p class="quote-text">"{st.session_state['affirmation']}"</p>
        </div>
        """, unsafe_allow_html=True)

def render_wins():
    st.markdown("### 💎 3 Daily Wins")
    
    if not st.session_state.user:
        st.warning("⚠️ Please log in to save your wins")
        return
    
    with st.form("wins"):
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        w1 = st.text_input("Win 1", placeholder="Small")
        w2 = st.text_input("Win 2", placeholder="Medium")
        w3 = st.text_input("Win 3", placeholder="Large")
        st.markdown('</div>', unsafe_allow_html=True)
        if st.form_submit_button("Log Wins"):
            if save_wins(st.session_state.user, w1, w2, w3):
                st.success("Wins Logged")
                time.sleep(1)
                st.rerun()
            else:
                st.warning("Please enter at least one win")

def render_the_canvas():
    """The Big Journal Section"""
    st.markdown("### 🖊️ The Canvas")
    
    if not st.session_state.user:
        st.warning("⚠️ Please log in to save your entries")
        return
    
    with st.form("journal_form"):
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown(f"**{datetime.now().strftime('%A, %B %d')}** — *Capture the signal.*")
        
        entry = st.text_area("Write freely...", height=300, label_visibility="collapsed")
        
        cols = st.columns([1, 4])
        with cols[0]:
            submitted = st.form_submit_button("💾 Save Entry")
        
        if submitted and entry:
            mood = st.session_state.get('current_mood', 'Neutral')
            save_canvas_entry(st.session_state.user, entry, mood)
            st.success("Journal Updated.")
            time.sleep(1)
            st.rerun()
            
        st.markdown('</div>', unsafe_allow_html=True)

# --- MAIN LAYOUT ---
def render_app():
    inject_vibrant_css()
    render_sidebar()
    
    st.markdown("""
    <h1 style="text-align: center; font-size: 3.5rem; margin-bottom: 10px;">
        Mind <span style="background: -webkit-linear-gradient(#eee, #333); -webkit-background-clip: text; color: transparent; text-shadow: 0 0 20px #fff;">Reset</span> 🟣
    </h1>
    """, unsafe_allow_html=True)

    # Top Section: Two Columns (1.5 : 1 Ratio)
    col1, col2 = st.columns([1.5, 1])
    
    with col1:
        render_vibe_check()
        render_incinerator()
        
    with col2:
        render_mindset()
        render_wins()

    # Bottom Section: Full Width Canvas
    st.write("---")
    render_the_canvas()

if __name__ == "__main__":
    st.set_page_config(layout="wide", page_title="Mind Reset Journal")
    render_app()
