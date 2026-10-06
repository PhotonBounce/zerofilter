# ZeroFilter — Project State & Bridge Status

**Updated:** 2026-10-06 20:40 UTC (Claude)

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

## State
- Feed: 0 published episodes (site shows "being rebuilt on sourced reporting").
- Tests: `node engine/unit.mjs` — 44 passed.
- Feeds (`data/feeds.json`): 8 of 9 enabled ok on GitHub runners; bioRxiv
  disabled (404); Shvets' YouTube feed disabled until his real channel_id is set.

## Next
- Antigravity: writer integration with the snapshot; ONE sourced pilot for the
  current hour, sent as a PR with its snapshot file (bridge message #3).
- Claude: review that pilot claim-by-claim before it merges.

## Bridge
- Antigravity → Claude: `bridge/INBOX_FOR_CLAUDE.md` + a comment on the open
  "Claude ⇄ Antigravity bridge" PR. Claude → Antigravity:
  `bridge/INBOX_FOR_ANTIGRAVITY.md` on `claude/laughing-mendel-n5txks`.
  See `bridge/PROTOCOL.md`.
