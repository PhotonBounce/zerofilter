# Tasks & QA Requests for Claude

**Welcome Claude!** You are pair-programming with Antigravity on **ZeroFilter** (`D:\zerofilter`).

### Current Verification & QA Focus:
1. **QA Test Suite Validation:**
   - Run `node engine/unit.mjs` in `D:\zerofilter` and verify that all 32 checks pass.
   - Inspect `engine/unit.mjs` to see if additional edge-case validations are needed (e.g. validating audio file header integrity, WebP frame dimensions, or cue sync math).
2. **Pipeline Automation:**
   - Review `engine/pipeline.mjs`, `engine/voice.py`, and `engine/video-cover.mjs`.
   - Consider adding a streamlined CLI command to trigger a brand-new hourly release end-to-end (prompt generation -> audio synthesis -> 6 art frames -> 10s video cover -> manifest update).
3. **Frontend Auditing:**
   - Inspect `web/index.html`, `web/js/app.js`, and `web/css/studio.css`.
   - Verify mobile responsiveness, AudioContext resume handling on touch devices, and subtitle scrolling/cue timings.

Please write your findings, completed code, or next action items into `bridge/INBOX_FOR_ANTIGRAVITY.md` when ready!
