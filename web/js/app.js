// app.js — Main frontend client application for ZeroFilter

import { parseEpisodes, formatTime } from "./episodes.js";
import { categoryOf } from "./categories.js";

const $ = (id) => document.getElementById(id);
const $$ = (sel) => document.querySelectorAll(sel);

let episodes = [];
let currentEpisode = null;
let activeFilter = "all";

const audio = $("main-audio");
const btnPlay = $("btn-play");
const playIcon = $("play-icon");
const seekBar = $("seek-bar");
const seekProgress = $("seek-progress");
const currentTimeEl = $("current-time");
const totalTimeEl = $("total-time");
const heroVideo = $("hero-video");
const stageOverlay = $("stage-overlay");
const stageImg = $("stage-img");
const stageCaption = $("stage-caption");
const cueText = $("cue-text");
const episodesGrid = $("episodes-grid");

// Initialize application
async function init() {
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

  // Reset stage
  stageOverlay.classList.add("hidden");
  cueText.textContent = `"${ep.paragraphs[0] || 'Broadcasting now...'}"`;

  if (autoPlay) {
    playAudio();
  } else {
    pauseAudio();
  }
}

function playAudio() {
  audio.play().then(() => {
    btnPlay.classList.add("playing");
    playIcon.textContent = "❚❚";
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
    // Find highest frame whose timestamp t <= current audio t
    let activeFrame = null;
    for (const f of frames) {
      if (t >= f.t) activeFrame = f;
    }

    if (activeFrame && activeFrame.src) {
      if (stageImg.src !== activeFrame.src) {
        stageImg.src = activeFrame.src;
      }
      stageCaption.textContent = activeFrame.caption || "";
      stageOverlay.classList.remove("hidden");
    } else {
      stageOverlay.classList.add("hidden");
    }
  } else {
    stageOverlay.classList.add("hidden");
  }
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

  // Keyboard navigation
  window.addEventListener("keydown", (e) => {
    if (e.target.tagName === "INPUT" || e.target.tagName === "TEXTAREA") return;
    if (e.code === "Space") {
      e.preventDefault();
      togglePlay();
    } else if (e.code === "ArrowRight") {
      audio.currentTime = Math.min(audio.duration || 180, audio.currentTime + 5);
    } else if (e.code === "ArrowLeft") {
      audio.currentTime = Math.max(0, audio.currentTime - 5);
    }
  });
}

init();
