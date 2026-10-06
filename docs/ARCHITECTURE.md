# ZeroFilter System Architecture

## 1. High-Level Overview
ZeroFilter is an English-language portal designed for high-frequency, hourly audio-visual news broadcasts. It runs on a lean, zero-dependency stack with millisecond-fast load times, synchronized visual art overlays, and looping video covers.

```
                  +----------------------------------------------+
                  |         ZeroFilter Portal (Frontend)         |
                  |  Vanilla HTML5 + Vanilla CSS + ES6 Modules  |
                  +----------------------------------------------+
                                         |
               +-------------------------+-------------------------+
               |                         |                         |
        [data/episodes.json]       [thumbs/<id>.mp4]       [art/<id>/f<nn>.webp]
        Hourly Episode Manifest    10s Looping Covers      Synchronized Art
               |                         |                         |
               +-------------------------+-------------------------+
                                         |
                  +----------------------------------------------+
                  |         ZeroFilter Engine (Automation)       |
                  |  Node.js ES Modules + Gemini & Veo API      |
                  +----------------------------------------------+
```

---

## 2. Directory Structure

```
D:\zerofilter\
├── web/                           # Standalone Frontend Application
│   ├── index.html                 # Main landing page & audio/video player
│   ├── style.css                  # Dark mode, responsive design system
│   ├── css/
│   │   └── studio.css             # Studio & dynamic overlay styles
│   ├── js/
│   │   ├── app.js                 # UI orchestration, player & timeline engine
│   │   ├── episodes.js            # Episode manifest validator & schema
│   │   ├── cues.js                # Subtitle cues & sync timing
│   │   ├── categories.js          # Topic taxonomy & tag filters
│   │   └── stage.js               # Visual overlay and stage animations
│   ├── data/
│   │   └── episodes.json          # Master JSON manifest of all releases
│   ├── thumbs/                    # Episode covers: <id>.webp & <id>.mp4
│   └── art/                       # Story frames: <id>/f01.webp .. f06.webp
├── engine/                        # Automated Content Pipeline
│   ├── pipeline.mjs               # Master runner: prep -> voice -> art -> publish
│   ├── writer.mjs                 # 3-minute script generator (3-part formula)
│   ├── voice.mjs                  # Audio synthesis & duration alignment
│   ├── art.mjs                    # Story frame & prompt generator (Gemini)
│   ├── video-cover.mjs            # 10s looping Veo cover generator
│   └── unit.mjs                   # Automated validation & test suite
├── docs/                          # Developer & Editorial Documentation
│   ├── ARCHITECTURE.md            # System specification
│   ├── EPISODE_FORMULA.md         # 3-minute hourly broadcast structure
│   ├── HOST_PERSONA.md            # Rex Vance voice and guidelines
│   └── DEVELOPMENT.md             # How to run and extend in Antigravity
├── .github/workflows/             # CI/CD & Scheduled Dispatch
│   ├── publish-episode.yml        # Hourly automated release workflow
│   └── gen-video-covers.yml       # Veo video cover generator
└── README.md                      # Project root entry point
```

---

## 3. Data Schema: `data/episodes.json`

Every hourly episode is validated against the following schema:
```json
{
  "id": "2026-10-06-01",
  "date": "2026-10-06",
  "hour": "01:00",
  "kind": "hourly",
  "category": "geopolitics",
  "title": "Quantum Delayed Choice, Pentagon Backdoors & Ukraine Drone Swarms",
  "subject": "Hourly uncensored breakdown of US congressional corruption, Ukraine frontlines, Wheeler's delayed choice, and CIA remote viewing files.",
  "seconds": 180,
  "audio": "audio/2026-10-06-01.mp3",
  "thumb": "thumbs/2026-10-06-01.webp",
  "cover_video": "thumbs/2026-10-06-01.mp4",
  "paragraphs": [
    "Paragraph 1 text (US politics exposed)...",
    "Paragraph 2 text (Global / Ukraine frontline)...",
    "Paragraph 3 text (AI compute scaling)...",
    "Paragraph 4 text (Quantum physics / delayed choice)...",
    "Paragraph 5 text (PEAR lab / remote viewing)...",
    "Paragraph 6 text (Rex Vance sign-off)..."
  ],
  "art": {
    "frames": [
      { "t": 0, "src": "art/2026-10-06-01/f01.webp", "caption": "Capitol Hill defense lobby backdoors" },
      { "t": 30, "src": "art/2026-10-06-01/f02.webp", "caption": "Ukrainian autonomous drone line" },
      { "t": 60, "src": "art/2026-10-06-01/f03.webp", "caption": "Photonic quantum computing core" },
      { "t": 95, "src": "art/2026-10-06-01/f04.webp", "caption": "Wheeler's delayed-choice interferometer" },
      { "t": 130, "src": "art/2026-10-06-01/f05.webp", "caption": "Declassified Project Stargate coordinates" },
      { "t": 160, "src": "art/2026-10-06-01/f06.webp", "caption": "Rex Vance broadcasting from the bunker" }
    ]
  }
}
```

---

## 4. Key Frontend Features
1. **10s Looping Video Covers:**
   - In desktop and mobile views, cards and hero headers render `<video autoplay loop muted playsinline poster="thumbs/<id>.webp" src="thumbs/<id>.mp4">`.
   - Smooth fallback to static `.webp` on mobile data saver or error.
2. **Synchronized Story Art Layer:**
   - During audio playback, the art overlay updates in real-time based on paragraph timestamps `f.t`.
   - Subtle Ken-Burns pan and dissolve transitions.
3. **Synchronized Subtitle Strip:**
   - Word-level / phrase-level highlight tracking the audio waveform.
4. **Instant Offline Playback:**
   - Service worker ready, localStorage playback resume, zero external framework overhead.
