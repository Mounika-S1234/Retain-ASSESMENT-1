from flask import Blueprint, request, jsonify
from models.user_model import (
    fetch_all_users,
    fetch_user,
    create_user,
    update_user,
    delete_user,
    search_users_by_name,
    login_user,
)
from utils.hash import hash_password
from utils.validators import is_valid_email

user_bp = Blueprint("user", __name__)

@user_bp.route("/users", methods=["GET"])
def get_all_users():
    try:
        users = fetch_all_users()
        users_list = [{"id": u["id"], "name": u["name"], "email": u["email"]} for u in users]
        return jsonify(users_list), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@user_bp.route("/user/<user_id>", methods=["GET"])
def get_user(user_id):
    try:
        user = fetch_user(user_id)
        if user:
            return jsonify({"id": user["id"], "name": user["name"], "email": user["email"]}), 200
        else:
            return jsonify({"error": "User not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@user_bp.route("/users", methods=["POST"])
def create_new_user():
    try:
        data = request.get_json()
        name = data.get("name")
        email = data.get("email")
        password = data.get("password")

        if not name or not email or not password or not is_valid_email(email):
            return jsonify({"error": "Invalid input"}), 400

        hashed_pw = hash_password(password)
        create_user(name, email, hashed_pw)
        return jsonify({"message": "User created"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@user_bp.route("/user/<user_id>", methods=["PUT"])
def update_existing_user(user_id):
    try:
        data = request.get_json()
        name = data.get("name")
        email = data.get("email")

        if not name or not email or not is_valid_email(email):
            return jsonify({"error": "Invalid input"}), 400

        update_user(user_id, name, email)
        return jsonify({"message": "User updated"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@user_bp.route("/user/<user_id>", methods=["DELETE"])
def delete_existing_user(user_id):
    try:
        delete_user(user_id)
        return jsonify({"message": f"User {user_id} deleted"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@user_bp.route("/search", methods=["GET"])
def search_users():
    name = request.args.get("name")
    if not name:
        return jsonify({"error": "Please provide a name to search"}), 400
    try:
        users = search_users_by_name(name)
        users_list = [{"id": u["id"], "name": u["name"], "email": u["email"]} for u in users]
        return jsonify(users_list), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@user_bp.route("/login", methods=["POST"])
def login():
    try:
        data = request.get_json()
        email = data.get("email")
        password = data.get("password")

        if not email or not password or not is_valid_email(email):
            return jsonify({"status": "failed", "error": "Invalid input"}), 400

        hashed_pw = hash_password(password)
        user = login_user(email, hashed_pw)
        if user:
            return jsonify({"status": "success", "user_id": user["id"]}), 200
        else:
            return jsonify({"status": "failed"}), 401
    except Exception as e:
        return jsonify({"status": "failed", "error": str(e)}), 500
