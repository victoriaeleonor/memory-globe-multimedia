#user registration and login
from flask import Blueprint, request, jsonify, session
import database
import bcrypt

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    username = data.get("username", "").strip()
    password = data.get("password", "").strip()


    if not username or not password:
        return jsonify({"error": "Faltan campos"}), 400

    conn = database.get_db()
    try:
        conn.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (username, password)  #hashear password con bcrypt
        )
        conn.commit()
        return jsonify({"message": "User created"}), 201
    except Exception:
        return jsonify({"error": "User already exists"}), 409
    finally:
        conn.close()

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username", "").strip()
    password = data.get("password", "").strip()

    conn = database.get_db()
    user = conn.execute(
        "SELECT * FROM users WHERE username = ? AND password = ?",
        (username, password)
    ).fetchone()
    conn.close()

    if not user:
        return jsonify({"error": "Credenciales incorrectas"}), 401

    return jsonify({"message": "Login exitoso", "user_id": user["id"], "username": user["username"]}), 200
