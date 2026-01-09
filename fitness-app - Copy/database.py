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

    # 2. PLANS TABLE
    c.execute('''
        CREATE TABLE IF NOT EXISTS saved_plans (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            plan_data TEXT,
            created_at TEXT,
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
# PLAN FUNCTIONS
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
    
    # UPDATED: We now select 'id' as well so we can delete specific plans
    c.execute('SELECT id, plan_data, created_at FROM saved_plans WHERE username = ? ORDER BY created_at DESC', 
              (username,))
    
    rows = c.fetchall()
    conn.close()
    
    results = []
    for row in rows:
        results.append({
            "id": row[0],         # Capture the ID
            "plan": json.loads(row[1]),
            "created_at": row[2]
        })
        
    return results

def delete_plan(plan_id):
    """
    Deletes a specific plan by ID.
    """
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    
    c.execute('DELETE FROM saved_plans WHERE id = ?', (plan_id,))
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()