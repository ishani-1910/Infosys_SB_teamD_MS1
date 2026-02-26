"""
database_tracker.py
Full SQLite database layer for the RoutineX Smart Daily Tracker.
Handles: daily diary entries, weight logs, goals, weekly reviews,
         saved workout plans, saved diet plans, canvas journal entries.
"""

import sqlite3
import json
from datetime import datetime, timedelta, date

DB_NAME = "routinex.db"


def _conn():
    c = sqlite3.connect(DB_NAME)
    c.row_factory = sqlite3.Row
    return c


# ──────────────────────────────────────────────────────────────
# INIT — creates every table if not present (safe to re-run)
# ──────────────────────────────────────────────────────────────

def init_tracker_db():
    con = _conn()
    cur = con.cursor()

    # ── 1. USER GOALS ──────────────────────────────────────────
    cur.execute("""
        CREATE TABLE IF NOT EXISTS user_goals (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            username    TEXT NOT NULL,
            goal_type   TEXT NOT NULL,          -- e.g. 'weight_loss','muscle_gain','endurance'
            description TEXT,                   -- free text: "Lose 2 kg in 2 months"
            start_weight REAL,                  -- kg at goal creation
            target_weight REAL,                 -- kg target (nullable)
            start_date  TEXT NOT NULL,          -- YYYY-MM-DD
            target_date TEXT,                   -- YYYY-MM-DD
            is_active   INTEGER DEFAULT 1,
            created_at  TEXT NOT NULL,
            FOREIGN KEY(username) REFERENCES users(username)
        )
    """)

    # ── 2. DAILY DIARY ─────────────────────────────────────────
    cur.execute("""
        CREATE TABLE IF NOT EXISTS daily_diary (
            id                  INTEGER PRIMARY KEY AUTOINCREMENT,
            username            TEXT NOT NULL,
            entry_date          TEXT NOT NULL,    -- YYYY-MM-DD
            mood                INTEGER,          -- 1-5
            mood_label          TEXT,
            energy_level        INTEGER,          -- 1-5
            sleep_hours         REAL,
            water_glasses       INTEGER,
            workout_done        INTEGER DEFAULT 0, -- 0/1
            workout_notes       TEXT,
            diet_followed       INTEGER DEFAULT 0, -- 0/1
            diet_notes          TEXT,
            journal_text        TEXT,             -- diary / reflection
            stress_level        INTEGER,          -- 1-5
            steps_count         INTEGER,
            created_at          TEXT NOT NULL,
            updated_at          TEXT NOT NULL,
            UNIQUE(username, entry_date),
            FOREIGN KEY(username) REFERENCES users(username)
        )
    """)

    # ── 3. WEIGHT LOG ──────────────────────────────────────────
    cur.execute("""
        CREATE TABLE IF NOT EXISTS weight_log (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            username    TEXT NOT NULL,
            log_date    TEXT NOT NULL,   -- YYYY-MM-DD
            weight_kg   REAL NOT NULL,
            notes       TEXT,
            created_at  TEXT NOT NULL,
            UNIQUE(username, log_date),
            FOREIGN KEY(username) REFERENCES users(username)
        )
    """)

    # ── 4. WEEKLY REVIEWS ──────────────────────────────────────
    cur.execute("""
        CREATE TABLE IF NOT EXISTS weekly_reviews (
            id                  INTEGER PRIMARY KEY AUTOINCREMENT,
            username            TEXT NOT NULL,
            week_start          TEXT NOT NULL,   -- YYYY-MM-DD (Monday)
            week_end            TEXT NOT NULL,   -- YYYY-MM-DD (Sunday)
            avg_mood            REAL,
            avg_energy          REAL,
            avg_sleep           REAL,
            avg_water           REAL,
            workouts_completed  INTEGER,
            days_diet_followed  INTEGER,
            weight_change       REAL,            -- kg delta vs prev week
            ai_summary          TEXT,            -- AI generated weekly insight
            ai_suggestion       TEXT,            -- AI recommended next steps
            created_at          TEXT NOT NULL,
            UNIQUE(username, week_start),
            FOREIGN KEY(username) REFERENCES users(username)
        )
    """)

    # ── 5. SAVED WORKOUT PLANS (full data) ─────────────────────
    cur.execute("""
        CREATE TABLE IF NOT EXISTS saved_workout_plans (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            username    TEXT NOT NULL,
            plan_name   TEXT NOT NULL,
            goal        TEXT,
            duration_months INTEGER,
            plan_data   TEXT NOT NULL,   -- JSON
            is_active   INTEGER DEFAULT 0,
            created_at  TEXT NOT NULL,
            FOREIGN KEY(username) REFERENCES users(username)
        )
    """)

    # ── 6. SAVED DIET PLANS (full data) ────────────────────────
    cur.execute("""
        CREATE TABLE IF NOT EXISTS saved_diet_plans (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            username    TEXT NOT NULL,
            plan_name   TEXT NOT NULL,
            goal        TEXT,
            calories    INTEGER,
            plan_data   TEXT NOT NULL,   -- JSON
            is_active   INTEGER DEFAULT 0,
            created_at  TEXT NOT NULL,
            FOREIGN KEY(username) REFERENCES users(username)
        )
    """)

    # ── 7. CANVAS / JOURNAL ENTRIES ────────────────────────────
    cur.execute("""
        CREATE TABLE IF NOT EXISTS canvas_entries (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            username    TEXT NOT NULL,
            content     TEXT NOT NULL,
            mood        TEXT,
            tags        TEXT,            -- comma-separated
            created_at  TEXT NOT NULL,
            FOREIGN KEY(username) REFERENCES users(username)
        )
    """)

    # ── 8. DAILY WINS ──────────────────────────────────────────
    cur.execute("""
        CREATE TABLE IF NOT EXISTS daily_wins (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            username    TEXT NOT NULL,
            win1        TEXT,
            win2        TEXT,
            win3        TEXT,
            win_date    TEXT NOT NULL,   -- YYYY-MM-DD
            created_at  TEXT NOT NULL,
            FOREIGN KEY(username) REFERENCES users(username)
        )
    """)

    # ── 9. TO-DO LIST (daily tasks) ────────────────────────────
    cur.execute("""
        CREATE TABLE IF NOT EXISTS daily_todos (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            username    TEXT NOT NULL,
            todo_date   TEXT NOT NULL,   -- YYYY-MM-DD
            task_text   TEXT NOT NULL,
            is_done     INTEGER DEFAULT 0,
            created_at  TEXT NOT NULL,
            FOREIGN KEY(username) REFERENCES users(username)
        )
    """)

    con.commit()
    con.close()


# ──────────────────────────────────────────────────────────────
# GOALS
# ──────────────────────────────────────────────────────────────

def save_goal(username, goal_type, description, start_weight, target_weight, start_date, target_date):
    con = _conn()
    cur = con.cursor()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # deactivate previous
    cur.execute("UPDATE user_goals SET is_active=0 WHERE username=?", (username,))
    cur.execute("""
        INSERT INTO user_goals
        (username,goal_type,description,start_weight,target_weight,start_date,target_date,is_active,created_at)
        VALUES(?,?,?,?,?,?,?,1,?)
    """, (username, goal_type, description, start_weight, target_weight, start_date, target_date, now))
    con.commit(); con.close()


def get_active_goal(username):
    con = _conn()
    row = con.execute(
        "SELECT * FROM user_goals WHERE username=? AND is_active=1 ORDER BY created_at DESC LIMIT 1",
        (username,)
    ).fetchone()
    con.close()
    return dict(row) if row else None


# ──────────────────────────────────────────────────────────────
# DAILY DIARY
# ──────────────────────────────────────────────────────────────

def upsert_diary(username, entry_date, **fields):
    """Insert or update a diary row. Pass only the fields you want to save."""
    con = _conn()
    cur = con.cursor()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    existing = cur.execute(
        "SELECT id FROM daily_diary WHERE username=? AND entry_date=?",
        (username, entry_date)
    ).fetchone()

    if existing:
        sets = ", ".join(f"{k}=?" for k in fields)
        vals = list(fields.values()) + [now, existing["id"]]
        cur.execute(f"UPDATE daily_diary SET {sets}, updated_at=? WHERE id=?", vals)
    else:
        cols = ["username", "entry_date", "created_at", "updated_at"] + list(fields.keys())
        vals = [username, entry_date, now, now] + list(fields.values())
        placeholders = ",".join(["?"] * len(cols))
        cur.execute(f"INSERT INTO daily_diary ({','.join(cols)}) VALUES({placeholders})", vals)

    con.commit(); con.close()


def get_diary_entry(username, entry_date):
    con = _conn()
    row = con.execute(
        "SELECT * FROM daily_diary WHERE username=? AND entry_date=?",
        (username, entry_date)
    ).fetchone()
    con.close()
    return dict(row) if row else None


def get_diary_range(username, start_date, end_date):
    con = _conn()
    rows = con.execute(
        "SELECT * FROM daily_diary WHERE username=? AND entry_date BETWEEN ? AND ? ORDER BY entry_date ASC",
        (username, start_date, end_date)
    ).fetchall()
    con.close()
    return [dict(r) for r in rows]


def get_diary_last_n(username, n=30):
    con = _conn()
    rows = con.execute(
        "SELECT * FROM daily_diary WHERE username=? ORDER BY entry_date DESC LIMIT ?",
        (username, n)
    ).fetchall()
    con.close()
    return [dict(r) for r in rows]


# ──────────────────────────────────────────────────────────────
# WEIGHT LOG
# ──────────────────────────────────────────────────────────────

def log_weight(username, log_date, weight_kg, notes=""):
    con = _conn()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    con.execute("""
        INSERT INTO weight_log(username,log_date,weight_kg,notes,created_at)
        VALUES(?,?,?,?,?)
        ON CONFLICT(username,log_date) DO UPDATE SET weight_kg=excluded.weight_kg, notes=excluded.notes
    """, (username, log_date, weight_kg, notes, now))
    con.commit(); con.close()


def get_weight_history(username, limit=52):
    con = _conn()
    rows = con.execute(
        "SELECT log_date, weight_kg, notes FROM weight_log WHERE username=? ORDER BY log_date ASC LIMIT ?",
        (username, limit)
    ).fetchall()
    con.close()
    return [dict(r) for r in rows]


def get_latest_weight(username):
    con = _conn()
    row = con.execute(
        "SELECT weight_kg, log_date FROM weight_log WHERE username=? ORDER BY log_date DESC LIMIT 1",
        (username,)
    ).fetchone()
    con.close()
    return dict(row) if row else None


# ──────────────────────────────────────────────────────────────
# WEEKLY REVIEWS
# ──────────────────────────────────────────────────────────────

def save_weekly_review(username, week_start, week_end, avg_mood, avg_energy,
                        avg_sleep, avg_water, workouts_completed, days_diet,
                        weight_change, ai_summary, ai_suggestion):
    con = _conn()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    con.execute("""
        INSERT INTO weekly_reviews
        (username,week_start,week_end,avg_mood,avg_energy,avg_sleep,avg_water,
         workouts_completed,days_diet_followed,weight_change,ai_summary,ai_suggestion,created_at)
        VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)
        ON CONFLICT(username,week_start) DO UPDATE SET
            avg_mood=excluded.avg_mood, avg_energy=excluded.avg_energy,
            avg_sleep=excluded.avg_sleep, avg_water=excluded.avg_water,
            workouts_completed=excluded.workouts_completed,
            days_diet_followed=excluded.days_diet_followed,
            weight_change=excluded.weight_change,
            ai_summary=excluded.ai_summary, ai_suggestion=excluded.ai_suggestion
    """, (username, week_start, week_end, avg_mood, avg_energy, avg_sleep,
          avg_water, workouts_completed, days_diet, weight_change, ai_summary, ai_suggestion, now))
    con.commit(); con.close()


def get_weekly_reviews(username, limit=12):
    con = _conn()
    rows = con.execute(
        "SELECT * FROM weekly_reviews WHERE username=? ORDER BY week_start DESC LIMIT ?",
        (username, limit)
    ).fetchall()
    con.close()
    return [dict(r) for r in rows]


def get_latest_weekly_review(username):
    con = _conn()
    row = con.execute(
        "SELECT * FROM weekly_reviews WHERE username=? ORDER BY week_start DESC LIMIT 1",
        (username,)
    ).fetchone()
    con.close()
    return dict(row) if row else None


# ──────────────────────────────────────────────────────────────
# SAVED WORKOUT PLANS
# ──────────────────────────────────────────────────────────────

def save_workout_plan(username, plan_name, goal, duration_months, plan_data, set_active=True):
    con = _conn()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if set_active:
        con.execute("UPDATE saved_workout_plans SET is_active=0 WHERE username=?", (username,))
    con.execute("""
        INSERT INTO saved_workout_plans(username,plan_name,goal,duration_months,plan_data,is_active,created_at)
        VALUES(?,?,?,?,?,?,?)
    """, (username, plan_name, goal, duration_months, json.dumps(plan_data), 1 if set_active else 0, now))
    con.commit(); con.close()


def get_active_workout_plan(username):
    con = _conn()
    row = con.execute(
        "SELECT * FROM saved_workout_plans WHERE username=? AND is_active=1 ORDER BY created_at DESC LIMIT 1",
        (username,)
    ).fetchone()
    con.close()
    if row:
        d = dict(row)
        d["plan_data"] = json.loads(d["plan_data"])
        return d
    return None


def get_all_workout_plans(username):
    con = _conn()
    rows = con.execute(
        "SELECT id,plan_name,goal,duration_months,is_active,created_at FROM saved_workout_plans WHERE username=? ORDER BY created_at DESC",
        (username,)
    ).fetchall()
    con.close()
    return [dict(r) for r in rows]


def get_workout_plan_by_id(plan_id):
    con = _conn()
    row = con.execute("SELECT * FROM saved_workout_plans WHERE id=?", (plan_id,)).fetchone()
    con.close()
    if row:
        d = dict(row)
        d["plan_data"] = json.loads(d["plan_data"])
        return d
    return None


def activate_workout_plan(username, plan_id):
    con = _conn()
    con.execute("UPDATE saved_workout_plans SET is_active=0 WHERE username=?", (username,))
    con.execute("UPDATE saved_workout_plans SET is_active=1 WHERE id=?", (plan_id,))
    con.commit(); con.close()


def delete_workout_plan(plan_id):
    con = _conn()
    con.execute("DELETE FROM saved_workout_plans WHERE id=?", (plan_id,))
    con.commit(); con.close()


# ──────────────────────────────────────────────────────────────
# SAVED DIET PLANS
# ──────────────────────────────────────────────────────────────

def save_diet_plan(username, plan_name, goal, calories, plan_data, set_active=True):
    con = _conn()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if set_active:
        con.execute("UPDATE saved_diet_plans SET is_active=0 WHERE username=?", (username,))
    con.execute("""
        INSERT INTO saved_diet_plans(username,plan_name,goal,calories,plan_data,is_active,created_at)
        VALUES(?,?,?,?,?,?,?)
    """, (username, plan_name, goal, calories, json.dumps(plan_data), 1 if set_active else 0, now))
    con.commit(); con.close()


def get_active_diet_plan(username):
    con = _conn()
    row = con.execute(
        "SELECT * FROM saved_diet_plans WHERE username=? AND is_active=1 ORDER BY created_at DESC LIMIT 1",
        (username,)
    ).fetchone()
    con.close()
    if row:
        d = dict(row)
        d["plan_data"] = json.loads(d["plan_data"])
        return d
    return None


def get_all_diet_plans(username):
    con = _conn()
    rows = con.execute(
        "SELECT id,plan_name,goal,calories,is_active,created_at FROM saved_diet_plans WHERE username=? ORDER BY created_at DESC",
        (username,)
    ).fetchall()
    con.close()
    return [dict(r) for r in rows]


def delete_diet_plan(plan_id):
    con = _conn()
    con.execute("DELETE FROM saved_diet_plans WHERE id=?", (plan_id,))
    con.commit(); con.close()


# ──────────────────────────────────────────────────────────────
# CANVAS / JOURNAL
# ──────────────────────────────────────────────────────────────

def save_canvas_entry(username, content, mood="", tags=""):
    con = _conn()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    con.execute(
        "INSERT INTO canvas_entries(username,content,mood,tags,created_at) VALUES(?,?,?,?,?)",
        (username, content, mood, tags, now)
    )
    con.commit(); con.close()


def get_canvas_entries(username, limit=50):
    con = _conn()
    rows = con.execute(
        "SELECT * FROM canvas_entries WHERE username=? ORDER BY created_at DESC LIMIT ?",
        (username, limit)
    ).fetchall()
    con.close()
    return [dict(r) for r in rows]


def delete_canvas_entry(entry_id):
    con = _conn()
    con.execute("DELETE FROM canvas_entries WHERE id=?", (entry_id,))
    con.commit(); con.close()


# ──────────────────────────────────────────────────────────────
# DAILY WINS
# ──────────────────────────────────────────────────────────────

def save_wins(username, win_date, win1, win2, win3):
    con = _conn()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # one wins record per day (upsert by deleting old then inserting)
    con.execute("DELETE FROM daily_wins WHERE username=? AND win_date=?", (username, win_date))
    con.execute(
        "INSERT INTO daily_wins(username,win1,win2,win3,win_date,created_at) VALUES(?,?,?,?,?,?)",
        (username, win1 or "", win2 or "", win3 or "", win_date, now)
    )
    con.commit(); con.close()


def get_wins(username, limit=20):
    con = _conn()
    rows = con.execute(
        "SELECT * FROM daily_wins WHERE username=? ORDER BY win_date DESC LIMIT ?",
        (username, limit)
    ).fetchall()
    con.close()
    return [dict(r) for r in rows]


def delete_wins(win_id):
    con = _conn()
    con.execute("DELETE FROM daily_wins WHERE id=?", (win_id,))
    con.commit(); con.close()


# ──────────────────────────────────────────────────────────────
# TO-DO
# ──────────────────────────────────────────────────────────────

def add_todo(username, todo_date, task_text):
    con = _conn()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    con.execute(
        "INSERT INTO daily_todos(username,todo_date,task_text,is_done,created_at) VALUES(?,?,?,0,?)",
        (username, todo_date, task_text, now)
    )
    con.commit(); con.close()


def get_todos(username, todo_date):
    con = _conn()
    rows = con.execute(
        "SELECT * FROM daily_todos WHERE username=? AND todo_date=? ORDER BY created_at ASC",
        (username, todo_date)
    ).fetchall()
    con.close()
    return [dict(r) for r in rows]


def toggle_todo(todo_id, is_done):
    con = _conn()
    con.execute("UPDATE daily_todos SET is_done=? WHERE id=?", (1 if is_done else 0, todo_id))
    con.commit(); con.close()


def delete_todo(todo_id):
    con = _conn()
    con.execute("DELETE FROM daily_todos WHERE id=?", (todo_id,))
    con.commit(); con.close()


# ──────────────────────────────────────────────────────────────
# ANALYTICS HELPERS
# ──────────────────────────────────────────────────────────────

def get_streak(username):
    con = _conn()
    rows = con.execute(
        "SELECT entry_date FROM daily_diary WHERE username=? ORDER BY entry_date DESC",
        (username,)
    ).fetchall()
    con.close()
    dates = [r["entry_date"] for r in rows]
    if not dates:
        return 0
    streak = 0
    check = date.today()
    for ds in dates:
        d = date.fromisoformat(ds)
        if d == check:
            streak += 1
            check -= timedelta(days=1)
        elif d == check + timedelta(days=1):
            streak += 1
            check = d - timedelta(days=1)
        else:
            break
    return streak


def get_weekly_stats(username, week_start_str):
    """Aggregate diary entries for a given week (Mon-Sun)."""
    ws = date.fromisoformat(week_start_str)
    we = ws + timedelta(days=6)
    entries = get_diary_range(username, week_start_str, we.isoformat())
    if not entries:
        return None
    moods    = [e["mood"] for e in entries if e.get("mood")]
    energies = [e["energy_level"] for e in entries if e.get("energy_level")]
    sleeps   = [e["sleep_hours"] for e in entries if e.get("sleep_hours")]
    waters   = [e["water_glasses"] for e in entries if e.get("water_glasses")]
    workouts = sum(1 for e in entries if e.get("workout_done") == 1)
    diets    = sum(1 for e in entries if e.get("diet_followed") == 1)
    return {
        "avg_mood":    round(sum(moods)/len(moods), 1) if moods else None,
        "avg_energy":  round(sum(energies)/len(energies), 1) if energies else None,
        "avg_sleep":   round(sum(sleeps)/len(sleeps), 1) if sleeps else None,
        "avg_water":   round(sum(waters)/len(waters), 1) if waters else None,
        "workouts_completed": workouts,
        "days_diet_followed": diets,
        "days_logged": len(entries),
        "entries": entries,
    }
