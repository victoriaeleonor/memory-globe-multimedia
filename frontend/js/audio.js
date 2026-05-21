// audio.js — Grabación y reproducción de audio

let mediaRecorder = null;
let recordedChunks = [];
let isRecording = false;

// Iniciar grabación desde el micrófono del navegador
async function startRecording() {
  const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
  mediaRecorder = new MediaRecorder(stream, { mimeType: "audio/webm" });
  recordedChunks = [];

  mediaRecorder.ondataavailable = (e) => {
    if (e.data.size > 0) recordedChunks.push(e.data);
  };

  mediaRecorder.start();
  isRecording = true;
  console.log("Grabando...");
}

// Detener y obtener el Blob de audio grabado
function stopRecording() {
  return new Promise((resolve) => {
    mediaRecorder.onstop = () => {
      const blob = new Blob(recordedChunks, { type: "audio/webm" });
      resolve(blob);
    };
    mediaRecorder.stop();
    isRecording = false;
  });
}

// Subir audio (grabado o archivo subido por el usuario)
async function uploadAudio(fileOrBlob, filename = "recording.webm") {
  const formData = new FormData();
  formData.append("file", fileOrBlob, filename);

  const res = await fetch("/api/media/upload/audio", {
    method: "POST",
    body: formData,
  });

  if (!res.ok) throw new Error("Error subiendo audio");
  const data = await res.json();
  return data.filename;
}

// Subir foto
async function uploadPhoto(file) {
  const formData = new FormData();
  formData.append("file", file);

  const res = await fetch("/api/media/upload/photo", {
    method: "POST",
    body: formData,
  });

  if (!res.ok) throw new Error("Error subiendo foto");
  const data = await res.json();
  return data.filename;
}

// Reproducir audio por filename
function playAudio(filename) {
  const audio = new Audio(`/api/media/audios/${filename}`);
  audio.play();
  return audio;
}
