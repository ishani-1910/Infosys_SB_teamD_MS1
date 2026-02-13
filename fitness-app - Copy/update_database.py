"""
Database Update Script
Run this to add the new tables to your existing database
"""
import sqlite3

DB_NAME = "routinex.db"

print("🔧 Updating database schema...")

conn = sqlite3.connect(DB_NAME)
c = conn.cursor()

# Check existing tables
c.execute("SELECT name FROM sqlite_master WHERE type='table';")
existing_tables = [row[0] for row in c.fetchall()]
print(f"✅ Existing tables: {', '.join(existing_tables)}")

# 4. WORKOUT CHECK-INS
if 'workout_checkins' not in existing_tables:
    print("➕ Creating workout_checkins table...")
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
    print("✅ workout_checkins table created")
else:
    print("⏭️  workout_checkins table already exists")

# 5. DAILY CHECK-IN LOGS
if 'daily_checkin_logs' not in existing_tables:
    print("➕ Creating daily_checkin_logs table...")
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
    print("✅ daily_checkin_logs table created")
else:
    print("⏭️  daily_checkin_logs table already exists")

# 6. CANVAS ENTRIES
if 'canvas_entries' not in existing_tables:
    print("➕ Creating canvas_entries table...")
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
    print("✅ canvas_entries table created")
else:
    print("⏭️  canvas_entries table already exists")

# 7. DAILY WINS
if 'daily_wins' not in existing_tables:
    print("➕ Creating daily_wins table...")
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
    print("✅ daily_wins table created")
else:
    print("⏭️  daily_wins table already exists")

conn.commit()

# Verify all tables
c.execute("SELECT name FROM sqlite_master WHERE type='table';")
all_tables = [row[0] for row in c.fetchall()]
print(f"\n✅ Final database tables: {', '.join(all_tables)}")

conn.close()

print("\n🎉 Database update complete!")
print("\n📋 Next steps:")
print("1. Make sure all Python files are updated (database.py, database_extended.py, etc.)")
print("2. Restart your Streamlit app: streamlit run app.py")
print("3. Test the features!")
