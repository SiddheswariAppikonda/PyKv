# auth_service/database.py
import os
import sqlite3
from typing import Optional, List, Dict

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "users.db")

def get_connection():
    return sqlite3.connect(DB_PATH)

# -------------------------
# Initialize table
# -------------------------
def create_users_table():
    conn = get_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

# -------------------------
# Add user
# -------------------------
def add_user(username: str, password: str):
    conn = get_connection()
    try:
        conn.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (username, password)
        )
        conn.commit()
    finally:
        conn.close()

# -------------------------
# Get single user
# -------------------------
def get_user(username: str) -> Optional[Dict[str, str]]:
    conn = get_connection()
    c = conn.cursor()
    c.execute(
        "SELECT id, username, password FROM users WHERE username = ?",
        (username,)
    )
    row = c.fetchone()
    conn.close()

    if row:
        return {
            "id": row[0],
            "username": row[1],
            "password": row[2]
        }
    return None

# -------------------------
# Get all users (NO passwords)
# -------------------------
def get_all_users() -> List[Dict[str, str]]:
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT id, username FROM users")
    rows = c.fetchall()
    conn.close()

    return [
        {"id": row[0], "username": row[1]}
        for row in rows
    ]

# Ensure table exists
create_users_table()
