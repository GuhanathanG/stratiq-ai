import sqlite3
import bcrypt
import streamlit as st

# ===== CREATE USERS TABLE =====

def init_auth_db():
    conn = sqlite3.connect("stratiq.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password BLOB
    )
    """)

    conn.commit()
    conn.close()


# ===== REGISTER USER =====

def register_user(username, password):
    conn = sqlite3.connect("stratiq.db")
    cursor = conn.cursor()

    hashed_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

    try:
        cursor.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (username, hashed_pw)
        )
        conn.commit()
        conn.close()
        return True
    except:
        conn.close()
        return False


# ===== LOGIN USER =====

def login_user(username, password):
    conn = sqlite3.connect("stratiq.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT password FROM users WHERE username = ?",
        (username,)
    )

    result = cursor.fetchone()
    conn.close()

    if result:
        stored_password = result[0]
        return bcrypt.checkpw(password.encode(), stored_password)

    return False


# ===== AUTH STATE =====

def logout():
    st.session_state.authenticated = False
    st.session_state.username = None