import sqlite3

conn = sqlite3.connect('habits.db')
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id TEXT PRIMARY KEY,
    username TEXT NOT NULL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS habits (
    id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    frequency TEXT NOT NULL,
    start_date TIMESTAMP NOT NULL,
    end_date TIMESTAMP NOT NULL,
    user_id TEXT,
    FOREIGN KEY (user_id) REFERENCES users(id)
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS records (
    id TEXT PRIMARY KEY,
    date TIMESTAMP NOT NULL,
    mood TEXT,
    notes TEXT,
    habit_id TEXT,
    FOREIGN KEY (habit_id) REFERENCES habits(id)
)
""")

conn.commit()
conn.close()
