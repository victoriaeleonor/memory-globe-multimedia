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
    
    password_bytes = password.encode('utf-8')
    hash_password = bcrypt.hashpw(password_bytes, bcrypt.gensalt())
    save_hash = hash_password.decode('utf-8')


    conn = database.get_db()
    try:
        conn.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (username, save_hash)  #hashear password con bcrypt
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
        "SELECT * FROM users WHERE username = ?",
        (username, )
    ).fetchone()
    conn.close()

    if user:
        #si fetchone() devuelve tupla
        saved_password_hs = user["password"]
        password_bytes = password.encode('utf-8')
        hash_bytes = saved_password_hs.encode('utf-8')

        if bcrypt.checkpw(password_bytes, hash_bytes):
            return jsonify({"message": "Login success", "user_id": user["id"], "username": user["username"]}), 200

    return jsonify({"error": "Wrong credentials"}), 401
