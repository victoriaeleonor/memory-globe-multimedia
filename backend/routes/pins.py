from flask import Blueprint, request, jsonify
import database

pins_bp = Blueprint("pins", __name__)

def pin_to_dict(pin):
    p = dict(pin)
    p["photo_url"] = f"/api/media/photos/{p['photo_filename']}" if p.get("photo_filename") else None
    p["audio_url"] = f"/api/media/audios/{p['audio_filename']}" if p.get("audio_filename") else None
    return p

@pins_bp.route("/", methods=["GET"])
def get_pins():
    conn = database.get_db()
    pins = conn.execute("""
        SELECT pins.*, users.username
        FROM pins JOIN users ON pins.user_id = users.id
        ORDER BY pins.created_at DESC
    """).fetchall()
    conn.close()

    return jsonify([pin_to_dict(p) for p in pins]), 200

@pins_bp.route("/", methods=["POST"])
def create_pin():
    data = request.get_json()
    required = ["user_id", "title", "latitude", "longitude", "photo_filename", "audio_filename"]
    if not all(data.get(f) for f in required):
        return jsonify({"error": "Mandatory fields missing"}), 400

    conn = database.get_db()
    cursor = conn.execute("""
        INSERT INTO pins (user_id, title, description, latitude, longitude, photo_filename, audio_filename)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        data["user_id"], data["title"], data.get("description", ""),
        data["latitude"], data["longitude"],
        data["photo_filename"], data["audio_filename"]
    ))
    conn.commit()

    pin_id = cursor.lastrowid
    pin = conn.execute("""
        SELECT pins.*, users.username FROM pins
        JOIN users ON pins.user_id = users.id WHERE pins.id = ?
    """, (pin_id,)).fetchone()
    conn.close()

    return jsonify(pin_to_dict(pin)), 201

@pins_bp.route("/<int:pin_id>", methods=["DELETE"])
def delete_pin(pin_id):
    conn = database.get_db()
    conn.execute("DELETE FROM pins WHERE id = ?", (pin_id,))
    conn.commit()
    conn.close()
    return jsonify({"message": "Pin deleted"}), 200
