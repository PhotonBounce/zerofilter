# ZeroFilter System Blueprint & Cold-Start Bootup Guide

This document is the definitive technical blueprint of the **ZeroFilter Autonomous Broadcast Engine**. It explains the full architecture, how every pipeline component operates, how to clone and replicate it for a new project, and how an agent or developer should handle a system reboot or downtime when catching up on episodes.

---

## Part 1: Cold-Start Bootup & Downtime Recovery Guide

When the machine restarts, boots up, or resumes after hours/days of downtime, follow this exact protocol to determine system state and catch up safely.

### 1.1 First Step: Diagnostic State Check
Run the following commands in the project root:

```bash
# 1. Check local git branch and status
git status

# 2. Fetch latest changes from remote
git fetch origin

# 3. Check current test suite health
node engine/unit.mjs
```

### 1.2 How to Detect if You Are "Behind" on Episodes
Check the timestamps in `web/data/episodes.json` and compare them with the current UTC time:

```bash
# Print latest episode in manifest vs current UTC time
node -e "const eps = JSON.parse(require('fs').readFileSync('web/data/episodes.json')).episodes; console.log('Latest Local Ep:', eps[0].id, eps[0].date, eps[0].hour); console.log('Current UTC:', new Date().toISOString());"
```

Also check `origin/main` to see what automated hourly releases were merged by GitHub Actions during downtime:
```bash
git log origin/main -n 5 --oneline
```

### 1.3 The Golden Rule of Catching Up: NO HOURLY BACKFILL
> [!IMPORTANT]
> **Strict Anti-Backfill Rule (`engine/editorial.mjs` & `AGENTS.md` Rule 2)**:
> - **Never backdate an hourly episode.** Hourly episodes (`kind: "hourly"`) require real-time snapshots with `MAX_CAPTURE_LAG_MS <= 3h`.
> - If the machine was offline for 8 hours, **DO NOT fabricate or hand-write old hourly ingest files** (`data/ingest/*.json`). Faking past snapshots will fail CI and violate the anti-hallucination gate.
> - **What to do instead for the live feed**: Simply run `node engine/ingest.mjs` to capture the **current real-time UTC hour**, and publish the episode for the *current hour*.
> - **What to do if you need to fill historical backlog volume**: Produce **Daily Retrospective Dossiers** (`kind: "daily"`). Daily episodes do not require hourly snapshots; they cite permanent peer-reviewed papers, congressional reports, court records, or declassified archives marked `kind: "reference"` with `published <= ep.date`.

### 1.4 Resuming Workflow Upon Boot

```
                                  [SYSTEM BOOT]
                                        |
                            +-----------+-----------+
                            |                       |
                     [HOURLY PIPELINE]       [RETROSPECTIVE BACKLOG]
                            |                       |
                 Run live ingest:                Produce daily dossiers
                 node engine/ingest.mjs          tools/produce_daily_trump_series*.py
                            |                       |
                 Write current ep from           Ava Vance neural TTS +
                 data/ingest/<now>.json          HUD WebP story art
                            |                       |
                            +-----------+-----------+
                                        |
                            Run: node engine/unit.mjs
                                        |
                            Run: node engine/build_site.mjs
                                        |
                            Commit & Push to branch (PR to main)
```

---

## Part 2: Architecture & Component Blueprint

ZeroFilter is an autonomous, high-frequency multimedia broadcast station that ingests raw intelligence, validates source veracity, synthesizes neural voice narration, renders visual cyber-forensic HUD story art, and serves an ultra-fast, zero-dependency frontend.

```
+-----------------------------------------------------------------------------------+
|                              ZEROFILTER ARCHITECTURE                              |
+-----------------------------------------------------------------------------------+

 1. INTELLIGENCE INGEST          2. EDITORIAL GATE             3. MULTIMEDIA ENGINE
 +--------------------+         +--------------------+         +--------------------+
 | data/feeds.json    | ------> | engine/            | ------> | engine/voice.py    |
 | - RSS / Atom       |         |   editorial.mjs    |         | - Edge-TTS Neural  |
 | - YouTube Feeds    |         | Anti-Hallucination |         | - Byte Cues Offset |
 | - arXiv & bioRxiv  |         | Source Veracity    |         +--------------------+
 +--------------------+         +--------------------+                   |
           |                              |                              v
           v                              v                    +--------------------+
 +--------------------+         +--------------------+         | PIL HUD Art Engine |
 | data/ingest/       |         | Verified Claims:   |         | - 1376x768 WebP    |
 | <YYYY-MM-DD-HH>.json|         | P0 - P4 Sources    |         | - Looping MP4s     |
 +--------------------+         +--------------------+         +--------------------+
                                                                         |
                                                                         v
 4. DISTRIBUTION & PLAYER       <----------------------------------------+
 +----------------------------------------------------------------------------------+
 | web/ (Vanilla HTML5 / Modern CSS / ES6 Modules)                                   |
 | - web/data/episodes.json (Master Manifest)                                       |
 | - web/audio/<id>.mp3 (Broadcast Audio)                                           |
 | - web/art/<id>/f01..f06.webp (Synchronized Story Frames)                         |
 | - web/thumbs/<id>.webp & <id>.mp4 (Cover Media)                                  |
 | - web/js/app.js & web/js/access.js (Timeline Player & Monetization)              |
 +----------------------------------------------------------------------------------+
```

---

## Part 3: Deep Component Breakdown

### 3.1 The Ingest Engine (`engine/ingest.mjs`)
- **Feed Configuration**: Defined in [`data/feeds.json`](file:///d:/zerofilter/data/feeds.json). Supports RSS 2.0, RSS 1.0 (RDF), Atom, and YouTube channel upload feeds (`https://www.youtube.com/feeds/videos.xml?channel_id=...`).
- **Sanitization**: Strips HTML entities, CDATA wrappers, tracking query parameters, and enforces `https://`.
- **Clock Synchronization**: Queries global NTP/HTTP headers to guarantee the local machine clock isn't drifting.
- **Snapshot Generation**: At each UTC hour, writes `data/ingest/YYYY-MM-DD-HH.json` containing all articles/videos collected in that window, with item counts matching reported feed totals.

### 3.2 The Editorial Integrity Gate (`engine/editorial.mjs`)
The core anti-hallucination sentinel. An episode **cannot** be published or pass `engine/unit.mjs` unless it satisfies:
1. **No Future Dating**: `episodeTime(ep) <= Date.now()`.
2. **Strict Claim Verification**: Every claim paragraph (P0, P1, P2, P3, P4) must cite at least one verified source with `https://` URL, a valid `published` date (YYYY-MM-DD), and `published <= ep.date`. P5 is sign-off/synthesis and requires no source.
3. **No Fake Quotes**: Any paragraph mentioning a real tracked speaker (e.g. `QUOTED_PEOPLE` like Yuri Shvets) must cite a link where that person directly spoke from their own feed.
4. **Proven Snapshot Matching**:
   - For `hourly`: Sourced URLs must exist inside `data/ingest/<ep.ingest>.json`.
   - For `daily`: Permitted to cite permanent peer-reviewed or judicial records marked `kind: "reference"` with `published <= ep.date`.

### 3.3 The Neural Voice Engine (`engine/voice.py`)
- **Model**: Microsoft Neural Speech (`en-US-AvaMultilingualNeural` or `en-US-AvaNeural`) via `edge-tts`.
- **Rate & Pitch Tuning**: Configured to `+14%` rate and `-1Hz` pitch for authoritative broadcast cadence (~150 words per minute).
- **Exact Cue Tracking**: Each paragraph is synthesized individually and merged. The byte length is measured (`MP3_BYTES_PER_SECOND = 48000 / 8 = 6000 bytes/sec`), recording the exact starting timestamp of every paragraph:
  ```json
  "cues": [0.0, 31.49, 63.96, 91.78, 121.66, 147.14]
  ```
  The web player uses these explicit cues to change subtitles and story art frames without estimation or drift.

### 3.4 Visual Production Engine (`tools/produce_*.py`)
- **Dimensions**: 1376x768 WebP (16:9 ratio, >1280px minimum width).
- **HUD Telemetry Aesthetic**: Built with Python `PIL` (`Pillow`). Generates cyber-forensic HUD boxes, telemetry frequency bars, source exhibit boxes, classification banners, and subtle RGB noise grain.
- **Frame Sync**: Monotonically increasing timestamps linked 1-to-1 with paragraph cues.
- **Looping Video Covers**: 10-second looping MP4s stored in `web/thumbs/<id>.mp4`.

### 3.5 The Web Player & Access System (`web/`)
- **Zero Frameworks**: 100% Vanilla HTML5, modern CSS with HSL design tokens, and modular ES6 JavaScript.
- **Playback Controls**:
  - `playNextEpisode()` / `playPreviousEpisode()` with de-duplicated queues and loop-around.
  - Keyboard shortcuts (`Shift+ArrowRight`, `N`, `P`, Space, Arrow keys).
  - Media Session API support for hardware lockscreen/keyboard keys.
- **Monetization & Access Control (`web/js/access.js`)**:
  - 7-day automatic free trial initialized in `localStorage`.
  - 50% audio cutoff and seek-blocking for expired/free tier users.
  - Developer unlock tier verified via client-side SHA-256 hash comparison without storing plaintext secrets.

---

## Part 4: How to Clone This for a Similar Project

To duplicate this system for a different domain (e.g. Finance, Biotech, Tech News, Gaming):

### Step 1: Clone and Clean Repository
```bash
git clone https://github.com/PhotonBounce/zerofilter.git my-podcast-station
cd my-podcast-station
```

### Step 2: Configure Your Domain Feeds
Edit `data/feeds.json` with RSS/Atom/YouTube channels relevant to your topic:
```json
[
  {
    "id": "reuters-business",
    "name": "Reuters Business",
    "url": "https://www.reutersagency.com/feed/?taxonomy=best-sectors&post_type=best",
    "kind": "news"
  },
  {
    "id": "custom-youtube-channel",
    "name": "Analyst Channel",
    "url": "https://www.youtube.com/feeds/videos.xml?channel_id=YOUR_CHANNEL_ID",
    "kind": "speaker",
    "speaker": "Speaker Name"
  }
]
```

### Step 3: Define Your Taxonomy
Edit `web/js/categories.js` and `data/categories.json` to define your topic categories, badges, and filters.

### Step 4: Configure Persona and Voice
Edit `engine/voice.py` to pick your preferred voice (e.g. `en-US-GuyNeural`, `en-GB-SoniaNeural`, `en-US-AvaMultilingualNeural`).

### Step 5: Test Full Pipeline Locally
```bash
# 1. Install dependencies
pip install edge-tts pillow

# 2. Test live feed ingest
node engine/ingest.mjs

# 3. Test unit test suite
node engine/unit.mjs

# 4. Build static distribution bundle
node engine/build_site.mjs
```

### Step 6: GitHub Actions Secrets for Deployment
Configure repository secrets in GitHub:
- `FTP_HOST`, `FTP_USER`, `FTP_PASS` (if using FTP deployment via `deploy-ftp.yml`), or enable GitHub Pages in settings targeting `dist/` or `gh-pages` branch.

---

## Part 5: Summary Checklist for Cold Boot

| Check | Action | Pass Condition |
| :--- | :--- | :--- |
| **1. Branch** | `git status` | Clean working tree on target branch |
| **2. Sync** | `git fetch origin` | Know latest remote commits on `main` |
| **3. Tests** | `node engine/unit.mjs` | All checks pass (0 errors) |
| **4. Time Check** | Compare last ep date vs current UTC | If missed hours, do **NOT** backfill; capture current hour |
| **5. Live Release** | `node engine/ingest.mjs` | Fresh snapshot in `data/ingest/` |
| **6. Site Compile**| `node engine/build_site.mjs` | `dist/` updated with all manifest episodes |
