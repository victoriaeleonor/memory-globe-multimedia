// app.js — Lógica principal y estado de la aplicación

let currentUser = null;  // { id, username }

// ── Auth ──────────────────────────────────────────────
async function login(username, password) {
  const res = await fetch("/api/auth/login", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ username, password }),
  });
  const data = await res.json();
  if (!res.ok) throw new Error(data.error);
  currentUser = { id: data.user_id, username: data.username };
  return currentUser;
}

async function register(username, password) {
  const res = await fetch("/api/auth/register", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ username, password }),
  });
  const data = await res.json();
  if (!res.ok) throw new Error(data.error);
  return data;
}

// ── Pins ──────────────────────────────────────────────
async function fetchAllPins() {
  const res = await fetch("/api/pins/");
  const pins = await res.json();
  loadAllPins(pins);  // globe.js
}

async function createPin({ title, description, latitude, longitude, photoFile, audioFileOrBlob, audioFilename }) {
  const photo_filename = await uploadPhoto(photoFile);
  const audio_filename = await uploadAudio(audioFileOrBlob, audioFilename);

  const res = await fetch("/api/pins/", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      user_id: currentUser.id,
      title,
      description,
      latitude,
      longitude,
      photo_filename,
      audio_filename,
    }),
  });

  const pin = await res.json();
  addPinToGlobe(pin);   // globe.js — local
  emitNewPin(pin);      // socket.js — tiempo real al otro usuario
  return pin;
}

// ── Modales (implementar en index.html) ───────────────
function openPinModal(pin) {
  // Mostrar foto, descripción y reproducir audio del pin
  console.log("Abrir modal para pin:", pin);
}

function openNewPinForm(lat, lng) {
  // Mostrar formulario para crear pin en lat/lng
  console.log("Nuevo pin en:", lat, lng);
}
