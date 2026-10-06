// app.js — Main frontend client application for ZeroFilter

import { parseEpisodes, formatTime } from "./episodes.js";
import { categoryOf } from "./categories.js";

const $ = (id) => document.getElementById(id);
const $$ = (sel) => document.querySelectorAll(sel);

let episodes = [];
let currentEpisode = null;
let activeFilter = "all";
let activeCam = "loop"; // "loop" | "host" | "bunker" | "story"

const audio = $("main-audio");
const btnPlay = $("btn-play");
const playIcon = $("play-icon");
const seekBar = $("seek-bar");
const seekProgress = $("seek-progress");
const currentTimeEl = $("current-time");
const totalTimeEl = $("total-time");
const heroVideo = $("hero-video");
const hostLayer = $("host-layer");
const bunkerLayer = $("bunker-layer");
const stageOverlay = $("stage-overlay");
const stageImg = $("stage-img");
const stageCaption = $("stage-caption");
const cueText = $("cue-text");
const episodesGrid = $("episodes-grid");

// Spectrum visualizer
const canvas = $("audio-spectrum");
let canvasCtx = null;
let audioCtx = null;
let analyser = null;
let source = null;
let animFrameId = null;

// Dossier modal
const dossierModal = $("dossier-modal");
const btnOpenDossier = $("btn-open-dossier");
const btnCloseDossier = $("btn-close-dossier");
const dossierBackdrop = $("dossier-backdrop");
const btnTestVoice = $("btn-test-voice");
const sampleAudio = $("sample-audio");

// Initialize application
async function init() {
  if (canvas) {
    canvasCtx = canvas.getContext("2d");
    drawDefaultSpectrum();
  }

  try {
    const res = await fetch("data/episodes.json?nocache=" + Date.now());
    const data = await res.json();
    episodes = parseEpisodes(data);
  } catch (err) {
    console.error("Failed to load episodes manifest:", err);
  }

  if (episodes.length > 0) {
    loadEpisode(episodes[0], false);
  }

  renderFeed();
  setupEventListeners();
  setupSpectrumVisualizer();
}

function switchCamera(cam) {
  activeCam = cam;
  $$(".cam-btn").forEach(btn => {
    btn.classList.toggle("active", btn.getAttribute("data-cam") === cam);
  });

  // Reset layers
  hostLayer.classList.add("hidden");
  bunkerLayer.classList.add("hidden");
  stageOverlay.classList.add("hidden");

  if (cam === "loop") {
    // Let video display
  } else if (cam === "host") {
    hostLayer.classList.remove("hidden");
  } else if (cam === "bunker") {
    bunkerLayer.classList.remove("hidden");
  } else if (cam === "story") {
    // Show current synchronized story frame
    syncPlayback();
  }
}

function loadEpisode(ep, autoPlay = true) {
  currentEpisode = ep;

  // Update spotlight UI
  $("ep-title").textContent = ep.title;
  $("ep-subject").textContent = ep.subject;
  $("ep-category").textContent = categoryOf(ep.category).label.toUpperCase();
  $("ep-duration").textContent = `⏱ ${formatTime(ep.seconds)} MIN`;
  $("ep-time").textContent = `${ep.date} · ${ep.hour || "HOURLY"} UTC`;

  // Update media
  if (heroVideo) {
    heroVideo.poster = ep.thumb;
    if (ep.cover_video) {
      heroVideo.src = ep.cover_video;
      heroVideo.load();
      heroVideo.play().catch(() => {});
    }
  }

  // Update audio
  audio.src = ep.audio;
  audio.currentTime = 0;
  seekBar.max = ep.seconds || 180;
  seekBar.value = 0;
  totalTimeEl.textContent = formatTime(ep.seconds);
  currentTimeEl.textContent = "0:00";

  cueText.textContent = `"${ep.paragraphs[0] || 'Broadcasting now...'}"`;

  // Reset to active camera
  switchCamera(activeCam);

  if (autoPlay) {
    playAudio();
  } else {
    pauseAudio();
  }
}

function playAudio() {
  initAudioContext();
  audio.play().then(() => {
    btnPlay.classList.add("playing");
    playIcon.textContent = "❚❚";
    startSpectrumLoop();
  }).catch((err) => {
    console.warn("Autoplay blocked or audio not yet loaded:", err);
  });
}

function pauseAudio() {
  audio.pause();
  btnPlay.classList.remove("playing");
  playIcon.textContent = "▶";
}

function togglePlay() {
  if (audio.paused) {
    playAudio();
  } else {
    pauseAudio();
  }
}

function syncPlayback() {
  const t = audio.currentTime;
  seekBar.value = t;
  currentTimeEl.textContent = formatTime(t);

  if (!currentEpisode) return;

  // Subtitle cue sync by estimated paragraph timing
  const nParas = currentEpisode.paragraphs.length;
  const paraDuration = (currentEpisode.seconds || 180) / nParas;
  const paraIdx = Math.min(nParas - 1, Math.floor(t / paraDuration));
  if (currentEpisode.paragraphs[paraIdx]) {
    cueText.textContent = `"${currentEpisode.paragraphs[paraIdx]}"`;
  }

  // Synchronized Stage Overlay
  const frames = currentEpisode.art?.frames || [];
  if (frames.length > 0) {
    let activeFrame = null;
    for (const f of frames) {
      if (t >= f.t) activeFrame = f;
    }

    if (activeFrame && activeFrame.src) {
      if (stageImg.src !== activeFrame.src) {
        stageImg.src = activeFrame.src;
      }
      stageCaption.textContent = activeFrame.caption || "";
      if (activeCam === "story") {
        stageOverlay.classList.remove("hidden");
      }
    } else {
      if (activeCam === "story") stageOverlay.classList.add("hidden");
    }
  } else {
    if (activeCam === "story") stageOverlay.classList.add("hidden");
  }
}

// Spectrum Visualizer
function setupSpectrumVisualizer() {
  window.addEventListener("resize", resizeCanvas);
  resizeCanvas();
}

function resizeCanvas() {
  if (!canvas) return;
  canvas.width = canvas.parentElement.clientWidth || 500;
  canvas.height = 36;
}

function initAudioContext() {
  if (audioCtx) {
    if (audioCtx.state === "suspended") audioCtx.resume();
    return;
  }
  try {
    const AudioContext = window.AudioContext || window.webkitAudioContext;
    audioCtx = new AudioContext();
    analyser = audioCtx.createAnalyser();
    analyser.fftSize = 64;
    analyser.smoothingTimeConstant = 0.8;
    source = audioCtx.createMediaElementSource(audio);
    source.connect(analyser);
    analyser.connect(audioCtx.destination);
  } catch (err) {
    console.warn("AudioContext init error:", err);
  }
}

function drawDefaultSpectrum() {
  if (!canvasCtx || !canvas) return;
  canvasCtx.clearRect(0, 0, canvas.width, canvas.height);
  const bars = 32;
  const barWidth = canvas.width / bars - 2;
  for (let i = 0; i < bars; i++) {
    const h = 3;
    const x = i * (barWidth + 2);
    canvasCtx.fillStyle = "rgba(0, 229, 255, 0.2)";
    canvasCtx.fillRect(x, canvas.height - h, barWidth, h);
  }
}

function startSpectrumLoop() {
  if (animFrameId) cancelAnimationFrame(animFrameId);

  const bufferLength = analyser ? analyser.frequencyBinCount : 32;
  const dataArray = new Uint8Array(bufferLength);

  function renderFrame() {
    animFrameId = requestAnimationFrame(renderFrame);

    if (audio.paused) {
      drawDefaultSpectrum();
      cancelAnimationFrame(animFrameId);
      return;
    }

    if (analyser) {
      analyser.getByteFrequencyData(dataArray);
    } else {
      // Simulated responsive pulse if Web Audio is restricted
      for (let i = 0; i < bufferLength; i++) {
        dataArray[i] = Math.floor(Math.sin(Date.now() / 150 + i * 0.4) * 80 + 120);
      }
    }

    canvasCtx.clearRect(0, 0, canvas.width, canvas.height);
    const bars = 32;
    const barWidth = (canvas.width / bars) - 2;

    for (let i = 0; i < bars; i++) {
      const val = dataArray[i] || 0;
      const percent = val / 255;
      const h = Math.max(3, percent * (canvas.height - 4));
      const x = i * (barWidth + 2);
      const y = canvas.height - h;

      // Color gradient from cyber cyan to amber at peak
      const gradient = canvasCtx.createLinearGradient(0, y, 0, canvas.height);
      if (percent > 0.75) {
        gradient.addColorStop(0, "#ffb300");
        gradient.addColorStop(1, "#00e5ff");
      } else {
        gradient.addColorStop(0, "#00e5ff");
        gradient.addColorStop(1, "rgba(0, 229, 255, 0.3)");
      }

      canvasCtx.fillStyle = gradient;
      canvasCtx.fillRect(x, y, barWidth, h);
    }
  }

  renderFrame();
}

function renderFeed() {
  episodesGrid.innerHTML = "";
  const filtered = activeFilter === "all" 
    ? episodes 
    : episodes.filter(e => e.category === activeFilter);

  $("feed-count").textContent = `${filtered.length} Release${filtered.length === 1 ? "" : "s"}`;

  filtered.forEach(ep => {
    const card = document.createElement("article");
    card.className = "episode-card";
    card.setAttribute("data-id", ep.id);

    card.innerHTML = `
      <div class="card-media">
        <video class="card-video" loop muted playsinline poster="${ep.thumb}">
          <source src="${ep.cover_video || ''}" type="video/mp4">
        </video>
        <span class="card-time-badge">${ep.hour || '00:00'} UTC</span>
      </div>
      <div class="card-body">
        <div class="card-tags">
          <span class="badge category-badge">${categoryOf(ep.category).label}</span>
        </div>
        <h3 class="card-title">${ep.title}</h3>
        <p class="card-desc">${ep.subject}</p>
        <div class="card-footer">
          <span class="card-duration">⏱ ${formatTime(ep.seconds)}</span>
          <button type="button" class="btn-card-play">LISTEN NOW ▶</button>
        </div>
      </div>
    `;

    // Looping preview on card hover
    const video = card.querySelector("video");
    card.addEventListener("mouseenter", () => {
      if (video && video.src) video.play().catch(() => {});
    });
    card.addEventListener("mouseleave", () => {
      if (video) video.pause();
    });

    card.addEventListener("click", () => {
      loadEpisode(ep, true);
      window.scrollTo({ top: 0, behavior: "smooth" });
    });

    episodesGrid.appendChild(card);
  });
}

function setupEventListeners() {
  btnPlay.addEventListener("click", togglePlay);

  audio.addEventListener("timeupdate", syncPlayback);
  audio.addEventListener("ended", () => {
    pauseAudio();
    audio.currentTime = 0;
    stageOverlay.classList.add("hidden");
  });

  seekBar.addEventListener("input", () => {
    audio.currentTime = Number(seekBar.value);
    syncPlayback();
  });

  // Camera angle switcher
  $$(".cam-btn").forEach(btn => {
    btn.addEventListener("click", () => {
      const cam = btn.getAttribute("data-cam");
      switchCamera(cam);
    });
  });

  // Playback speeds
  $$(".speed-btn").forEach(btn => {
    btn.addEventListener("click", () => {
      $$(".speed-btn").forEach(b => b.classList.remove("active"));
      btn.classList.add("active");
      audio.playbackRate = Number(btn.getAttribute("data-speed"));
    });
  });

  // Category filters
  $$(".nav-btn").forEach(btn => {
    btn.addEventListener("click", () => {
      $$(".nav-btn").forEach(b => b.classList.remove("active"));
      btn.classList.add("active");
      activeFilter = btn.getAttribute("data-filter");
      renderFeed();
    });
  });

  // Dossier modal handlers
  btnOpenDossier.addEventListener("click", () => {
    dossierModal.classList.remove("hidden");
    dossierModal.setAttribute("aria-hidden", "false");
  });

  const closeDossier = () => {
    dossierModal.classList.add("hidden");
    dossierModal.setAttribute("aria-hidden", "true");
    if (sampleAudio) sampleAudio.pause();
  };

  btnCloseDossier.addEventListener("click", closeDossier);
  dossierBackdrop.addEventListener("click", closeDossier);

  btnTestVoice.addEventListener("click", () => {
    if (sampleAudio.paused) {
      sampleAudio.play();
      btnTestVoice.textContent = "PLAYING SAMPLE... ❚❚";
    } else {
      sampleAudio.pause();
      btnTestVoice.textContent = "TEST VOICE SYNTHESIS ▶";
    }
  });

  sampleAudio.addEventListener("ended", () => {
    btnTestVoice.textContent = "TEST VOICE SYNTHESIS ▶";
  });

  // Share episode button
  $("btn-share").addEventListener("click", () => {
    if (navigator.clipboard && currentEpisode) {
      navigator.clipboard.writeText(window.location.href);
      alert("ZeroFilter release link copied to clipboard!");
    }
  });

  // Keyboard navigation
  window.addEventListener("keydown", (e) => {
    if (e.target.tagName === "INPUT" || e.target.tagName === "TEXTAREA") return;
    if (e.code === "Space") {
      e.preventDefault();
      togglePlay();
    } else if (e.code === "Escape") {
      closeDossier();
    } else if (e.code === "ArrowRight") {
      audio.currentTime = Math.min(audio.duration || 180, audio.currentTime + 5);
    } else if (e.code === "ArrowLeft") {
      audio.currentTime = Math.max(0, audio.currentTime - 5);
    }
  });
}

init();
