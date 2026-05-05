import sqlite3
from datetime import datetime
import os

DB_PATH = "Database/FALCON.db"

# Ensure Database folder exists
os.makedirs("Database", exist_ok=True)

def create_table():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS conversations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user TEXT,
        assistant TEXT,
        timestamp TEXT
    )
    """)

    conn.commit()
    conn.close()


def save_conversation(user, assistant):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute(
        "INSERT INTO conversations (user, assistant, timestamp) VALUES (?, ?, ?)",
        (user, assistant, time)
    )

    conn.commit()
    conn.close()


create_table()