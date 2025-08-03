from db import get_db_connection

def fetch_all_users():
    with get_db_connection() as conn:
        return conn.execute("SELECT id, name, email FROM users").fetchall()

def fetch_user(user_id):
    with get_db_connection() as conn:
        return conn.execute("SELECT id, name, email FROM users WHERE id = ?", (user_id,)).fetchone()

def create_user(name, email, hashed_pw):
    with get_db_connection() as conn:
        conn.execute("INSERT INTO users (name, email, password) VALUES (?, ?, ?)", (name, email, hashed_pw))
        conn.commit()

def update_user(user_id, name, email):
    with get_db_connection() as conn:
        conn.execute("UPDATE users SET name = ?, email = ? WHERE id = ?", (name, email, user_id))
        conn.commit()

def delete_user(user_id):
    with get_db_connection() as conn:
        conn.execute("DELETE FROM users WHERE id = ?", (user_id,))
        conn.commit()

def search_users_by_name(name):
    with get_db_connection() as conn:
        return conn.execute("SELECT id, name, email FROM users WHERE name LIKE ?", (f"%{name}%",)).fetchall()

def login_user(email, hashed_pw):
    with get_db_connection() as conn:
        return conn.execute("SELECT id FROM users WHERE email = ? AND password = ?", (email, hashed_pw)).fetchone()
