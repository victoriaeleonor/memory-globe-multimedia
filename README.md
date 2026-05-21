# Memory Globe 🌍

Red social minimalista de recuerdos geolocalizados. Dos usuarios comparten fotos y audios anclados en un globo terráqueo 3D interactivo, en tiempo real.

## Stack

- **Backend:** Python + Flask + Flask-SocketIO
- **Frontend:** HTML/CSS/JS + Globe.gl
- **Base de datos:** SQLite
- **Tiempo real:** WebSockets

## Estructura

```
memory-globe/
├── backend/
│   ├── app.py              # Servidor principal + WebSockets
│   ├── database.py         # Inicialización y conexión SQLite
│   ├── config.py           # Configuración general
│   ├── requirements.txt    # Dependencias Python
│   ├── routes/
│   │   ├── auth.py         # Register / Login
│   │   ├── pins.py         # CRUD de pins
│   │   └── media.py        # Subida y servido de foto/audio
│   └── uploads/
│       ├── photos/         # Fotos subidas
│       └── audios/         # Audios subidos (mp3, wav, grabados)
└── frontend/
    ├── index.html          # Página principal
    ├── css/style.css       # Estilos
    ├── js/
    │   ├── app.js          # Lógica principal y estado
    │   ├── globe.js        # Globo 3D con Globe.gl
    │   ├── socket.js       # Conexión WebSocket tiempo real
    │   └── audio.js        # Grabación y reproducción de audio
    └── assets/             # Íconos y recursos estáticos
```

## Instalación

```bash
# 1. Clonar el repo
git clone https://github.com/tu-usuario/memory-globe.git
cd memory-globe

# 2. Crear entorno virtual e instalar dependencias
cd backend
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt

# 3. Inicializar la base de datos y correr el servidor
python app.py
```

Abrir http://localhost:5000 en el navegador.

## Formatos de audio soportados

Subida de archivo: mp3, wav, ogg, m4a
Grabación desde el navegador: webm (se convierte automáticamente)

## Equipo

- Persona A — Backend (API, WebSockets, base de datos)
- Persona B — Frontend (globo 3D, UI, audio)
