# test_db_write.py
import sqlite3

def test_db():
    try:
        conn = sqlite3.connect("achievement_diary.db")
        conn.execute("PRAGMA foreign_keys = ON;")
        cursor = conn.cursor()

        cursor.execute('CREATE TABLE IF NOT EXISTS sanity_test (id INTEGER PRIMARY KEY, value TEXT)')
        cursor.execute('INSERT INTO sanity_test (value) VALUES (?)', ("test",))

        conn.commit()
        conn.close()
        print("✅ DB is not locked, write successful")
    except Exception as e:
        print("❌ DB is locked or errored:", e)

test_db()