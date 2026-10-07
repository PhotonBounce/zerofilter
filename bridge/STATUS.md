# ZeroFilter — Project State & Bridge Status

**Updated:** 2026-10-07 00:57 UTC (Claude)

## Live
- https://photon-bounce.com/zerofilter/ — uploaded by PhotonBounce/photonbounce
  `deploy-zerofilter.yml`. No token (owner's choice): Claude starts it after a
  change that should go live; last upload 2026-10-06 20:36 UTC, live check ok.
  This repo's `deploy-ftp.yml` still runs the gate + build on every push.
- https://photonbounce.github.io/zerofilter/ — `deploy-pages.yml`.
- Both ship `dist/` from `engine/build_site.mjs`: the player plus only the
  episodes that pass the editorial + provenance gate.

## Rules (owner, 2026-10-06): no fake quotes, no fake news, nothing dated ahead
- `docs/EPISODE_FORMULA.md` §0 (rules 1–7), enforced by `engine/editorial.mjs`.
- Every published episode names its ingest snapshot (`data/ingest/YYYY-MM-DD-HH.json`,
  from `node engine/ingest.mjs`); P0/P1 news and every quote must be in it.
- The 151 unsourced episodes are held in `data/held/episodes-unverified.json`.
- The 5-minute generator is stopped; `data/queue.json` is paused.

## Clock
- `engine/ingest.mjs` refuses to run when the PC clock is more than 2 min off
  internet time (the producing PC ran ~2 h fast on 2026-10-06). Fix the
  Windows clock before collecting; snapshots record `clock_skew_s`.

## State
- Feed: 1 published episode, `2026-10-06-22` (Antigravity's sourced pilot, review fixes applied by
  Claude at the owner's request, re-voiced on a runner: 177.6 s).
- Tests: `node engine/unit.mjs` — 72 passed.
- Feeds (`data/feeds.json`): 8 of 9 enabled ok on GitHub runners; bioRxiv
  disabled (404); Shvets' YouTube feed disabled until his real channel_id is set.

## Player & art (owner, 2026-10-07)
- One control bar under the picture; captions (current sentence) under the bar.
- Story art = factual story cards: each paragraph's real headlines, source and
  date (see `web/art/2026-10-06-22/`). No decorative "intel" graphics:
  nothing that looks like classified data, maps or telemetry that isn't real.
- Voice: owner is choosing from `samples/` (6 edge-tts voices); ElevenLabs is
  the paid option.

## Next
- Antigravity: next episodes, one per real hour, each as a PR with its
  snapshot. Write only what each source says: "reportedly" stays
  "reportedly", a proposal is not a proof, and give the exact figures (see
  Claude's review on #7). Six DIFFERENT frames per episode.
- Voice without the PC: push `bridge/voice-request.json` = {"episode": "<id>"}
  on a claude/** branch, or run `voice-episode.yml` by hand.
- Claude: reviews each episode claim by claim, merges, starts the
  photon-bounce.com upload.

## Bridge
- Antigravity → Claude: `bridge/INBOX_FOR_CLAUDE.md` + a comment on the open
  "Claude ⇄ Antigravity bridge" PR. Claude → Antigravity:
  `bridge/INBOX_FOR_ANTIGRAVITY.md` on `claude/laughing-mendel-n5txks`.
  See `bridge/PROTOCOL.md`.
