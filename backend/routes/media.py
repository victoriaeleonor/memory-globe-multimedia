from flask import Blueprint, request, jsonify, send_from_directory
import os
import uuid
import config

media_bp = Blueprint("media", __name__)

def allowed_file(filename, allowed_set):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in allowed_set

@media_bp.route("/upload/photo", methods=["POST"])
def upload_photo():
    if "file" not in request.files:
        return jsonify({"error": "No se envio archivo"}), 400

    file = request.files["file"]
    if not allowed_file(file.filename, config.ALLOWED_PHOTO_EXTENSIONS):
        return jsonify({"error": "Formato no permitido"}), 400

    ext = file.filename.rsplit(".", 1)[1].lower()
    filename = f"{uuid.uuid4().hex}.{ext}"
    file.save(os.path.join(config.UPLOAD_FOLDER_PHOTOS, filename))

    return jsonify({"filename": filename}), 201

@media_bp.route("/upload/audio", methods=["POST"])
def upload_audio():
    if "file" not in request.files:
        return jsonify({"error": "No se envio archivo"}), 400

    file = request.files["file"]
    if not allowed_file(file.filename, config.ALLOWED_AUDIO_EXTENSIONS):
        return jsonify({"error": "Formato no permitido. Permitidos: mp3, wav, ogg, m4a, webm"}), 400

    ext = file.filename.rsplit(".", 1)[1].lower()
    filename = f"{uuid.uuid4().hex}.{ext}"
    file.save(os.path.join(config.UPLOAD_FOLDER_AUDIOS, filename))

    return jsonify({"filename": filename}), 201

@media_bp.route("/photos/<filename>")
def serve_photo(filename):
    return send_from_directory(config.UPLOAD_FOLDER_PHOTOS, filename)

@media_bp.route("/audios/<filename>")
def serve_audio(filename):
    return send_from_directory(config.UPLOAD_FOLDER_AUDIOS, filename)
