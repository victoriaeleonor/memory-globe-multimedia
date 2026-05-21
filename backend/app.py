from flask import Flask, send_from_directory
from flask_socketio import SocketIO
from flask_cors import CORS
import os
import config
import database

app = Flask(__name__, static_folder="../frontend")
app.config["SECRET_KEY"] = config.SECRET_KEY
app.config["MAX_CONTENT_LENGTH"] = config.MAX_CONTENT_LENGTH

CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

# Registrar rutas
from routes.auth import auth_bp
from routes.pins import pins_bp
from routes.media import media_bp
app.register_blueprint(auth_bp, url_prefix="/api/auth")
app.register_blueprint(pins_bp, url_prefix="/api/pins")
app.register_blueprint(media_bp, url_prefix="/api/media")

# Servir el frontend
@app.route("/")
def index():
    return send_from_directory("../frontend", "index.html")

@app.route("/<path:path>")
def static_files(path):
    return send_from_directory("../frontend", path)

# WebSocket: nuevo pin en tiempo real
@socketio.on("new_pin")
def handle_new_pin(data):
    socketio.emit("pin_added", data, broadcast=True)

if __name__ == "__main__":
    database.init_db()
    socketio.run(app, debug=True, port=5000)
