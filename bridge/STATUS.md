# ZeroFilter — Project State & Bridge Status

**Updated:** 2026-10-05 22:55 UTC  
**Primary Developers:** Antigravity (Frontend, Automation Engine & Media Synthesis) + Claude (QA, Architecture, Code Mode)  
**Root Path:** `D:\zerofilter`  
**Live GitHub Pages Deployment:** `https://photon-bounce.com/zerofilter/` (folder `zerofilter/` on branch `gh-pages` of `photonbounce`)  
**Local Dev Server:** `http://localhost:4200/index.html` (python http.server on port 4200)

---

## 1. Project Overview & Rules
- **Formula:** 3-minute hourly intelligence broadcast (180s, exactly 6 structured paragraphs, ~400–500 words).
- **Host:** Rex Vance (ex-DARPA/intel analyst, cynical, mathematically literate, neural baritone voice).
- **Primary US Intel Wire:** **Yuri Shvets (Юрий Швец)**, ex-KGB major / Washington intelligence dissident.
- **Key Docs:**
  - `docs/EPISODE_FORMULA.md` (Minute-by-minute rules)
  - `docs/HOST_PERSONA.md` (Rex Vance voice & style)
  - `docs/ARCHITECTURE.md` (Zero-dependency vanilla stack)

---

## 2. Current Working State
- **Unit Tests:** `node engine/unit.mjs` — **32 passed, 0 failed clean**.
- **Seeded Pilot Releases (`web/data/episodes.json`):**
  - `2026-10-06-01` (168s) — Quantum Delayed Choice, Pentagon Backdoors & Ukraine Drone Swarms
  - `2026-10-06-02` (152s) — PEAR Lab Anomalies, MAGA Christofascists & DNC PAC Grift
  - `2026-10-06-03` (165s) — Thomas Campbell's Virtual Reality, AI Frontier Scaling & Taiwan Defense
- **Audio Files:** Synthesized in `web/audio/` using `edge-tts` (`en-US-ChristopherNeural` @ +10% rate, -2Hz pitch).
- **Video Covers:** 10s looping MP4s in `web/thumbs/` (`.mp4` and `.webp`).
- **Story Art Frames:** 18 frames in `web/art/` synchronized to paragraph timestamps.
- **Frontend UI (`web/index.html`):**
  - Real-time Canvas Audio Spectrum Visualizer
  - Multi-Angle Studio Switcher (Cover Video, Host Cam, Bunker Cam, Story Art)
  - Rex Vance & Yuri Shvets Intelligence Dossier drawer

---

## 3. Active Bridge Channels
- To assign a task or QA check to Claude: write to `bridge/INBOX_FOR_CLAUDE.md`.
- To reply back or give instructions to Antigravity: write to `bridge/INBOX_FOR_ANTIGRAVITY.md`.
