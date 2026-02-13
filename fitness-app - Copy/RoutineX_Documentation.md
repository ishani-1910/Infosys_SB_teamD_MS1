# RoutineX - Complete Project Documentation

## Table of Contents
1. [Project Overview](#project-overview)
2. [Features](#features)
3. [Technology Stack](#technology-stack)
4. [Installation & Setup](#installation--setup)
5. [Architecture](#architecture)
6. [Database Schema](#database-schema)
7. [Module Documentation](#module-documentation)
8. [User Guide](#user-guide)
9. [API Integration](#api-integration)
10. [Configuration](#configuration)
11. [Development Guide](#development-guide)
12. [Troubleshooting](#troubleshooting)

---

## Project Overview

**RoutineX** is a comprehensive fitness and mental wellness application built with Streamlit. It provides users with personalized workout plans, nutrition guidance, and mental health tools to support their overall wellbeing journey.

### Key Highlights
- **AI-Powered Planning**: Uses Google's Gemini AI for generating personalized workout and diet plans
- **Mental Health Integration**: Includes mood tracking, journaling, breathing exercises, and AI chat support
- **User Profiles**: Secure authentication and data persistence
- **Responsive Design**: Clean, modern UI with custom CSS styling

### Project Goals
- Provide an all-in-one platform for physical and mental fitness
- Leverage AI to create personalized, adaptive fitness plans
- Track progress and maintain accountability through daily check-ins
- Support mental wellness alongside physical health

---

## Features

### 1. **Workout Planning**
- Personalized workout plans based on user goals (muscle gain, fat loss, endurance, etc.)
- Multi-month progressive training schedules
- Week-by-week breakdown with specific exercises
- Consideration for injuries, experience level, and available equipment
- Active workout tracking for daily check-ins

### 2. **Nutrition Planning**
- Calorie and macro calculation based on user metrics
- Customizable diet plans with cultural preferences
- Multiple meal frequency options (3-6 meals per day)
- Support for various diet types (Vegetarian, Vegan, Keto, etc.)
- Allergy and food restriction management
- Detailed meal breakdowns with prep notes

### 3. **Mental Health & Wellness**
- **Daily Check-in**: Track mood, stress factors, and daily habits
- **Breathing & Calm**: Guided breathing exercises
- **Mind Reset**: Journaling canvas and daily wins logging
- **Talk to AI**: AI-powered mental health support chat
- Mood history tracking and visualization

### 4. **User Profile Management**
- Secure user registration and authentication
- Profile dashboard with saved plans
- View and manage:
  - Diet plans
  - Active workouts
  - Journal entries
  - Daily wins log

### 5. **Progress Tracking**
- Workout completion tracking
- Water intake monitoring
- Meditation tracking
- Sleep quality logging
- Daily notes and reflections

---

## Technology Stack

### Core Technologies
- **Frontend Framework**: Streamlit (Python web framework)
- **Backend**: Python 3.10+
- **Database**: SQLite3
- **AI/ML**: Google Gemini API (gemini-2.5-flash, gemini-2.0-flash)

### Key Libraries
```
streamlit          # Web framework
python-dotenv      # Environment variable management
google-generativeai # Gemini AI integration
sqlite3            # Database (built-in)
hashlib            # Password hashing (built-in)
json               # Data serialization (built-in)
```

### Development Tools
- Python virtual environment (recommended)
- Git for version control
- VS Code / PyCharm (recommended IDEs)

---

## Installation & Setup

### Prerequisites
- Python 3.10 or higher
- pip (Python package manager)
- Google Gemini API key

### Step 1: Clone or Extract Project
```bash
# Extract the fitness-app folder
cd fitness-app
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Configure Environment Variables
Create a `.env` file in the root directory:

```env
# .env file
GEMINI_API_KEY=your_gemini_api_key_here
# Alternative key name (will be used as fallback)
GOOGLE_API_KEY=your_gemini_api_key_here
```

**To get a Gemini API key:**
1. Visit https://makersuite.google.com/app/apikey
2. Create a new API key
3. Copy and paste into your `.env` file

### Step 4: Initialize Database
The database will be automatically initialized on first run. To manually initialize:

```bash
python database.py
```

### Step 5: Run the Application
```bash
streamlit run app.py
```

The application will open in your default browser at `http://localhost:8501`

---

## Architecture

### System Architecture Diagram
```
┌─────────────────────────────────────────┐
│         User Interface (Streamlit)      │
│  ┌─────────┐ ┌─────────┐ ┌───────────┐ │
│  │  Home   │ │ Planner │ │  Mental   │ │
│  │  Page   │ │  Page   │ │  Health   │ │
│  └─────────┘ └─────────┘ └───────────┘ │
└─────────────┬───────────────────────────┘
              │
┌─────────────┴───────────────────────────┐
│        Application Logic Layer          │
│  ┌──────────┐ ┌──────────┐ ┌─────────┐ │
│  │  Engine  │ │ Database │ │ Mental  │ │
│  │  Module  │ │  Module  │ │ Health  │ │
│  └──────────┘ └──────────┘ └─────────┘ │
└─────────────┬───────────────────────────┘
              │
┌─────────────┴───────────────────────────┐
│         External Services Layer         │
│  ┌──────────┐            ┌───────────┐  │
│  │  Gemini  │            │  SQLite   │  │
│  │   API    │            │  Database │  │
│  └──────────┘            └───────────┘  │
└─────────────────────────────────────────┘
```

### Project Structure
```
fitness-app/
├── app.py                      # Main application entry point
├── requirements.txt            # Python dependencies
├── .env                        # Environment variables (create this)
│
├── engine/                     # Core logic modules
│   ├── __init__.py
│   ├── scheduler.py           # Workout plan generation
│   ├── diet_generator.py      # Diet plan generation
│   └── nutrition.py           # Nutrition calculations
│
├── config/                     # Configuration files
│   └── diet_rules.json        # Activity & goal modifiers
│
├── assets/                     # Images and media files
│   ├── hero.png
│   ├── workout.png
│   ├── dietplan.png
│   └── mental.png
│
├── database.py                # Core database functions
├── database_extended.py       # Extended database features
│
├── mental_health.py           # Mental health module router
├── agent_interface.py         # AI chat interface
├── daily_checkin_enhanced.py  # Daily check-in system
├── breathetab.py             # Breathing exercises
├── tab_mind_reset.py         # Journaling & wins
│
├── tests/                     # Test files
│   └── test_run.py
│
├── utils/                     # Utility functions
│
├── data/                      # Data directory
│
├── routinex.db               # Main SQLite database
└── mind_reset.db             # Mental health database
```

### Application Flow

#### 1. Authentication Flow
```
User → Login/Signup Page → Credentials Verification (database.py)
                                    ↓
                        Success: Set session_state.user
                                    ↓
                        Redirect to Profile/Planner
```

#### 2. Workout Plan Generation Flow
```
User Input (Goals, Profile) → engine/scheduler.py
                                    ↓
                    Gemini API Call (Month-by-month)
                                    ↓
                        JSON Response Parsing
                                    ↓
                    Display to User + Save Option
                                    ↓
                    Save to workout_checkins table
```

#### 3. Diet Plan Generation Flow
```
User Metrics → engine/nutrition.py (Calculate needs)
                        ↓
    User Preferences → engine/diet_generator.py
                        ↓
            Gemini API Call (Meal planning)
                        ↓
            JSON Response with Meals
                        ↓
        Display + Save to saved_plans table
```

---

## Database Schema

### Database Files
- `routinex.db` - Main application database
- `mind_reset.db` - Mental health specific data

### Tables

#### 1. `users`
Stores user authentication data.
```sql
CREATE TABLE users (
    username TEXT PRIMARY KEY,
    password_hash TEXT NOT NULL,
    created_at TEXT
);
```

#### 2. `saved_plans`
Stores user diet plans.
```sql
CREATE TABLE saved_plans (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    plan_data TEXT,  -- JSON string
    created_at TEXT,
    FOREIGN KEY(username) REFERENCES users(username)
);
```

#### 3. `mental_logs`
Stores daily mood and mental health logs.
```sql
CREATE TABLE mental_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    mood_score INTEGER,
    mood_label TEXT,
    stress_factors TEXT,  -- Comma-separated
    notes TEXT,
    date TEXT,  -- YYYY-MM-DD
    FOREIGN KEY(username) REFERENCES users(username)
);
```

#### 4. `workout_checkins`
Stores active workout plans for users.
```sql
CREATE TABLE workout_checkins (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    workout_data TEXT NOT NULL,  -- JSON string
    plan_name TEXT,
    duration_weeks INTEGER,
    created_at TEXT NOT NULL,
    is_active INTEGER DEFAULT 1,
    FOREIGN KEY(username) REFERENCES users(username)
);
```

#### 5. `daily_checkin_logs`
Tracks daily habits and progress.
```sql
CREATE TABLE daily_checkin_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    date TEXT NOT NULL,  -- YYYY-MM-DD
    workout_completed INTEGER DEFAULT 0,
    water_intake INTEGER DEFAULT 0,
    meditation INTEGER DEFAULT 0,
    sleep_quality INTEGER,
    notes TEXT,
    created_at TEXT NOT NULL,
    FOREIGN KEY(username) REFERENCES users(username),
    UNIQUE(username, date)
);
```

#### 6. `canvas_entries`
Stores journal/canvas entries.
```sql
CREATE TABLE canvas_entries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    content TEXT NOT NULL,
    mood TEXT,
    created_at TEXT NOT NULL,
    FOREIGN KEY(username) REFERENCES users(username)
);
```

#### 7. `daily_wins`
Stores daily accomplishments.
```sql
CREATE TABLE daily_wins (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    win1 TEXT,
    win2 TEXT,
    win3 TEXT,
    created_at TEXT NOT NULL,
    FOREIGN KEY(username) REFERENCES users(username)
);
```

---

## Module Documentation

### 1. **app.py**
Main application file that orchestrates all components.

**Key Functions:**
- Page routing and navigation
- Session state management
- UI rendering for all pages
- Integration of sub-modules

**Pages:**
- Home: Landing page with hero section
- Planner: Workout and diet plan generation
- Mental Health: Mental wellness tools
- Premium: Coming soon features
- Profile: User dashboard

**Session State Variables:**
```python
st.session_state.page       # Current page
st.session_state.user       # Logged-in username
st.session_state.auth_mode  # Login vs Signup mode
```

### 2. **database.py**
Core database operations.

**Key Functions:**

```python
init_db()
# Initializes all database tables

add_user(username, password)
# Creates new user account
# Returns: True on success, False if username exists

verify_user(username, password)
# Verifies login credentials
# Returns: True if valid, False otherwise

save_plan(username, plan_data)
# Saves a diet plan for user
# plan_data: Dictionary containing meal plan

get_user_plans(username)
# Retrieves all saved plans for user
# Returns: List of plan dictionaries

delete_plan(plan_id)
# Deletes a specific plan

log_mood(username, mood_score, mood_label, stress_factors, notes)
# Logs daily mood entry

get_mood_history(username)
# Returns last 7 mood entries
```

### 3. **database_extended.py**
Extended database functionality.

**Key Functions:**

```python
save_workout_for_checkin(username, workout_data, plan_name, duration_weeks)
# Saves active workout plan
# Returns: workout_id

get_active_workout(username)
# Gets user's current active workout
# Returns: Workout dictionary or None

log_daily_checkin(username, date, workout_completed, water_intake, 
                  meditation, sleep_quality, notes)
# Logs daily check-in data

get_checkin_history(username, days=7)
# Gets recent check-in logs

save_canvas_entry(username, content, mood)
# Saves journal entry

get_canvas_entries(username, limit=20)
# Retrieves journal entries

delete_canvas_entry(entry_id)
# Deletes specific entry

save_wins(username, win1, win2, win3)
# Saves daily wins

get_wins(username, limit=20)
# Retrieves daily wins

delete_wins(win_id)
# Deletes specific win entry
```

### 4. **engine/scheduler.py**
Workout plan generation engine.

**Main Function:**
```python
generate_workout_plan(profile, goal, duration_months, additional_info="")
```

**Parameters:**
- `profile`: Dictionary with user experience, injuries
- `goal`: Fitness goal (muscle_gain, fat_loss, etc.)
- `duration_months`: Plan duration (1-6 months)
- `additional_info`: Equipment, notes

**Returns:**
```python
{
    "summary": "Plan description",
    "schedule": [
        {
            "week_number": 1,
            "focus": "Hypertrophy",
            "workouts": [
                {
                    "day": "Monday",
                    "focus": "Chest & Triceps",
                    "exercises": ["Exercise - Sets x Reps", ...]
                },
                ...
            ]
        },
        ...
    ]
}
```

**How It Works:**
1. Iterates through each month
2. Generates 4 weeks per month
3. Creates progressive overload structure
4. Uses Gemini AI for exercise selection
5. Returns compiled schedule

### 5. **engine/nutrition.py**
Nutritional needs calculator.

**Main Function:**
```python
calculate_nutritional_needs(age, weight, height, gender, 
                           activity_level, goal)
```

**Calculations:**
1. **BMR (Basal Metabolic Rate)**
   - Men: 10 × weight + 6.25 × height - 5 × age + 5
   - Women: 10 × weight + 6.25 × height - 5 × age - 161

2. **TDEE (Total Daily Energy Expenditure)**
   - TDEE = BMR × activity_multiplier

3. **Target Calories**
   - Based on goal (surplus/deficit from config)

4. **Macronutrients**
   - Split according to goal (from diet_rules.json)

**Returns:**
```python
{
    "calories": 2500,
    "macros": {
        "protein": 150,  # grams
        "fats": 70,      # grams
        "carbs": 280     # grams
    }
}
```

### 6. **engine/diet_generator.py**
AI-powered diet plan generator.

**Main Function:**
```python
generate_diet_plan(targets, profile)
```

**Parameters:**
- `targets`: Calorie and macro targets
- `profile`: Diet type, cuisine, allergies, meals per day

**Process:**
1. Constructs detailed prompt for Gemini AI
2. Tries multiple models (gemini-2.5-flash, gemini-2.0-flash)
3. Parses JSON response
4. Validates macro totals

**Returns:**
```python
{
    "summary": {
        "total_calories": 2500,
        "protein": 150,
        "carbs": 280,
        "fats": 70,
        "note": "Plan description"
    },
    "meals": [
        {
            "meal_name": "Breakfast",
            "food_items": [
                {
                    "item": "Oatmeal",
                    "quantity": "1 cup",
                    "calories": 300,
                    "protein": 10,
                    "carbs": 50,
                    "fats": 5,
                    "prep_note": "Cook with milk"
                },
                ...
            ]
        },
        ...
    ]
}
```

### 7. **mental_health.py**
Mental health module router.

**Views:**
- `home`: Main mental health dashboard
- `checkin`: Daily check-in
- `breathing`: Breathing exercises
- `reset`: Mind reset (journaling)
- `talk`: AI chat support

**Key Features:**
- Dynamic module loading (exec)
- Background image styling
- Session state management
- Navigation between sub-views

### 8. **daily_checkin_enhanced.py**
Daily check-in system with habit tracking.

**Features:**
- Workout completion checkbox
- Water intake counter (glasses)
- Meditation tracking
- Sleep quality rating (1-5)
- Daily notes
- Progress visualization

### 9. **agent_interface.py**
AI chat interface for mental health support.

**Features:**
- Conversational AI using Gemini
- Context-aware responses
- Mental health support focus
- Chat history management

### 10. **breathetab.py**
Guided breathing exercises.

**Exercises:**
- Box Breathing (4-4-4-4)
- 4-7-8 Breathing
- Deep Belly Breathing
- Custom timer functionality

### 11. **tab_mind_reset.py**
Journaling and wins tracking.

**Features:**
- Canvas for free-form journaling
- Mood tagging
- Daily wins (3 entries)
- Entry history viewing
- Database persistence

---

## User Guide

### Getting Started

#### 1. Create an Account
1. Click "PROFILE" in navigation
2. Select "Create Account"
3. Choose username and password (min 4 characters)
4. Click "CREATE ACCOUNT"

#### 2. Generate a Workout Plan
1. Navigate to "PLANNER"
2. Select "Workout Planner" tab
3. Fill in your details:
   - Fitness goal
   - Experience level
   - Any injuries
   - Available equipment
   - Plan duration (1-6 months)
4. Click "GENERATE WORKOUT PLAN"
5. Review the plan
6. Click "ACTIVATE FOR DAILY CHECK-IN" to track it

#### 3. Create a Diet Plan
1. Navigate to "PLANNER"
2. Select "Diet Planner" tab
3. Enter your metrics:
   - Age, weight, height, gender
   - Activity level
   - Fitness goal
4. Select preferences:
   - Diet type (Vegan, Keto, etc.)
   - Cuisine preference
   - Allergies
   - Meals per day
5. Click "GENERATE DIET PLAN"
6. Review and save the plan

#### 4. Daily Check-in
1. Go to "MENTAL HEALTH"
2. Click "Daily check-in"
3. Complete your check-in:
   - Did you workout? ✓
   - Water intake (glasses)
   - Meditation (minutes)
   - Sleep quality (1-5)
   - Notes
4. Submit to track progress

#### 5. Mind Reset (Journaling)
1. Go to "MENTAL HEALTH"
2. Click "Mind Reset"
3. Write in your journal canvas
4. Select your current mood
5. Log daily wins (3 things)
6. Save entries

#### 6. Talk to AI
1. Go to "MENTAL HEALTH"
2. Click "Talk ⭐"
3. Chat with AI for support
4. Discuss feelings, get advice
5. Receive empathetic responses

### Profile Management

#### View Saved Plans
1. Navigate to "PROFILE"
2. Browse tabs:
   - **Diet Plans**: View/delete saved diets
   - **Workouts**: See active workout schedule
   - **Canvas Entries**: Review journal entries
   - **Daily Wins**: Check your wins log

#### Logout
Click "LOGOUT" button in profile page

---

## API Integration

### Google Gemini API

**Purpose**: AI-powered content generation

**Models Used:**
- `gemini-2.5-flash` (primary)
- `gemini-2.0-flash` (fallback)
- `gemini-flash-latest` (fallback)

**API Key Configuration:**
```python
# In .env file
GEMINI_API_KEY=your_key_here
```

**Usage in Code:**
```python
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

model = genai.GenerativeModel('gemini-2.5-flash')
response = model.generate_content(prompt)
```

**Rate Limits:**
- Free tier: 60 requests/minute
- Paid tier: Higher limits available

**Error Handling:**
```python
try:
    response = model.generate_content(prompt)
except Exception as e:
    # Fallback to alternative model
    # Or return error message
```

---

## Configuration

### config/diet_rules.json

**Activity Multipliers:**
```json
{
  "activity_multipliers": {
    "sedentary": 1.2,
    "lightly_active": 1.375,
    "moderately_active": 1.55,
    "very_active": 1.725,
    "extra_active": 1.9
  }
}
```

**Goal Modifiers:**
```json
{
  "goal_modifiers": {
    "muscle_gain": {
      "calorie_surplus": 300,
      "macro_split": {
        "protein": 0.30,
        "fats": 0.25,
        "carbs": 0.45
      }
    },
    "fat_loss": {
      "calorie_surplus": -500,
      "macro_split": {
        "protein": 0.40,
        "fats": 0.30,
        "carbs": 0.30
      }
    }
  }
}
```

### CSS Customization

The app uses extensive custom CSS in `app.py`:

**Key Styling Classes:**
- `.brand` - Main logo/title
- `.tagline` - Subtitle text
- `.section-title` - Page section headers
- `.plan-card` - Diet plan display cards
- Button styling for primary/secondary actions

**Color Scheme:**
- Primary: Black (#000000)
- Background: White (#FFFFFF)
- Accents: Grey tones
- Mental Health: Pastel colors (purple, yellow, teal, pink)

---

## Development Guide

### Setting Up Development Environment

1. **Clone Repository**
```bash
git clone <repository-url>
cd fitness-app
```

2. **Create Virtual Environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install Dependencies**
```bash
pip install -r requirements.txt
```

4. **Set Up Environment Variables**
```bash
echo "GEMINI_API_KEY=your_key" > .env
```

5. **Run in Development Mode**
```bash
streamlit run app.py
```

### Adding New Features

#### Adding a New Page
1. Add page button to navigation in `app.py`
2. Create session state condition
3. Implement page rendering logic
4. Style with custom CSS if needed

Example:
```python
# In navigation
if st.button("NEW PAGE"):
    st.session_state.page = "new_page"
    st.rerun()

# Page rendering
elif st.session_state.page == "new_page":
    st.markdown("<h2>New Feature</h2>", unsafe_allow_html=True)
    # Your page code here
```

#### Adding Database Table
1. Update `database.py` `init_db()` function
2. Add CRUD functions for new table
3. Create UI for data entry/display

Example:
```python
def init_db():
    # ... existing tables ...
    c.execute('''
        CREATE TABLE IF NOT EXISTS new_table (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            data TEXT,
            created_at TEXT NOT NULL,
            FOREIGN KEY(username) REFERENCES users(username)
        )
    ''')
```

### Testing

#### Manual Testing Checklist
- [ ] User registration works
- [ ] Login authentication works
- [ ] Workout plan generation works
- [ ] Diet plan generation works
- [ ] Plans save to database
- [ ] Mental health features work
- [ ] Daily check-in logs correctly
- [ ] Journal entries save
- [ ] Logout clears session

#### Automated Testing
```python
# tests/test_run.py
import unittest
from database import add_user, verify_user, init_db

class TestDatabase(unittest.TestCase):
    def setUp(self):
        init_db()
    
    def test_user_creation(self):
        result = add_user("testuser", "password123")
        self.assertTrue(result)
    
    def test_user_login(self):
        add_user("testuser2", "password123")
        result = verify_user("testuser2", "password123")
        self.assertTrue(result)

if __name__ == '__main__':
    unittest.main()
```

### Code Style Guidelines

**Python Style (PEP 8):**
- 4 spaces for indentation
- Max line length: 100 characters
- Use descriptive variable names
- Add docstrings to functions

**Streamlit Best Practices:**
- Use session state for persistence
- Implement proper error handling
- Show loading states for API calls
- Use caching where appropriate (`@st.cache_data`)

### Version Control

**Git Workflow:**
```bash
# Create feature branch
git checkout -b feature/new-feature

# Make changes and commit
git add .
git commit -m "Add new feature"

# Push to remote
git push origin feature/new-feature

# Create pull request
```

**Commit Message Format:**
```
<type>: <description>

[optional body]

Types: feat, fix, docs, style, refactor, test, chore
```

---

## Troubleshooting

### Common Issues

#### 1. "API Key not found" Error

**Symptom:** Diet/Workout generation fails with API key error

**Solution:**
```bash
# Check .env file exists
ls -la .env

# Verify contents
cat .env

# Ensure key is correct
GEMINI_API_KEY=your_actual_key_here

# Restart application
streamlit run app.py
```

#### 2. Database Locked Error

**Symptom:** "database is locked" message

**Solution:**
```python
# Close any open database connections
# Add timeout to connection
conn = sqlite3.connect(DB_NAME, timeout=10)
```

#### 3. Module Import Errors

**Symptom:** "ModuleNotFoundError: No module named 'X'"

**Solution:**
```bash
# Reinstall requirements
pip install -r requirements.txt

# Or install specific package
pip install google-generativeai
```

#### 4. Streamlit Port Already in Use

**Symptom:** "Address already in use"

**Solution:**
```bash
# Use different port
streamlit run app.py --server.port 8502

# Or kill existing process
# On Unix/Mac
lsof -ti:8501 | xargs kill -9

# On Windows
netstat -ano | findstr :8501
taskkill /PID <PID> /F
```

#### 5. JSON Parsing Errors

**Symptom:** "JSONDecodeError" from AI responses

**Solution:**
- Check Gemini API key validity
- Verify API quota not exceeded
- Try fallback model in code
- Add better error handling:

```python
try:
    data = json.loads(response)
except json.JSONDecodeError:
    # Log the raw response
    print(f"Raw response: {response}")
    # Try cleaning
    cleaned = response.replace("```json", "").replace("```", "")
    data = json.loads(cleaned)
```

#### 6. Session State Issues

**Symptom:** Data not persisting between page changes

**Solution:**
```python
# Initialize session state properly
if "key" not in st.session_state:
    st.session_state.key = default_value

# Use st.rerun() after state changes
st.session_state.page = "new_page"
st.rerun()
```

### Debug Mode

Enable debug logging:
```python
import logging
logging.basicConfig(level=logging.DEBUG)

# In your code
logging.debug(f"User data: {user_data}")
logging.debug(f"API response: {response}")
```

### Performance Optimization

**Slow Page Loads:**
```python
# Cache expensive functions
@st.cache_data(ttl=3600)
def expensive_function(param):
    # Your code
    return result

# Cache resources
@st.cache_resource
def load_model():
    return genai.GenerativeModel('gemini-2.5-flash')
```

### Getting Help

**Resources:**
- Streamlit Documentation: https://docs.streamlit.io
- Gemini API Docs: https://ai.google.dev/docs
- SQLite Documentation: https://www.sqlite.org/docs.html

**Support Channels:**
- Create an issue in project repository
- Check existing issues for solutions
- Contact development team

---

## Appendix

### A. Environment Variables Reference

| Variable | Required | Description | Example |
|----------|----------|-------------|---------|
| GEMINI_API_KEY | Yes | Google Gemini API key | AIza... |
| GOOGLE_API_KEY | No | Alternative key name | AIza... |

### B. Database Backup

**Manual Backup:**
```bash
# Backup databases
cp routinex.db routinex_backup_$(date +%Y%m%d).db
cp mind_reset.db mind_reset_backup_$(date +%Y%m%d).db
```

**Automated Backup Script:**
```python
import shutil
from datetime import datetime

def backup_databases():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    shutil.copy('routinex.db', f'backups/routinex_{timestamp}.db')
    shutil.copy('mind_reset.db', f'backups/mind_reset_{timestamp}.db')
```

### C. Deployment Guide

**Deploying to Streamlit Cloud:**

1. Push code to GitHub
2. Visit https://share.streamlit.io
3. Connect GitHub repository
4. Set environment variables in Streamlit Cloud dashboard
5. Deploy

**Deploying to Heroku:**

1. Create `Procfile`:
```
web: streamlit run app.py --server.port $PORT
```

2. Create `setup.sh`:
```bash
mkdir -p ~/.streamlit/
echo "[server]
headless = true
port = $PORT
enableCORS = false
" > ~/.streamlit/config.toml
```

3. Deploy:
```bash
heroku create your-app-name
git push heroku main
heroku config:set GEMINI_API_KEY=your_key
```

### D. Security Best Practices

1. **Never commit API keys**
   - Add `.env` to `.gitignore`
   - Use environment variables

2. **Password Security**
   - Passwords are hashed with SHA-256
   - Consider upgrading to bcrypt for production

3. **Input Validation**
   - Validate all user inputs
   - Sanitize data before database insertion
   - Use parameterized queries (already implemented)

4. **Database Security**
   - Keep databases out of public folders
   - Regular backups
   - Consider encryption for sensitive data

### E. Future Enhancements

**Potential Features:**
- [ ] Social features (friend connections)
- [ ] Progress charts and analytics
- [ ] Exercise video library
- [ ] Recipe database with images
- [ ] Mobile app version
- [ ] Wearable device integration
- [ ] Community challenges
- [ ] Professional trainer matching
- [ ] Meal prep shopping lists
- [ ] Workout video recording
- [ ] Advanced analytics dashboard
- [ ] Integration with fitness trackers

---

## Changelog

### Version 1.0.0 (Current)
- Initial release
- Workout plan generation
- Diet plan generation
- Mental health tools
- User authentication
- Profile management

---

## Credits & License

### Built With
- **Streamlit** - Web framework
- **Google Gemini** - AI model
- **SQLite** - Database

### Development Team
- Project developed as a comprehensive fitness application
- AI integration using Google Gemini API

### License
[Add your license information here]

---

## Contact & Support

For questions, issues, or contributions:
- GitHub: [Repository URL]
- Email: [Contact Email]
- Documentation: This file

---

*Last Updated: February 2026*
*Documentation Version: 1.0.0*
