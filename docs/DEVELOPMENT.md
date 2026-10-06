# ZeroFilter: Development & Next Steps Guide

This guide describes how to open, run, and expand **ZeroFilter** in a separate Antigravity IDE instance.

---

## 1. Opening the Project in Antigravity

1. In Antigravity (or command palette `File -> Open Folder...`), open:
   ```
   D:\zerofilter
   ```
2. The project is an independent Git repository configured with its own `main` branch.

---

## 2. Running Locally

The web portal requires no build step—it runs directly via any static HTTP server:

```bash
# Option 1: Node.js static server
npx serve D:\zerofilter\web -l 4200

# Option 2: Python 3 built-in server
python -m http.server 4200 --directory D:\zerofilter\web
```

Open your browser to:
```
http://localhost:4200/
```

---

## 3. Running Engine & QA Tests

```bash
cd D:\zerofilter\engine

# Run unit tests (verifies episode schema, audio bounds, captions, and cues)
node unit.mjs

# Run test episode generation dry run
node pipeline.mjs --dry-run
```

---

## 4. Next Steps for the New Antigravity Instance

When you launch the new Antigravity instance on `D:\zerofilter`, prompt it with:

> *"Resume development on ZeroFilter portal in D:\zerofilter. Review docs/EPISODE_FORMULA.md, docs/HOST_PERSONA.md, and docs/ARCHITECTURE.md. Run engine/unit.mjs, generate the first 3 pilot hourly releases with full 3-minute scripts, voice them, generate 6 story frames + 10s looping video covers per release, and verify live audio/video playback in web/index.html."*

### Immediate Milestones:
1. **Pilot Episodes Production:**
   - Episode 01: *Wheeler's Quantum Mirror, Theocratic Creep & The Ukraine Drone Line*
   - Episode 02: *PEAR Lab Mind-Machine Data, MAGA Christofascists & Corrupt DNC PACs*
   - Episode 03: *Thomas Campbell's Virtual Reality, AI Frontier Models & Taiwan Strait Intel*
2. **Audio Voice Profile:**
   - Configure ElevenLabs voice ID or Google Cloud / Gemini Audio voice tuned for Rex Vance (fast-paced, gritty, confident American baritone).
3. **Veo Video Covers:**
   - Run `node engine/video-cover.mjs generate thumbs/<id>.webp thumbs/<id>.mp4` to populate 10s looping covers.
4. **Deploy Target:**
   - Set up GitHub Actions or FTP deployment to your chosen domain (e.g. `zerofilter.news`).
