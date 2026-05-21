# Memory Globe 🌍🖼️📌

Minimalist social media of geolocalized memories. Two users share pictures and audio (music) attach in a 3D interactive globe in real time.

## Stack

- **Backend:** Python + Flask + Flask-SocketIO
- **Frontend:** HTML/CSS/JS + Globe.gl
- **Database:** SQLite
- **Real time:** WebSockets

## Instalation

```bash
# 1. Clone repo
git clone https://github.com/tu-usuario/memory-globe.git
cd memory-globe

# 2. Create virtual environment and install dependencies
cd backend
# --activate venv--
#python -m venv venv
#source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt

# 3. Initialize server
python app.py
```

Open http://localhost:5000 in browser.

## Supported audio formats

File upload: mp3, wav, ogg, m4a
Recording from browser: webm 
