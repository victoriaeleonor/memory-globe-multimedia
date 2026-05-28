// app.js — Lógica principal y estado de la aplicación

window.currentUser = null; // { id, username }

// ── Auth ──────────────────────────────────────────────
//Login
async function login(username, password) {
  const res = await fetch("/api/auth/login", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ username, password }),
  });
  const data = await res.json();
  if (!res.ok) throw new Error(data.error);
  window.currentUser = { id: data.user_id, username: data.username };
  return window.currentUser;
}

//Register
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
  return pins;
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

//Escucha el submit del formulario login
document.getElementById("login-form").addEventListener("submit", async (e) => {
  e.preventDefault(); //avoids the page to reload

  const username = document.getElementById("first").value;
  const password = document.getElementById("password").value;

  try {
    await login(username, password);
    // si llegamos acá, el login fue exitoso
    document.getElementById("login-screen").style.display = "none";
    // acá después cargaremos los pins y mostraremos el globo
  } catch (err) {
    document.getElementById("auth-error").textContent = err.message;
  }
});
