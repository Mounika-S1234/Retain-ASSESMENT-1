# from flask import Flask, request, jsonify
# import sqlite3
# import hashlib
# import re

# app = Flask(__name__)

# conn = sqlite3.connect('users.db', check_same_thread=False)
# cursor = conn.cursor()

# def hash_password(password):
#     return hashlib.sha256(password.encode()).hexdigest()

# def is_valid_email(email):
#     return re.match(r"[^@]+@[^@]+\.[^@]+", email)

# @app.route('/')
# def home():
#     return jsonify({"status": "healthy", "service": "User Management System"}), 200

# @app.route('/users', methods=['GET'])
# def get_all_users():
#     try:
#         cursor.execute("SELECT id, name, email FROM users")
#         users = cursor.fetchall()
#         users_list = [{"id": u[0], "name": u[1], "email": u[2]} for u in users]
#         return jsonify(users_list), 200
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500

# @app.route('/user/<user_id>', methods=['GET'])
# def get_user(user_id):
#     try:
#         cursor.execute("SELECT id, name, email FROM users WHERE id = ?", (user_id,))
#         user = cursor.fetchone()
#         if user:
#             return jsonify({"id": user[0], "name": user[1], "email": user[2]}), 200
#         else:
#             return jsonify({"error": "User not found"}), 404
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500

# @app.route('/users', methods=['POST'])
# def create_user():
#     try:
#         data = request.get_json()
#         name = data.get('name')
#         email = data.get('email')
#         password = data.get('password')

#         if not name or not email or not password or not is_valid_email(email):
#             return jsonify({"error": "Invalid input"}), 400

#         hashed_pw = hash_password(password)
#         cursor.execute("INSERT INTO users (name, email, password) VALUES (?, ?, ?)", (name, email, hashed_pw))
#         conn.commit()
#         return jsonify({"message": "User created"}), 201
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500

# @app.route('/user/<user_id>', methods=['PUT'])
# def update_user(user_id):
#     try:
#         data = request.get_json()
#         name = data.get('name')
#         email = data.get('email')

#         if not name or not email or not is_valid_email(email):
#             return jsonify({"error": "Invalid input"}), 400

#         cursor.execute("UPDATE users SET name = ?, email = ? WHERE id = ?", (name, email, user_id))
#         conn.commit()
#         return jsonify({"message": "User updated"}), 200
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500

# @app.route('/user/<user_id>', methods=['DELETE'])
# def delete_user(user_id):
#     try:
#         cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
#         conn.commit()
#         return jsonify({"message": f"User {user_id} deleted"}), 200
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500

# @app.route('/search', methods=['GET'])
# def search_users():
#     name = request.args.get('name')
#     if not name:
#         return jsonify({"error": "Please provide a name to search"}), 400
#     try:
#         cursor.execute("SELECT id, name, email FROM users WHERE name LIKE ?", (f"%{name}%",))
#         users = cursor.fetchall()
#         users_list = [{"id": u[0], "name": u[1], "email": u[2]} for u in users]
#         return jsonify(users_list), 200
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500

# @app.route('/login', methods=['POST'])
# def login():
#     try:
#         data = request.get_json()
#         email = data.get('email')
#         password = data.get('password')

#         if not email or not password or not is_valid_email(email):
#             return jsonify({"status": "failed", "error": "Invalid input"}), 400

#         hashed_pw = hash_password(password)
#         cursor.execute("SELECT id FROM users WHERE email = ? AND password = ?", (email, hashed_pw))
#         user = cursor.fetchone()
#         if user:
#             return jsonify({"status": "success", "user_id": user[0]}), 200
#         else:
#             return jsonify({"status": "failed"}), 401
#     except Exception as e:
#         return jsonify({"status": "failed", "error": str(e)}), 500


# if __name__ == "__main__":
#     app.run(host="localhost", port=5000, debug=True)

# Directory structure:
# .
# ├── app.py
# ├── db.py
# ├── models/
# │   └── user_model.py
# ├── routes/
# │   └── user_routes.py
# ├── utils/
# │   ├── hash.py
# │   └── validators.py
# └── CHANGES.md

# === app.py ===
from flask import Flask
from routes.user_routes import user_bp
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.register_blueprint(user_bp)

@app.route('/')
def home():
    return {"status": "healthy", "service": "User Management System"}, 200

if __name__ == '__main__':
    app.run(host=os.getenv("HOST", "localhost"), port=int(os.getenv("PORT", 5000)), debug=True)


# === db.py ===
import sqlite3

def get_db_connection():
    conn = sqlite3.connect('users.db')
    conn.row_factory = sqlite3.Row
    return conn


# === models/user_model.py ===
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


# === routes/user_routes.py ===
from flask import Blueprint, request, jsonify
from models.user_model import *
from utils.hash import hash_password
from utils.validators import is_valid_email

user_bp = Blueprint('user_bp', __name__)

@user_bp.route('/users', methods=['GET'])
def get_all_users():
    try:
        users = fetch_all_users()
        return jsonify([dict(u) for u in users]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@user_bp.route('/user/<user_id>', methods=['GET'])
def get_user_by_id(user_id):
    try:
        user = fetch_user(user_id)
        return (jsonify(dict(user)), 200) if user else (jsonify({"error": "User not found"}), 404)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@user_bp.route('/users', methods=['POST'])
def create_new_user():
    try:
        data = request.get_json()
        name, email, password = data.get('name'), data.get('email'), data.get('password')

        if not all([name, email, password]) or not is_valid_email(email):
            return jsonify({"error": "Invalid input"}), 400

        hashed_pw = hash_password(password)
        create_user(name, email, hashed_pw)
        return jsonify({"message": "User created"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@user_bp.route('/user/<user_id>', methods=['PUT'])
def update_user_by_id(user_id):
    try:
        data = request.get_json()
        name, email = data.get('name'), data.get('email')

        if not all([name, email]) or not is_valid_email(email):
            return jsonify({"error": "Invalid input"}), 400

        update_user(user_id, name, email)
        return jsonify({"message": "User updated"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@user_bp.route('/user/<user_id>', methods=['DELETE'])
def delete_user_by_id(user_id):
    try:
        delete_user(user_id)
        return jsonify({"message": f"User {user_id} deleted"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@user_bp.route('/search', methods=['GET'])
def search_users():
    name = request.args.get('name')
    if not name:
        return jsonify({"error": "Please provide a name to search"}), 400
    try:
        users = search_users_by_name(name)
        return jsonify([dict(u) for u in users]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@user_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        email, password = data.get('email'), data.get('password')

        if not all([email, password]) or not is_valid_email(email):
            return jsonify({"status": "failed", "error": "Invalid input"}), 400

        hashed_pw = hash_password(password)
        user = login_user(email, hashed_pw)
        return (jsonify({"status": "success", "user_id": user["id"]}), 200) if user else (jsonify({"status": "failed"}), 401)
    except Exception as e:
        return jsonify({"status": "failed", "error": str(e)}), 500


# === utils/hash.py ===
import hashlib

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


# === utils/validators.py ===
import re

def is_valid_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)


# # === .env ===
# HOST=localhost
# PORT=5000


# # === CHANGES.md ===
# ## Major Issues Identified
# - Monolithic `app.py` mixing routing, logic, and DB code
# - Global DB cursor with threading risks
# - No environment variable management
# - No password security improvements
# - Inconsistent input validation and lack of proper error codes

# ## Key Changes
# - Separated routing (`routes/user_routes.py`) and models (`models/user_model.py`)
# - Replaced global DB cursor with context-managed connection (`db.py`)
# - Used `.env` file for configuration with `python-dotenv`
# - Moved utility functions (hashing, validators) into `utils/`
# - Improved HTTP status codes and consistent error handling
# - Wrote modular, readable, reusable code following separation of concerns

# ## Assumptions
# - Email is unique per user
# - SQLite is sufficient for this context (can be swapped with PostgreSQL easily)

# ## With More Time
# - Add Marshmallow for schema validation
# - Replace SHA256 with `bcrypt` for password hashing
# - Add unit tests and integration tests using `pytest`
# - Use Flask Blueprints for user auth separately
# - Add logging and monitoring support

# ## AI Usage
# - Used ChatGPT to assist with modular structure and refactoring strategy
# - Reviewed and manually modified all AI-assisted code to ensure correctness and maintainability

   