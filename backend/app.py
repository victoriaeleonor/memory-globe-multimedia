from flask import Flask, send_from_directory, request
from flask_socketio import SocketIO, emit
from flask_cors import CORS
import config
import database

app = Flask(__name__, static_folder="../frontend")
app.config["SECRET_KEY"] = config.SECRET_KEY
app.config["MAX_CONTENT_LENGTH"] = config.MAX_CONTENT_LENGTH

CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

# Track online users: { sid: {id, username} }
online_users = {}

# Register blueprints
from routes.auth import auth_bp
from routes.pins import pins_bp
from routes.media import media_bp
app.register_blueprint(auth_bp, url_prefix="/api/auth")
app.register_blueprint(pins_bp, url_prefix="/api/pins")
app.register_blueprint(media_bp, url_prefix="/api/media")

# Serve frontend
@app.route("/")
def index():
    return send_from_directory("../frontend", "index.html")

@app.route("/<path:path>")
def static_files(path):
    return send_from_directory("../frontend", path)

# ── Socket events ───────────────────────────────────────

@socketio.on("connect")
def handle_connect():
    pass  # user registers via "user_online" event after login

@socketio.on("user_online")
def handle_user_online(data):
    sid = request.sid
    online_users[sid] = {"id": data["id"], "username": data["username"]}
    socketio.emit("online_users", list(online_users.values()))

@socketio.on("disconnect")
def handle_disconnect():
    sid = request.sid
    online_users.pop(sid, None)
    socketio.emit("online_users", list(online_users.values()))

@socketio.on("new_pin")
def handle_new_pin(data):
    socketio.emit("pin_added", data)

if __name__ == "__main__":
    database.init_db()
    socketio.run(app, debug=True, port=5000)
