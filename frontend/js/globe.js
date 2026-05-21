// globe.js — Globo terráqueo 3D con Globe.gl
// Requiere: <script src="https://unpkg.com/globe.gl"></script>

let globe = null;
let pins = [];

function initGlobe(containerId) {
  globe = Globe()(document.getElementById(containerId))
    .globeImageUrl("//unpkg.com/three-globe/example/img/earth-blue-marble.jpg")
    .backgroundImageUrl("//unpkg.com/three-globe/example/img/night-sky.png")
    .pointsData(pins)
    .pointLat("latitude")
    .pointLng("longitude")
    .pointColor(() => "#1D9E75")
    .pointAltitude(0.02)
    .pointRadius(0.5)
    .pointLabel((d) => `<div style="background:#fff;padding:6px 10px;border-radius:8px;font-size:13px"><b>${d.title}</b><br/>${d.username}</div>`)
    .onPointClick((pin) => window.openPinModal(pin))
    .onGlobeClick(({ lat, lng }) => window.openNewPinForm(lat, lng));

  globe.controls().autoRotate = true;
  globe.controls().autoRotateSpeed = 0.5;
}

function addPinToGlobe(pin) {
  pins = [...pins, pin];
  globe.pointsData(pins);
}

function loadAllPins(pinsArray) {
  pins = pinsArray;
  globe.pointsData(pins);
}

// Parar la rotación cuando el usuario interactúa
function stopAutoRotate() {
  globe.controls().autoRotate = false;
}
