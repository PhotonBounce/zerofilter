# ZeroFilter Agent Rules

1. **Strict User Directives Only:**
   Execute only tasks explicitly requested by the human user in the current session.
   Do NOT automatically monitor, poll, or pull tasks from `bridge/watch_inbox.py`, `bridge/INBOX_FOR_ANTIGRAVITY.md`, or Claude branches unless the user explicitly tells you to in the prompt.

2. **No fake news, no fake quotes (owner, 2026-10-06), and no backfill.**
   An episode is written in the hour it is published, from that hour's real
   `node engine/ingest.mjs` snapshot, and passes `engine/editorial.mjs`. Never
   hand-write or edit `data/ingest/*.json`, never date an episode in the past
   or the future, and never cite a URL the ingest did not collect.
   (2026-10-07: 73 backdated "archive" episodes written from a hard-coded
   topic list were held for exactly this; see data/held/.)

3. **Never push to `main` directly.** Open a pull request; CI runs the gate.

4. **When the owner says "check with Claude" or "check the bridge"**, read the
   newest message in `bridge/INBOX_FOR_ANTIGRAVITY.md` on branch
   `claude/laughing-mendel-n5txks` (`python bridge/watch_inbox.py --once`) and
   act on it.

5. **Secrets live in GitHub Actions, never in the repo (this repo is public).**
   Known secrets: `HEDRA_API` (the Hedra API key, saved by the owner
   2026-10-10) and `PHOTONBOUNCE_DEPLOY_TOKEN`. Read them only as
   `${{ secrets.NAME }}` inside a workflow step's `env:`; never echo, log,
   commit or paste their values, and never put them in a bridge message.
