import sqlite3

def initialize_db():
    conn = sqlite3.connect('achievement_diary.db')
    conn.execute("PRAGMA foreign_keys = ON;")
    cursor = conn.cursor()

    # Create 'types' table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS types (
        type_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE
    );
    ''')

    cursor.execute('''
    INSERT OR IGNORE INTO types (name) VALUES ('writing');
    ''')

    # Create 'difficulty' table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS difficulty (
        difficulty_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE
    );
    ''')

    cursor.executemany('''
    INSERT OR IGNORE INTO difficulty (name) VALUES (?);
    ''', [('easy',), ('medium',), ('hard',)])

    # Create 'tasks' table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        description TEXT NOT NULL,
        archived BOOLEAN NOT NULL DEFAULT 0,
        completed BOOLEAN NOT NULL DEFAULT 0,
        type_id INTEGER NOT NULL,
        difficulty_id INTEGER NOT NULL,
        FOREIGN KEY (type_id) REFERENCES types(type_id),
        FOREIGN KEY (difficulty_id) REFERENCES difficulty(difficulty_id)
    );
    ''')

    conn.commit()
    conn.close()

def get_conn():
    conn = sqlite3.connect('achievement_diary.db')
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

# Run setup if this script is run directly
if __name__ == "__main__":
    initialize_db()
