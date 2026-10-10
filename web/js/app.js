// app.js — Main frontend client application for ZeroFilter

import { parseEpisodes, formatTime, cueStarts, paragraphAt, escapeHtml } from "./episodes.js";
import { categoryOf } from "./categories.js";
import { initTelemetryBackground } from "./telemetry-canvas.js";
import { cyberAudio } from "./ambient.js";
import { checkAccess, canPlayTime, verifyAndApplyDevKey } from "./access.js";
import { VectorStage } from "./vector-stage.js";

const $ = (id) => document.getElementById(id);
const $$ = (sel) => document.querySelectorAll(sel);

function trackAnalytics(eventName, params = {}) {
  if (typeof window.gtag === "function") {
    try {
      window.gtag("event", eventName, params);
    } catch (e) {
      console.debug("Analytics event error:", e);
    }
  }
}

let episodes = [];
let currentEpisode = null;
let currentStarts = [];
let currentPara = -1;
let activeFilter = "all";
let activeCam = "story"; // "loop" | "host" | "bunker" | "story"

// Podcasting State
let playedEpisodes = new Set(JSON.parse(localStorage.getItem("zf_played_episodes") || "[]"));
let autoplayEnabled = localStorage.getItem("zf_autoplay") !== "false";
let activeQueue = [];
let sleepTimerTimeout = null;
let sleepTimerMode = "0";

const audio = $("main-audio");
const btnPlay = $("btn-play");
const btnPrev = $("btn-prev");
const btnNext = $("btn-next");
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
const vectorLayer = $("vector-layer");
const vectorCanvas = $("vector-stage-canvas");
let vectorStage = null;

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

// Access Control & Paywall State
let accessState = checkAccess();
const accessPill = $("access-pill");
const accessIcon = $("access-icon");
const accessLabel = $("access-label");
const paywallBackdrop = $("paywall-backdrop");
const btnClosePaywall = $("btn-close-paywall");
const cryptoToggle = $("crypto-toggle-header");
const cryptoContent = $("crypto-content");
const cryptoArrow = $("crypto-arrow");

function updateAccessUI() {
  if (!accessPill || !accessLabel) return;
  accessPill.classList.remove("is-dev", "is-trial", "is-preview");

  if (accessState.tier === "developer") {
    accessPill.classList.add("is-dev");
    if (accessIcon) accessIcon.textContent = "👑";
    accessLabel.textContent = "DEV UNLIMITED";
    accessPill.title = "Developer Mode: Permanent Unlocked Access Active";
  } else if (accessState.tier === "trial") {
    accessPill.classList.add("is-trial");
    if (accessIcon) accessIcon.textContent = "⏳";
    accessLabel.textContent = `TRIAL: ${accessState.trialDaysLeft}d`;
    accessPill.title = `7-Day Free Trial Active (${accessState.trialDaysLeft} days remaining). Full Access.`;
  } else {
    accessPill.classList.add("is-preview");
    if (accessIcon) accessIcon.textContent = "🔒";
    accessLabel.textContent = "PREVIEW (50%)";
    accessPill.title = "Free Preview Mode: 50% audio cutoff. Click to unlock full access.";
  }
}

function openPaywallModal() {
  if (paywallBackdrop) {
    paywallBackdrop.classList.remove("hidden");
    cyberAudio.playClick();
  }
}

function closePaywallModal() {
  if (paywallBackdrop) {
    paywallBackdrop.classList.add("hidden");
    cyberAudio.playClick();
  }
}

async function handleUrlDevKey() {
  try {
    const url = new URL(window.location.href);
    let devKey = url.searchParams.get("key") || url.searchParams.get("dev");
    if (!devKey && window.location.hash.startsWith("#key=")) {
      devKey = window.location.hash.slice(5);
    }
    if (!devKey && window.location.hash.startsWith("#dev=")) {
      devKey = window.location.hash.slice(5);
    }

    if (devKey) {
      const valid = await verifyAndApplyDevKey(devKey);
      if (valid) {
        accessState = checkAccess();
        // Clean URL parameter so the secret key is removed from address bar
        url.searchParams.delete("key");
        url.searchParams.delete("dev");
        const cleanPath = url.pathname + (url.search ? url.search : "");
        window.history.replaceState({}, document.title, cleanPath);
      }
    }
  } catch (err) {
    console.debug("Dev key parse:", err);
  }
  updateAccessUI();
}

function markAsPlayed(epId) {
  if (!epId) return;
  playedEpisodes.add(epId);
  localStorage.setItem("zf_played_episodes", JSON.stringify([...playedEpisodes]));
  updateToolbar();
  updateCardPlayedStates();
}

function togglePlayed(epId, e) {
  if (e) e.stopPropagation();
  cyberAudio.playClick();
  if (playedEpisodes.has(epId)) {
    playedEpisodes.delete(epId);
  } else {
    playedEpisodes.add(epId);
  }
  localStorage.setItem("zf_played_episodes", JSON.stringify([...playedEpisodes]));
  updateToolbar();
  updateCardPlayedStates();
}

function updateToolbar() {
  const countEl = $("unheard-count");
  if (countEl) {
    const unheard = episodes.filter(e => !playedEpisodes.has(e.id)).length;
    countEl.textContent = unheard;
  }
}

function updateCardPlayedStates() {
  $$(".card-played-badge").forEach(badge => {
    const id = badge.getAttribute("data-id");
    const isPlayed = playedEpisodes.has(id);
    badge.classList.toggle("is-played", isPlayed);
    badge.textContent = isPlayed ? "✓ PLAYED" : "○ UNPLAYED";
  });
}

function resetSleepTimer() {
  if (sleepTimerTimeout) {
    clearTimeout(sleepTimerTimeout);
    sleepTimerTimeout = null;
  }
  sleepTimerMode = "0";
  const sel = $("sleep-timer-select");
  if (sel) sel.value = "0";
}

function setSleepTimer(val) {
  resetSleepTimer();
  sleepTimerMode = val;
  if (val === "15" || val === "30") {
    const ms = Number(val) * 60 * 1000;
    sleepTimerTimeout = setTimeout(() => {
      pauseAudio();
      resetSleepTimer();
    }, ms);
  }
}

// Initialize application
async function init() {
  await handleUrlDevKey();
  // Start interactive background telemetry & radar animation
  initTelemetryBackground("bg-telemetry-canvas");

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
  updateToolbar();
  setupEventListeners();
  setupSpectrumVisualizer();
  if (vectorCanvas) {
    vectorStage = new VectorStage(vectorCanvas);
  }
}

function switchCamera(cam) {
  activeCam = cam;
  trackAnalytics("camera_switch", {
    camera: cam,
    episode_id: currentEpisode ? currentEpisode.id : "none"
  });
  const camSelect = $("cam-select");
  if (camSelect && camSelect.value !== cam) camSelect.value = cam;
  $$(".cam-btn").forEach(btn => {
    btn.classList.toggle("active", btn.getAttribute("data-cam") === cam);
  });

  // Reset layers
  hostLayer.classList.add("hidden");
  bunkerLayer.classList.add("hidden");
  stageOverlay.classList.add("hidden");
  if (vectorLayer) vectorLayer.classList.add("hidden");

  // The cover video only decodes while it is the visible camera.
  if (heroVideo) {
    if (cam === "loop") heroVideo.play().catch(() => {});
    else heroVideo.pause();
  }

  if (cam === "loop") {
    // Let video display
  } else if (cam === "vector") {
    if (vectorLayer) vectorLayer.classList.remove("hidden");
    if (vectorStage && currentEpisode) vectorStage.setThemeByEpisode(currentEpisode);
  } else if (cam === "host") {
    hostLayer.classList.remove("hidden");
  } else if (cam === "bunker") {
    bunkerLayer.classList.remove("hidden");
  } else if (cam === "story") {
    // Show current synchronized story frame
    syncPlayback();
  }
}

function getCurrentPlaylist() {
  if (activeFilter && activeFilter !== "all") {
    const filtered = episodes.filter(e => e.category === activeFilter);
    if (filtered.length > 0) return filtered;
  }
  return episodes;
}

function loadEpisode(ep, autoPlay = true) {
  if (!ep) return;
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

  trackAnalytics("page_view", {
    page_title: `${ep.title} | ZeroFilter`,
    page_location: window.location.href,
    page_path: `${window.location.pathname}#${ep.id}`
  });
  trackAnalytics("episode_view", {
    episode_id: ep.id,
    episode_title: ep.title,
    category: ep.category,
    kind: ep.kind || "hourly"
  });

  if (vectorStage) {
    vectorStage.setThemeByEpisode(ep);
  }

  // Update media
  if (heroVideo) {
    heroVideo.poster = ep.thumb;
    if (ep.cover_video) {
      heroVideo.src = ep.cover_video;
      heroVideo.load();
      if (activeCam === "loop") heroVideo.play().catch(() => {});
    }
  }

  // Update audio cleanly
  const currentAudioSrc = audio.getAttribute("src") || "";
  if (currentAudioSrc !== ep.audio && !currentAudioSrc.endsWith(ep.audio)) {
    audio.pause();
    audio.src = ep.audio;
    audio.load();
  }
  audio.currentTime = 0;
  seekBar.max = ep.seconds || 180;
  seekBar.value = 0;
  totalTimeEl.textContent = formatTime(ep.seconds);
  currentTimeEl.textContent = "0:00";

  cueText.textContent = `"${ep.paragraphs[0] || 'Broadcasting now...'}"`;

  // Highlight active episode in grid
  $$(".episode-card").forEach(card => {
    card.classList.toggle("is-active", card.getAttribute("data-id") === ep.id);
  });

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
  const list = getCurrentPlaylist();
  if (!currentEpisode || list.length === 0) return;
  
  let idx = list.findIndex(e => e.id === currentEpisode.id);
  if (idx === -1) {
    idx = episodes.findIndex(e => e.id === currentEpisode.id);
    if (idx >= 0 && idx + 1 < episodes.length) {
      loadEpisode(episodes[idx + 1], true);
      return;
    }
  }
  
  const nextIdx = idx >= 0 ? (idx + 1) % list.length : 0;
  const nextEp = list[nextIdx];

  // Prevent loading the exact same episode when more than one exists
  if (nextEp.id === currentEpisode.id && list.length > 1) {
    const altIdx = (nextIdx + 1) % list.length;
    loadEpisode(list[altIdx], true);
    return;
  }

  // Synchronize activeQueue so it doesn't replay stale episodes
  if (activeQueue.length > 0) {
    const qIdx = activeQueue.findIndex(e => e.id === nextEp.id);
    if (qIdx >= 0) {
      activeQueue.splice(0, qIdx + 1);
    }
  }

  loadEpisode(nextEp, true);
}

function playPreviousEpisode() {
  const list = getCurrentPlaylist();
  if (!currentEpisode || list.length === 0) return;
  
  let idx = list.findIndex(e => e.id === currentEpisode.id);
  if (idx === -1) {
    idx = episodes.findIndex(e => e.id === currentEpisode.id);
    if (idx > 0) {
      loadEpisode(episodes[idx - 1], true);
      return;
    }
  }
  
  const prevIdx = idx > 0 ? idx - 1 : list.length - 1;
  const prevEp = list[prevIdx];

  if (prevEp.id === currentEpisode.id && list.length > 1) {
    const altIdx = (prevIdx - 1 + list.length) % list.length;
    loadEpisode(list[altIdx], true);
    return;
  }

  loadEpisode(prevEp, true);
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
    a.addEventListener("click", () => {
      trackAnalytics("citation_click", {
        episode_id: ep.id,
        citation_url: s.url,
        citation_title: s.title || s.url
      });
    });
    li.append(a, ` · ${s.published || ""}${s.speaker ? ` · ${s.speaker}` : ""}`);
    list.append(li);
  }
  box.hidden = sources.length === 0;
}

function playAudio() {
  initAudioContext();
  if (currentEpisode) {
    trackAnalytics("audio_play", {
      episode_id: currentEpisode.id,
      episode_title: currentEpisode.title,
      category: currentEpisode.category
    });
  }
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

  // Paywall guard: enforce 50% cutoff for non-unlocked visitors
  if (!accessState.isUnlocked && audio.duration > 0 && t >= audio.duration * 0.5) {
    audio.pause();
    audio.currentTime = audio.duration * 0.5;
    openPaywallModal();
    return;
  }

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
    const isCurrent = currentEpisode && currentEpisode.id === ep.id;
    card.className = `episode-card${isCurrent ? ' is-active' : ''}`;
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
          <button type="button" class="card-played-badge ${playedEpisodes.has(ep.id) ? 'is-played' : ''}" data-id="${escapeHtml(ep.id)}" title="Click to toggle played status">
            ${playedEpisodes.has(ep.id) ? '✓ PLAYED' : '○ UNPLAYED'}
          </button>
          <a href="${escapeHtml(ep.audio)}" download="${escapeHtml(ep.id)}.mp3" class="card-download-btn" title="Download Episode MP3" onclick="event.stopPropagation()">
            ⬇ MP3
          </a>
          <button type="button" class="btn-card-play">LISTEN NOW ▶</button>
        </div>
      </div>
    `;

    // Played state button handler
    card.querySelector(".card-played-badge")?.addEventListener("click", (e) => {
      togglePlayed(ep.id, e);
    });

    // Looping preview on card hover
    const video = card.querySelector("video");
    card.addEventListener("mouseenter", () => {
      if (video && ep.cover_video) video.play().catch(() => {});
    });
    card.addEventListener("mouseleave", () => {
      if (video) video.pause();
    });

    card.addEventListener("click", () => {
      cyberAudio.playClick();
      const list = getCurrentPlaylist();
      const clickedIdx = list.findIndex(e => e.id === ep.id);
      if (clickedIdx >= 0) {
        activeQueue = [...list.slice(clickedIdx + 1)];
      }
      loadEpisode(ep, true);
      window.scrollTo({ top: 0, behavior: "smooth" });
    });

    episodesGrid.appendChild(card);
  });
}

function setupEventListeners() {
  btnPlay.addEventListener("click", togglePlay);
  btnPrev?.addEventListener("click", () => {
    cyberAudio.playClick();
    playPreviousEpisode();
  });
  btnNext?.addEventListener("click", () => {
    cyberAudio.playClick();
    playNextEpisode();
  });

  audio.addEventListener("timeupdate", syncPlayback);
  // Lock-screen controls, headsets and other tabs can pause/play the element
  audio.addEventListener("play", () => {
    btnPlay.classList.add("playing");
    playIcon.textContent = "❚❚";
    cyberAudio.duck(true);
    startSpectrumLoop();
  });
  audio.addEventListener("pause", () => {
    btnPlay.classList.remove("playing");
    playIcon.textContent = "▶";
    cyberAudio.duck(false);
  });
  // The file, not the manifest, decides how long the seek bar is.
  audio.addEventListener("loadedmetadata", () => {
    if (Number.isFinite(audio.duration) && audio.duration > 0) {
      seekBar.max = audio.duration;
      totalTimeEl.textContent = formatTime(audio.duration);
    }
  });
  audio.addEventListener("ended", () => {
    if (currentEpisode) {
      markAsPlayed(currentEpisode.id);
      trackAnalytics("audio_complete", {
        episode_id: currentEpisode.id,
        episode_title: currentEpisode.title,
        duration: audio.duration
      });
    }
    stageOverlay.classList.add("hidden");
    
    // Sleep timer 'end of episode'
    if (sleepTimerMode === "end") {
      pauseAudio();
      resetSleepTimer();
      return;
    }

    if (activeQueue.length > 0) {
      let nextEp = activeQueue.shift();
      // Ensure we don't accidentally repeat the same episode
      while (nextEp && currentEpisode && nextEp.id === currentEpisode.id && activeQueue.length > 0) {
        nextEp = activeQueue.shift();
      }
      if (nextEp && (!currentEpisode || nextEp.id !== currentEpisode.id)) {
        loadEpisode(nextEp, true);
        return;
      }
    }
    
    if (autoplayEnabled && episodes.length > 1) {
      playNextEpisode();
    } else {
      pauseAudio();
      audio.currentTime = 0;
    }
  });

  seekBar.addEventListener("input", () => {
    let target = Number(seekBar.value);
    if (!accessState.isUnlocked && audio.duration > 0 && target >= audio.duration * 0.5) {
      target = audio.duration * 0.5;
      seekBar.value = target;
      openPaywallModal();
    }
    audio.currentTime = target;
    syncPlayback();
  });

  // Podcasting Toolbar Listeners
  $("btn-play-all")?.addEventListener("click", () => {
    cyberAudio.playClick();
    const list = getCurrentPlaylist();
    if (list.length === 0) return;
    let startIdx = 0;
    if (currentEpisode && currentEpisode.id === list[0].id && list.length > 1) {
      startIdx = 1;
    }
    activeQueue = [...list.slice(startIdx + 1)];
    loadEpisode(list[startIdx], true);
  });

  $("btn-play-unheard")?.addEventListener("click", () => {
    cyberAudio.playClick();
    const unheard = episodes.filter(e => !playedEpisodes.has(e.id));
    if (unheard.length === 0) {
      alert("All available briefings have been listened to!");
      return;
    }
    activeQueue = [...unheard.slice(1)];
    loadEpisode(unheard[0], true);
  });

  $("btn-toggle-autoplay")?.addEventListener("click", () => {
    cyberAudio.playClick();
    autoplayEnabled = !autoplayEnabled;
    localStorage.setItem("zf_autoplay", autoplayEnabled);
    const btn = $("btn-toggle-autoplay");
    if (btn) {
      btn.classList.toggle("active", autoplayEnabled);
      btn.innerHTML = `<span>↺</span> AUTOPLAY: ${autoplayEnabled ? 'ON' : 'OFF'}`;
    }
  });

  $("sleep-timer-select")?.addEventListener("change", (e) => {
    cyberAudio.playClick();
    setSleepTimer(e.target.value);
  });

  // Ambient Drone Bed Toggle
  $("btn-toggle-ambient")?.addEventListener("click", () => {
    const isNowOn = cyberAudio.toggleAmbient();
    const btn = $("btn-toggle-ambient");
    const txt = $("ambient-status-text");
    if (btn) btn.classList.toggle("active", isNowOn);
    if (txt) txt.textContent = isNowOn ? "AMBIENT: ON" : "AMBIENT: OFF";
    cyberAudio.playClick();
  });

  // Camera angle switcher
  $("cam-select")?.addEventListener("change", (e) => {
    cyberAudio.playClick();
    switchCamera(e.target.value);
  });
  $("speed-select")?.addEventListener("change", (e) => {
    audio.playbackRate = Number(e.target.value);
  });

  // Category filters
  $$(".nav-btn").forEach(btn => {
    btn.addEventListener("click", () => {
      $$(".nav-btn").forEach(b => b.classList.remove("active"));
      btn.classList.add("active");
      activeFilter = btn.getAttribute("data-filter");
      trackAnalytics("filter_category", { category: activeFilter });
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
      if (e.shiftKey || e.ctrlKey || e.altKey) {
        e.preventDefault();
        playNextEpisode();
      } else {
        const remaining = (audio.duration || 180) - audio.currentTime;
        if (remaining <= 5) {
          playNextEpisode();
        } else {
          audio.currentTime = Math.min(audio.duration || 180, audio.currentTime + 5);
        }
      }
    } else if (e.code === "ArrowLeft") {
      if (e.shiftKey || e.ctrlKey || e.altKey) {
        e.preventDefault();
        playPreviousEpisode();
      } else {
        if (audio.currentTime <= 3) {
          playPreviousEpisode();
        } else {
          audio.currentTime = Math.max(0, audio.currentTime - 5);
        }
      }
    } else if (e.key === "n" || e.key === "N" || e.code === "MediaTrackNext") {
      e.preventDefault();
      playNextEpisode();
    } else if (e.key === "p" || e.key === "P" || e.code === "MediaTrackPrevious") {
      e.preventDefault();
      playPreviousEpisode();
    } else if (e.key === "c" || e.key === "C") {
      const cams = ["vector", "story", "loop", "host", "bunker"];
      const nextCam = cams[(cams.indexOf(activeCam) + 1) % cams.length];
      switchCamera(nextCam);
    } else if (e.key === "m" || e.key === "M") {
      audio.muted = !audio.muted;
    }
  });

  // Access Pill & Paywall listeners
  accessPill?.addEventListener("click", () => {
    openPaywallModal();
  });
  btnClosePaywall?.addEventListener("click", closePaywallModal);
  paywallBackdrop?.addEventListener("click", (e) => {
    if (e.target === paywallBackdrop) closePaywallModal();
  });
  cryptoToggle?.addEventListener("click", () => {
    cryptoContent?.classList.toggle("hidden");
    if (cryptoArrow) {
      cryptoArrow.textContent = cryptoContent?.classList.contains("hidden") ? "▼" : "▲";
    }
  });
  $$(".btn-copy").forEach((btn) => {
    btn.addEventListener("click", () => {
      const targetId = btn.getAttribute("data-target");
      const codeEl = $(targetId);
      if (codeEl) {
        navigator.clipboard.writeText(codeEl.textContent.trim()).then(() => {
          const oldText = btn.textContent;
          btn.textContent = "COPIED!";
          setTimeout(() => { btn.textContent = oldText; }, 2000);
        }).catch(() => {});
      }
    });
  });

}

init();

