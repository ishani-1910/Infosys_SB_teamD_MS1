"""
Database Migration Script for RoutineX
Fixes the daily_wins table to add the missing win_date column
"""

import sqlite3
from datetime import datetime

DB_NAME = "routinex.db"

def migrate_database():
    """
    Add win_date column to daily_wins table if it doesn't exist
    """
    print("=" * 60)
    print("RoutineX Database Migration")
    print("=" * 60)
    
    try:
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        
        # Check if win_date column exists
        c.execute("PRAGMA table_info(daily_wins)")
        columns = [col[1] for col in c.fetchall()]
        
        if 'win_date' not in columns:
            print("❌ win_date column is MISSING from daily_wins table")
            print("🔧 Adding win_date column...")
            
            # Add the column with a default value
            c.execute("ALTER TABLE daily_wins ADD COLUMN win_date TEXT DEFAULT '1970-01-01'")
            
            # Update existing records to use the created_at date
            c.execute("""
                UPDATE daily_wins 
                SET win_date = DATE(created_at) 
                WHERE win_date IS NULL OR win_date = '1970-01-01'
            """)
            
            conn.commit()
            print("✅ win_date column added successfully!")
            print(f"✅ Updated {c.rowcount} existing records")
        else:
            print("✅ win_date column already exists - no migration needed")
        
        # Verify the fix
        c.execute("SELECT COUNT(*) FROM daily_wins")
        count = c.fetchone()[0]
        print(f"📊 Total records in daily_wins table: {count}")
        
        conn.close()
        print("\n✅ Database migration completed successfully!")
        
    except sqlite3.Error as e:
        print(f"\n❌ Database error: {e}")
        print("\nTroubleshooting:")
        print("1. Make sure routinex.db exists in the same directory")
        print("2. Close any other programs that might be using the database")
        print("3. Check file permissions")
        return False
    
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        return False
    
    return True

if __name__ == "__main__":
    print("\nThis script will fix the daily_wins table structure.")
    print("It's safe to run multiple times.\n")
    
    input("Press Enter to continue...")
    
    success = migrate_database()
    
    if success:
        print("\n" + "=" * 60)
        print("Migration completed! You can now run the app normally.")
        print("=" * 60)
    else:
        print("\n" + "=" * 60)
        print("Migration failed. Please check the errors above.")
        print("=" * 60)
    
    input("\nPress Enter to exit...")
