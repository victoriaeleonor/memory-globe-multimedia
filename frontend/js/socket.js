// socket.js — Conexión WebSocket en tiempo real
// Requiere: <script src="https://cdn.socket.io/4.7.5/socket.io.min.js"></script>

const socket = io("http://localhost:5000");

socket.on("connect", () => {
  console.log("Conectado al servidor en tiempo real");
});

socket.on("pin_added", (pin) => {
  // Cuando el otro usuario agrega un pin, aparece en el globo
  console.log("Nuevo pin recibido:", pin);
  window.addPinToGlobe(pin);  // definida en globe.js
});

socket.on("disconnect", () => {
  console.log("Desconectado del servidor");
});

function emitNewPin(pin) {
  socket.emit("new_pin", pin);
}
