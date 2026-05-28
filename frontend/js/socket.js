// socket.js — Real-time WebSocket connection

const socket = io("http://localhost:5000");

socket.on("connect", () => {
  console.log("Connected to real-time server");
  // If user was already logged in (e.g. reconnect after logout), re-announce
  if (window.currentUser) {
    socket.emit("user_online", { id: window.currentUser.id, username: window.currentUser.username });
  }
});

// When online users list changes → update sidebar
socket.on("online_users", (users) => {
  if (typeof renderOnlineUsers === "function") renderOnlineUsers(users);
});

// When any user adds a pin → update globe + sidebar for everyone
socket.on("pin_added", (pin) => {
  console.log("New pin received:", pin);
  if (!window._localPinIds) window._localPinIds = new Set();
  if (!window._localPinIds.has(pin.id)) {
    window.addPinToGlobe(pin);
    fetchAllPins().then(pins => {
      if (typeof renderSidebar === "function") renderSidebar(pins);
    });
  }
  window._localPinIds.delete(pin.id);
});

socket.on("disconnect", () => {
  console.log("Disconnected from server");
});

// Called after login to register as online
function announceOnline(user) {
  // Expose on window so the connect handler can re-announce on reconnect
  window.currentUser = user;
  if (socket.connected) {
    socket.emit("user_online", { id: user.id, username: user.username });
  } else {
    // Will be emitted in the "connect" handler above
    socket.connect();
  }
}

// Called when creating a pin — broadcasts to others
function emitNewPin(pin) {
  if (!window._localPinIds) window._localPinIds = new Set();
  window._localPinIds.add(pin.id);
  socket.emit("new_pin", pin);
}
