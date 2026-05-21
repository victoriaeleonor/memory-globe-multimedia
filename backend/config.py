import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

UPLOAD_FOLDER_PHOTOS = os.path.join(BASE_DIR, "uploads", "photos")
UPLOAD_FOLDER_AUDIOS = os.path.join(BASE_DIR, "uploads", "audios")
ALLOWED_PHOTO_EXTENSIONS = {"jpg", "jpeg", "png", "webp"}
ALLOWED_AUDIO_EXTENSIONS = {"mp3", "wav", "ogg", "m4a", "webm"}
MAX_CONTENT_LENGTH = 50 * 1024 * 1024  # 50 MB

DATABASE = os.path.join(BASE_DIR, "memory_globe.db")
SECRET_KEY = "dev-secret-key"  # cambiar en produccion
