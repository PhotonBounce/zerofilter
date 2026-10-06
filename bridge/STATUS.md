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
- **Framework:** Universal Autonomous DevOps & 24/7 Keep-Awake Engine active (`schedule(CronExpression="*/5 * * * *", IsDaemon=true)`).
- **Unit Tests:** `node engine/unit.mjs` — **144 passed, 0 failed clean**.
- **State On Disk:**
  - `status/pipeline_state.json`: Episode 17 completed, 17 total releases published.
  - `data/queue.json`: Head item is Episode 18 (`2026-10-06-18`).
  - `data/registry.json`: 17 active releases logged.
- **Published Releases (`web/data/episodes.json`):**
  - `2026-10-06-01` (168s) — Quantum Delayed Choice, Pentagon Backdoors & Ukraine Drone Swarms
  - `2026-10-06-02` (152s) — PEAR Lab Anomalies, MAGA Christofascists & DNC PAC Grift
  - `2026-10-06-03` (165s) — Thomas Campbell's Virtual Reality, AI Frontier Scaling & Taiwan Defense
  - `2026-10-06-04` (184s) — Black Sea Drone Strikes, Yuri Shvets PAC Disclosures & Entanglement Swapping
  - `2026-10-06-05` (177s) — Macroscopic Superposition, Tech Smuggling Receipts & Optomechanical Resonators
  - `2026-10-06-06` (186s) — Robert Monroe Gateway Archives, Yuri Shvets on KGB Psychotronics & SRI Telemetry
  - `2026-10-06-07` (181s) — Defense Revolving Doors, Dark Money PAC Laundering & Counter-Intel Leaks
  - `2026-10-06-08` (181s) — Black Sea Naval Drone Perimeters, Oil Refinery Flaring & Reflexive Control Bluffs
  - `2026-10-06-09` (184s) — Delayed-Choice Quantum Eraser, Wheeler's Smoky Dragon & SIGINT Interceptions
  - `2026-10-06-10` (183s) — Donald Hoffman's Perception Interface, KGB Deception Architecture & Neuro-Quantum Resonance
  - `2026-10-06-11` (173s) — Silicon Valley Defense Cartels, FISA 702 Receipts & Homomorphic Encryption
  - `2026-10-06-12` (171s) — Taiwan Strait Hellscape Doctrine, Beijing-Moscow Axis & EUV Chokepoints
  - `2026-10-06-13` (178s) — Quantum Vacuum Fluctuations, Casimir Micro-Thrusters & Orbital Surveillance
  - `2026-10-06-14` (180s) — Roger Penrose Orch-OR Quantum Biology, Non-Computable Algorithms & KGB Bio-Telemetry
  - `2026-10-06-15` (174s) — Baltic Sea GPS Jamming Corridors, Kremlin Shadow Tankers & Electronic Warfare Countermeasures
  - `2026-10-06-16` (189s) — Quantum Key Distribution Downlinks, Atmospheric Decoherence & China's Micius Network
  - `2026-10-06-17` (185s) — Pentagon Cost-Plus Contracting Cartels, Hypersonic Failure Audits & Revolving-Door Grift
- **Audio Files:** Synthesized in `web/audio/` using `edge-tts` (`en-US-ChristopherNeural` @ +10% rate, -2Hz pitch).
- **Video Covers:** 10s looping MP4s in `web/thumbs/` (`.mp4` and `.webp`).
- **Story Art Frames:** 102 synchronized frames in `web/art/`.
- **Zero-Branch Production Deployment:** Live at `https://photon-bounce.com/zerofilter/` without touching root.

---

## 3. Active Bridge Channels
- To assign a task or QA check to Claude: write to `bridge/INBOX_FOR_CLAUDE.md`.
- To reply back or give instructions to Antigravity: write to `bridge/INBOX_FOR_ANTIGRAVITY.md`.
