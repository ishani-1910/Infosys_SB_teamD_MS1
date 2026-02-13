import sqlite3
import json
from datetime import datetime, timedelta

DB_NAME = "routinex.db"

# ==========================================
# WORKOUT CHECK-IN FUNCTIONS
# ==========================================

def save_workout_for_checkin(username, workout_data, plan_name, duration_weeks):
    """
    Save a workout plan for daily check-in tracking.
    Deactivates any existing active workout first.
    """
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    
    # Deactivate existing active workouts
    c.execute("UPDATE workout_checkins SET is_active = 0 WHERE username = ?", (username,))
    
    # Insert new active workout
    workout_json = json.dumps(workout_data)
    created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    c.execute('''
        INSERT INTO workout_checkins 
        (username, workout_data, plan_name, duration_weeks, created_at, is_active) 
        VALUES (?, ?, ?, ?, ?, 1)
    ''', (username, workout_json, plan_name, duration_weeks, created_at))
    
    conn.commit()
    conn.close()

def get_active_workout(username):
    """Get the currently active workout plan"""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    
    c.execute('''
        SELECT id, workout_data, plan_name, duration_weeks, created_at 
        FROM workout_checkins 
        WHERE username = ? AND is_active = 1 
        ORDER BY created_at DESC LIMIT 1
    ''', (username,))
    
    row = c.fetchone()
    conn.close()
    
    if row:
        return {
            "id": row[0],
            "workout_data": json.loads(row[1]),
            "plan_name": row[2],
            "duration_weeks": row[3],
            "created_at": row[4]
        }
    return None

def get_all_user_workouts(username):
    """Get all workout plans (active and archived)"""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    
    c.execute('''
        SELECT id, plan_name, duration_weeks, created_at, is_active 
        FROM workout_checkins 
        WHERE username = ? 
        ORDER BY created_at DESC
    ''', (username,))
    
    rows = c.fetchall()
    conn.close()
    
    return [
        {
            "id": row[0],
            "plan_name": row[1],
            "duration_weeks": row[2],
            "created_at": row[3],
            "is_active": row[4] == 1
        }
        for row in rows
    ]

def archive_workout(workout_id):
    """Archive a workout (set is_active to 0)"""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("UPDATE workout_checkins SET is_active = 0 WHERE id = ?", (workout_id,))
    conn.commit()
    conn.close()

# ==========================================
# DAILY CHECK-IN FUNCTIONS
# ==========================================

def save_daily_checkin(username, date, workout_done, water, meditation, sleep, notes):
    """
    Save or update daily check-in for a specific date.
    Uses UPSERT logic (update if exists, insert if not).
    """
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    
    created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Check if entry exists
    c.execute("SELECT id FROM daily_checkin_logs WHERE username = ? AND date = ?", 
              (username, date))
    exists = c.fetchone()
    
    if exists:
        # Update existing
        c.execute('''
            UPDATE daily_checkin_logs 
            SET workout_completed = ?, water_intake = ?, meditation = ?, 
                sleep_quality = ?, notes = ?, created_at = ?
            WHERE id = ?
        ''', (workout_done, water, meditation, sleep, notes, created_at, exists[0]))
    else:
        # Insert new
        c.execute('''
            INSERT INTO daily_checkin_logs 
            (username, date, workout_completed, water_intake, meditation, 
             sleep_quality, notes, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (username, date, workout_done, water, meditation, sleep, notes, created_at))
    
    conn.commit()
    conn.close()

def get_daily_checkin(username, date):
    """Get check-in data for a specific date"""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    
    c.execute('''
        SELECT workout_completed, water_intake, meditation, sleep_quality, notes, created_at
        FROM daily_checkin_logs 
        WHERE username = ? AND date = ?
    ''', (username, date))
    
    row = c.fetchone()
    conn.close()
    
    if row:
        return {
            "workout_completed": row[0] == 1,
            "water_intake": row[1] == 1,
            "meditation": row[2] == 1,
            "sleep_quality": row[3],
            "notes": row[4],
            "created_at": row[5]
        }
    return None

def get_checkin_history(username, limit=7):
    """Get recent check-in history"""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    
    c.execute('''
        SELECT date, workout_completed, water_intake, meditation, sleep_quality, notes
        FROM daily_checkin_logs 
        WHERE username = ? 
        ORDER BY date DESC 
        LIMIT ?
    ''', (username, limit))
    
    rows = c.fetchall()
    conn.close()
    
    return [
        {
            "date": row[0],
            "workout_completed": row[1] == 1,
            "water_intake": row[2] == 1,
            "meditation": row[3] == 1,
            "sleep_quality": row[4],
            "notes": row[5]
        }
        for row in rows
    ]

def get_streak_count(username):
    """Calculate current streak of consecutive check-ins"""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    
    c.execute('''
        SELECT date FROM daily_checkin_logs 
        WHERE username = ? 
        ORDER BY date DESC
    ''', (username,))
    
    dates = [row[0] for row in c.fetchall()]
    conn.close()
    
    if not dates:
        return 0
    
    streak = 0
    current_date = datetime.now().date()
    
    for date_str in dates:
        date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()
        if date_obj == current_date:
            streak += 1
            current_date -= timedelta(days=1)
        elif date_obj == current_date + timedelta(days=1):
            # If we haven't checked in today, but checked in yesterday
            streak += 1
            current_date = date_obj - timedelta(days=1)
        else:
            break
    
    return streak

# ==========================================
# CANVAS ENTRY FUNCTIONS
# ==========================================

def save_canvas_entry(username, content, mood):
    """Save a Mind Reset canvas entry"""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    
    created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    c.execute('''
        INSERT INTO canvas_entries (username, content, mood, created_at)
        VALUES (?, ?, ?, ?)
    ''', (username, content, mood, created_at))
    
    conn.commit()
    conn.close()

def get_canvas_entries(username, limit=20):
    """Get canvas entries for user"""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    
    c.execute('''
        SELECT id, content, mood, created_at
        FROM canvas_entries 
        WHERE username = ? 
        ORDER BY created_at DESC 
        LIMIT ?
    ''', (username, limit))
    
    rows = c.fetchall()
    conn.close()
    
    return [
        {
            "id": row[0],
            "content": row[1],
            "mood": row[2],
            "created_at": row[3]
        }
        for row in rows
    ]

def delete_canvas_entry(entry_id):
    """Delete a canvas entry"""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("DELETE FROM canvas_entries WHERE id = ?", (entry_id,))
    conn.commit()
    conn.close()

# ==========================================
# WINS FUNCTIONS
# ==========================================

def save_wins(username, win1, win2, win3):
    """Save daily wins"""
    if not any([win1, win2, win3]):
        return False
    
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    
    created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    c.execute('''
        INSERT INTO daily_wins (username, win1, win2, win3, created_at)
        VALUES (?, ?, ?, ?, ?)
    ''', (username, win1 or "", win2 or "", win3 or "", created_at))
    
    conn.commit()
    conn.close()
    return True

def get_wins(username, limit=20):
    """Get wins for user"""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    
    c.execute('''
        SELECT id, win1, win2, win3, created_at
        FROM daily_wins 
        WHERE username = ? 
        ORDER BY created_at DESC 
        LIMIT ?
    ''', (username, limit))
    
    rows = c.fetchall()
    conn.close()
    
    return [
        {
            "id": row[0],
            "win1": row[1],
            "win2": row[2],
            "win3": row[3],
            "created_at": row[4]
        }
        for row in rows
    ]

def delete_wins(win_id):
    """Delete a win entry"""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("DELETE FROM daily_wins WHERE id = ?", (win_id,))
    conn.commit()
    conn.close()
