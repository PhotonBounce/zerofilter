// app.js — Main frontend client application for ZeroFilter

import { parseEpisodes, formatTime, cueStarts, paragraphAt, escapeHtml } from "./episodes.js";
import { categoryOf } from "./categories.js";

const $ = (id) => document.getElementById(id);
const $$ = (sel) => document.querySelectorAll(sel);

let episodes = [];
let currentEpisode = null;
let currentStarts = [];
let currentPara = -1;
let activeFilter = "all";
let activeCam = "story"; // "loop" | "host" | "bunker" | "story"

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
let barGradients = null; // [normal, peak], rebuilt on resize — not 32 per frame
const BARS = 32;

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

  if (episodes.length === 0) {
    btnPlay.disabled = true;
  } else {
    // A shared link (#<episode-id>) opens that release; otherwise the latest.
    const wanted = episodes.find((e) => e.id === location.hash.slice(1));
    loadEpisode(wanted || episodes[0], false);
  }

  renderFeed();
  setupEventListeners();
  setupSpectrumVisualizer();
}

function switchCamera(cam) {
  activeCam = cam;
  const camSelect = $("cam-select");
  if (camSelect && camSelect.value !== cam) camSelect.value = cam;
  $$(".cam-btn").forEach(btn => {
    btn.classList.toggle("active", btn.getAttribute("data-cam") === cam);
  });

  // Reset layers
  hostLayer.classList.add("hidden");
  bunkerLayer.classList.add("hidden");
  stageOverlay.classList.add("hidden");

  // The cover video only decodes while it is the visible camera.
  if (heroVideo) {
    if (cam === "loop") heroVideo.play().catch(() => {});
    else heroVideo.pause();
  }

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
  currentStarts = cueStarts(ep);
  currentPara = -1;
  const badge = $("broadcast-badge");
  if (badge) badge.textContent = `${ep === episodes[0] ? "LATEST RELEASE" : "ARCHIVE"} · ${ep.hour || "HOURLY"} UTC`;
  if (location.hash.slice(1) !== ep.id) history.replaceState(null, "", `#${ep.id}`);

  // Update spotlight UI
  $("ep-title").textContent = ep.title;
  $("ep-subject").textContent = ep.subject;
  renderSources(ep);
  $("ep-category").textContent = categoryOf(ep.category).label.toUpperCase();
  $("ep-duration").textContent = `⏱ ${formatTime(ep.seconds)} MIN`;
  $("ep-time").textContent = `${ep.date} · ${ep.hour || "HOURLY"} UTC`;

  // Update media
  if (heroVideo) {
    heroVideo.poster = ep.thumb;
    if (ep.cover_video) {
      heroVideo.src = ep.cover_video;
      heroVideo.load();
      if (activeCam === "loop") heroVideo.play().catch(() => {});
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

  updateMediaSession(ep);

  if (autoPlay) {
    playAudio();
  } else {
    pauseAudio();
  }
}

function updateMediaSession(ep) {
  if (!("mediaSession" in navigator)) return;
  try {
    navigator.mediaSession.metadata = new MediaMetadata({
      title: ep.title,
      artist: "Rex Vance // ZeroFilter",
      album: "ZeroFilter Intelligence Stream",
      artwork: [
        { src: ep.thumb, sizes: "1280x720", type: "image/webp" }
      ]
    });
    navigator.mediaSession.setActionHandler("play", () => playAudio());
    navigator.mediaSession.setActionHandler("pause", () => pauseAudio());
    navigator.mediaSession.setActionHandler("seekbackward", () => {
      audio.currentTime = Math.max(0, audio.currentTime - 10);
    });
    navigator.mediaSession.setActionHandler("seekforward", () => {
      audio.currentTime = Math.min(audio.duration || 180, audio.currentTime + 10);
    });
    navigator.mediaSession.setActionHandler("previoustrack", () => playPreviousEpisode());
    navigator.mediaSession.setActionHandler("nexttrack", () => playNextEpisode());
  } catch (err) {
    console.debug("MediaSession error:", err);
  }
}

function playNextEpisode() {
  if (!currentEpisode || episodes.length <= 1) return;
  const idx = episodes.findIndex(e => e.id === currentEpisode.id);
  if (idx >= 0 && idx + 1 < episodes.length) {
    loadEpisode(episodes[idx + 1], true);
  }
}

function playPreviousEpisode() {
  if (!currentEpisode || episodes.length <= 1) return;
  const idx = episodes.findIndex(e => e.id === currentEpisode.id);
  if (idx > 0) {
    loadEpisode(episodes[idx - 1], true);
  }
}

// Every published episode carries its sources (engine/editorial.mjs).
function renderSources(ep) {
  const box = $("ep-sources-box");
  const list = $("ep-sources");
  if (!box || !list) return;
  list.textContent = "";
  const sources = (Array.isArray(ep.sources) ? ep.sources : []).filter((s) => /^https:\/\//.test(s?.url || ""));
  for (const s of sources) {
    const li = document.createElement("li");
    const a = document.createElement("a");
    a.href = s.url;
    a.target = "_blank";
    a.rel = "noopener noreferrer";
    a.textContent = s.title || s.url;
    li.append(a, ` · ${s.published || ""}${s.speaker ? ` · ${s.speaker}` : ""}`);
    list.append(li);
  }
  box.hidden = sources.length === 0;
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

  // Subtitle cue sync: real cues from voice.py, else word-weighted estimate
  // Captions show the sentence being spoken: the paragraph's time span
  // (exact cues from voice.py) shared out by word count across its sentences.
  const paraIdx = paragraphAt(currentStarts, t);
  const para = currentEpisode.paragraphs[paraIdx];
  if (para) {
    const sentences = para.match(/[^.!?]+[.!?]+["”’)]*\s*|[^.!?]+$/g) || [para];
    const start = currentStarts[paraIdx];
    const end = currentStarts[paraIdx + 1] ?? (audio.duration || currentEpisode.seconds);
    const words = sentences.map((x) => x.split(/\s+/).filter(Boolean).length);
    const total = words.reduce((x, y) => x + y, 0) || 1;
    let acc = 0, idx = 0;
    for (let k = 0; k < sentences.length; k++) {
      if (t >= start + (acc / total) * (end - start)) idx = k;
      acc += words[k];
    }
    const key = paraIdx * 1000 + idx;
    if (key !== currentPara) {
      currentPara = key;
      cueText.textContent = sentences[idx].trim();
    }
  }

  // Synchronized Stage Overlay
  const frames = currentEpisode.art?.frames || [];
  if (frames.length > 0) {
    let activeFrame = null;
    for (const f of frames) {
      if (t >= f.t) activeFrame = f;
    }

    if (activeFrame && activeFrame.src) {
      if (stageImg.getAttribute("src") !== activeFrame.src) {
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
  // Draw at device pixels so the bars stay sharp on phones (DPR 2-3).
  const dpr = Math.min(window.devicePixelRatio || 1, 3);
  // The spectrum is the control bar's background: fill the bar.
  const cssW = canvas.parentElement.clientWidth || 500;
  const cssH = canvas.parentElement.clientHeight || 36;
  canvas.style.width = cssW + "px";
  canvas.style.height = cssH + "px";
  canvas.width = Math.round(cssW * dpr);
  canvas.height = Math.round(cssH * dpr);
  barGradients = null;
  if (audio.paused) drawDefaultSpectrum();
}

function gradients() {
  if (barGradients) return barGradients;
  // Canvas-wide vertical gradients: a bar of any height shows the right slice.
  const normal = canvasCtx.createLinearGradient(0, 0, 0, canvas.height);
  normal.addColorStop(0, "#00e5ff");
  normal.addColorStop(1, "rgba(0, 229, 255, 0.3)");
  const peak = canvasCtx.createLinearGradient(0, 0, 0, canvas.height);
  peak.addColorStop(0, "#ffb300");
  peak.addColorStop(0.35, "#00e5ff");
  peak.addColorStop(1, "rgba(0, 229, 255, 0.3)");
  return (barGradients = [normal, peak]);
}

// Speech energy sits below ~5 kHz. Map 32 bars logarithmically over
// 80 Hz-8 kHz instead of linearly over 0-24 kHz, where most bars stayed flat.
let barBins = null;
function binsForBars(binCount, sampleRate) {
  const hzPerBin = sampleRate / 2 / binCount;
  const lo = 80, hi = Math.min(8000, sampleRate / 2);
  const edges = [];
  for (let i = 0; i <= BARS; i++) edges.push(Math.round(lo * Math.pow(hi / lo, i / BARS) / hzPerBin));
  return edges.map((e, i) => i < BARS ? [Math.min(e, binCount - 1), Math.max(e + 1, Math.min(edges[i + 1], binCount))] : null).slice(0, BARS);
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
    analyser.fftSize = 1024;
    analyser.smoothingTimeConstant = 0.8;
    source = audioCtx.createMediaElementSource(audio);
    source.connect(analyser);
    analyser.connect(audioCtx.destination);
    barBins = binsForBars(analyser.frequencyBinCount, audioCtx.sampleRate);
    // iOS Safari suspends/"interrupts" the context on calls, lock and tab
    // switches; resume when the page comes back and audio should be playing.
    document.addEventListener("visibilitychange", () => {
      if (!document.hidden && !audio.paused && audioCtx.state !== "running") audioCtx.resume();
    });
  } catch (err) {
    console.warn("AudioContext init error:", err);
  }
}

function drawDefaultSpectrum() {
  if (!canvasCtx || !canvas) return;
  canvasCtx.clearRect(0, 0, canvas.width, canvas.height);
  const gap = canvas.width / BARS > 6 ? 2 : 1;
  const barWidth = canvas.width / BARS - gap;
  const h = Math.max(2, Math.round(canvas.height / 12));
  for (let i = 0; i < BARS; i++) {
    const x = i * (barWidth + gap);
    canvasCtx.fillStyle = "rgba(0, 229, 255, 0.2)";
    canvasCtx.fillRect(x, canvas.height - h, barWidth, h);
  }
}

function startSpectrumLoop() {
  if (animFrameId) cancelAnimationFrame(animFrameId);

  const bufferLength = analyser ? analyser.frequencyBinCount : BARS;
  const dataArray = new Uint8Array(bufferLength);
  const levels = new Float32Array(BARS);

  function renderFrame() {
    animFrameId = requestAnimationFrame(renderFrame);

    if (audio.paused) {
      drawDefaultSpectrum();
      cancelAnimationFrame(animFrameId);
      return;
    }

    if (analyser && barBins) {
      analyser.getByteFrequencyData(dataArray);
      for (let i = 0; i < BARS; i++) {
        const [a, b] = barBins[i];
        let max = 0;
        for (let k = a; k < b; k++) if (dataArray[k] > max) max = dataArray[k];
        levels[i] = max / 255;
      }
    } else {
      // Simulated responsive pulse if Web Audio is restricted
      const now = performance.now();
      for (let i = 0; i < BARS; i++) levels[i] = (Math.sin(now / 150 + i * 0.4) * 80 + 120) / 255;
    }

    canvasCtx.clearRect(0, 0, canvas.width, canvas.height);
    const gap = canvas.width / BARS > 6 ? 2 : 1;
    const barWidth = (canvas.width / BARS) - gap;
    const minH = Math.max(2, Math.round(canvas.height / 12));
    const [normal, peak] = gradients();

    for (let i = 0; i < BARS; i++) {
      const percent = levels[i];
      const h = Math.max(minH, percent * (canvas.height - 4));
      canvasCtx.fillStyle = percent > 0.75 ? peak : normal;
      canvasCtx.fillRect(i * (barWidth + gap), canvas.height - h, barWidth, h);
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
  if (filtered.length === 0) {
    const empty = document.createElement("p");
    empty.className = "feed-empty";
    empty.textContent = episodes.length === 0
      ? "No briefings published yet. Each one goes up only once every claim in it links to a real, dated source."
      : "No briefings in this category yet.";
    episodesGrid.appendChild(empty);
    return;
  }

  filtered.forEach(ep => {
    const card = document.createElement("article");
    card.className = "episode-card";
    card.setAttribute("data-id", ep.id);

    card.innerHTML = `
      <div class="card-media">
        <video class="card-video" loop muted playsinline preload="none" poster="${escapeHtml(ep.thumb)}">
          <source src="${escapeHtml(ep.cover_video || '')}" type="video/mp4">
        </video>
        <span class="card-time-badge">${escapeHtml(ep.hour || '00:00')} UTC</span>
      </div>
      <div class="card-body">
        <div class="card-tags">
          <span class="badge category-badge">${escapeHtml(categoryOf(ep.category).label)}</span>
        </div>
        <h3 class="card-title">${escapeHtml(ep.title)}</h3>
        <p class="card-desc">${escapeHtml(ep.subject)}</p>
        <div class="card-footer">
          <span class="card-duration">⏱ ${formatTime(ep.seconds)}</span>
          <button type="button" class="btn-card-play">LISTEN NOW ▶</button>
        </div>
      </div>
    `;

    // Looping preview on card hover. The URL sits on a <source> child, so
    // video.src is always "" — checking it meant previews never played.
    const video = card.querySelector("video");
    card.addEventListener("mouseenter", () => {
      if (video && ep.cover_video) video.play().catch(() => {});
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
  // Lock-screen controls, headsets and other tabs can pause/play the element
  // without going through our button; mirror its real state.
  audio.addEventListener("play", () => {
    btnPlay.classList.add("playing");
    playIcon.textContent = "❚❚";
    startSpectrumLoop();
  });
  audio.addEventListener("pause", () => {
    btnPlay.classList.remove("playing");
    playIcon.textContent = "▶";
  });
  // The file, not the manifest, decides how long the seek bar is.
  audio.addEventListener("loadedmetadata", () => {
    if (Number.isFinite(audio.duration) && audio.duration > 0) {
      seekBar.max = audio.duration;
      totalTimeEl.textContent = formatTime(audio.duration);
    }
  });
  audio.addEventListener("ended", () => {
    stageOverlay.classList.add("hidden");
    if (episodes.length > 1) {
      playNextEpisode();
    } else {
      pauseAudio();
      audio.currentTime = 0;
    }
  });

  seekBar.addEventListener("input", () => {
    audio.currentTime = Number(seekBar.value);
    syncPlayback();
  });

  // Camera angle switcher
  // Picture and speed live in the control bar as two small selects.
  $("cam-select")?.addEventListener("change", (e) => switchCamera(e.target.value));
  $("speed-select")?.addEventListener("change", (e) => {
    audio.playbackRate = Number(e.target.value);
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
    if (!currentEpisode) return;
    const url = `${location.origin}${location.pathname}#${currentEpisode.id}`;
    if (navigator.share) {
      navigator.share({ title: currentEpisode.title, url }).catch(() => {});
    } else if (navigator.clipboard) {
      navigator.clipboard.writeText(url).then(() => {
        $("btn-share").title = "Link copied";
      }).catch(() => {});
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
    } else if (e.key === "c" || e.key === "C") {
      const cams = ["loop", "host", "bunker", "story"];
      const nextCam = cams[(cams.indexOf(activeCam) + 1) % cams.length];
      switchCamera(nextCam);
    } else if (e.key === "m" || e.key === "M") {
      audio.muted = !audio.muted;
    }
  });
}

init();
