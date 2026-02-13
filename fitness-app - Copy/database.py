import sqlite3
import hashlib
import json
from datetime import datetime

# Database file name
DB_NAME = "routinex.db"

# ---------------------------------------------------------
# DATABASE INITIALIZATION
# ---------------------------------------------------------

def init_db():
    """
    Creates the necessary tables if they do not exist.
    """
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    # 1. USERS TABLE
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password_hash TEXT NOT NULL,
            created_at TEXT
        )
    ''')

    # 2. PLANS TABLE (Diet Plans Only)
    c.execute('''
        CREATE TABLE IF NOT EXISTS saved_plans (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            plan_data TEXT,
            created_at TEXT,
            FOREIGN KEY(username) REFERENCES users(username)
        )
    ''')

    # 3. MENTAL HEALTH LOGS
    c.execute('''
        CREATE TABLE IF NOT EXISTS mental_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            mood_score INTEGER,
            mood_label TEXT,
            stress_factors TEXT,
            notes TEXT,
            date TEXT,
            FOREIGN KEY(username) REFERENCES users(username)
        )
    ''')

    # 4. WORKOUT CHECK-INS (NEW)
    c.execute('''
        CREATE TABLE IF NOT EXISTS workout_checkins (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            workout_data TEXT NOT NULL,
            plan_name TEXT,
            duration_weeks INTEGER,
            created_at TEXT NOT NULL,
            is_active INTEGER DEFAULT 1,
            FOREIGN KEY(username) REFERENCES users(username)
        )
    ''')

    # 5. DAILY CHECK-IN LOGS (NEW)
    c.execute('''
        CREATE TABLE IF NOT EXISTS daily_checkin_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            date TEXT NOT NULL,
            workout_completed INTEGER DEFAULT 0,
            water_intake INTEGER DEFAULT 0,
            meditation INTEGER DEFAULT 0,
            sleep_quality INTEGER,
            notes TEXT,
            created_at TEXT NOT NULL,
            FOREIGN KEY(username) REFERENCES users(username),
            UNIQUE(username, date)
        )
    ''')

    # 6. CANVAS ENTRIES (NEW)
    c.execute('''
        CREATE TABLE IF NOT EXISTS canvas_entries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            content TEXT NOT NULL,
            mood TEXT,
            created_at TEXT NOT NULL,
            FOREIGN KEY(username) REFERENCES users(username)
        )
    ''')

    # 7. DAILY WINS (NEW)
    c.execute('''
        CREATE TABLE IF NOT EXISTS daily_wins (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            win1 TEXT,
            win2 TEXT,
            win3 TEXT,
            created_at TEXT NOT NULL,
            FOREIGN KEY(username) REFERENCES users(username)
        )
    ''')

    conn.commit()
    conn.close()

# ---------------------------------------------------------
# HELPER: PASSWORD HASHING
# ---------------------------------------------------------

def make_hash(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

# ---------------------------------------------------------
# USER FUNCTIONS
# ---------------------------------------------------------

def add_user(username, password):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    
    password_hash = make_hash(password)
    created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    try:
        c.execute('INSERT INTO users (username, password_hash, created_at) VALUES (?, ?, ?)', 
                  (username, password_hash, created_at))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def verify_user(username, password):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    
    password_hash = make_hash(password)
    
    c.execute('SELECT * FROM users WHERE username = ? AND password_hash = ?', 
              (username, password_hash))
    
    result = c.fetchone()
    conn.close()
    
    return result is not None

# ---------------------------------------------------------
# PLAN FUNCTIONS (Diet Plans)
# ---------------------------------------------------------

def save_plan(username, plan_data):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    
    plan_json = json.dumps(plan_data)
    created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    c.execute('INSERT INTO saved_plans (username, plan_data, created_at) VALUES (?, ?, ?)', 
              (username, plan_json, created_at))
    
    conn.commit()
    conn.close()

def get_user_plans(username):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    
    c.execute('SELECT id, plan_data, created_at FROM saved_plans WHERE username = ? ORDER BY created_at DESC', 
              (username,))
    
    rows = c.fetchall()
    conn.close()
    
    results = []
    for row in rows:
        results.append({
            "id": row[0],
            "plan": json.loads(row[1]),
            "created_at": row[2]
        })
        
    return results

def delete_plan(plan_id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('DELETE FROM saved_plans WHERE id = ?', (plan_id,))
    conn.commit()
    conn.close()

# ---------------------------------------------------------
# MENTAL HEALTH FUNCTIONS
# ---------------------------------------------------------

def log_mood(username, mood_score, mood_label, stress_factors, notes):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    
    # Store date as YYYY-MM-DD for simple daily uniqueness
    date_str = datetime.now().strftime("%Y-%m-%d")
    
    # Check if a log already exists for this user today
    c.execute("SELECT id FROM mental_logs WHERE username = ? AND date = ?", (username, date_str))
    exists = c.fetchone()
    
    # Convert list of factors to comma-separated string
    factors_str = ",".join(stress_factors) if isinstance(stress_factors, list) else stress_factors

    if exists:
        # Update existing log
        c.execute('''UPDATE mental_logs 
                     SET mood_score=?, mood_label=?, stress_factors=?, notes=? 
                     WHERE id=?''', 
                  (mood_score, mood_label, factors_str, notes, exists[0]))
    else:
        # Insert new log
        c.execute('''INSERT INTO mental_logs (username, mood_score, mood_label, stress_factors, notes, date) 
                     VALUES (?, ?, ?, ?, ?, ?)''', 
                  (username, mood_score, mood_label, factors_str, notes, date_str))
    
    conn.commit()
    conn.close()

def get_mood_history(username):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    # Get last 7 entries for the chart
    c.execute("SELECT date, mood_score FROM mental_logs WHERE username = ? ORDER BY date ASC LIMIT 7", (username,))
    data = c.fetchall()
    conn.close()
    return data

if __name__ == "__main__":
    init_db()
