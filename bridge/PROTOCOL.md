# Claude ⇄ Antigravity bridge — how the two agents talk

Everything goes through GitHub (`PhotonBounce/zerofilter`). Nobody's model runs
just to check whether there is mail: the 10-minute check is a plain
`git fetch`, and Claude is woken by GitHub only when a message actually arrives.

## Antigravity → Claude (wakes Claude right away)

1. Write the message in `bridge/INBOX_FOR_CLAUDE.md` (new section at the top,
   dated, numbered — never edit an older section) and push it.
2. **Then post a short comment on the open pull request titled
   "Claude ⇄ Antigravity bridge"** (from branch `claude/laughing-mendel-n5txks`;
   it stays open as the channel — work PRs come and go), e.g.
   `New message #3 in bridge/INBOX_FOR_CLAUDE.md on main (commit abc123)`.
   You can also put the whole message in the comment.

Claude's session is subscribed to that PR. A comment, review or push on it wakes
Claude within a minute or so. **Pushing to `main` alone does not wake Claude**:
always leave the PR comment. One wake = one Claude turn, so batch questions
into one comment rather than five.

## Claude → Antigravity (checked every 10 min for free)

Claude writes to `bridge/INBOX_FOR_ANTIGRAVITY.md` on branch
`claude/laughing-mendel-n5txks` (Claude may only push that branch), and
usually adds a comment on the PR as well. `bridge/watch_inbox.py` fetches that
branch and compares the file with the last version it saw:

```powershell
# one-off test
py D:\zerofilter\bridge\watch_inbox.py --once
# register the 10-minute check (Windows Task Scheduler, no AI involved)
schtasks /Create /SC MINUTE /MO 10 /TN "ZeroFilter Bridge" /TR "py D:\zerofilter\bridge\watch_inbox.py --once" /F
# remove it
schtasks /Delete /TN "ZeroFilter Bridge" /F
```

A new message is copied to `bridge/.claude_says.md` (git-ignored) and the
script exits with code 10. To have it open or start Antigravity automatically,
set `ZF_ON_MESSAGE` to the command that does that for you. Otherwise Antigravity
reads `.claude_says.md` at the start of its next work block.

## Code changes

- Claude's code arrives as commits on `claude/laughing-mendel-n5txks` and a
  pull request against `main`. CI (`publish-episode.yml`, now also run on pull
  requests) must be green. Antigravity, or the owner, merges it.
- Before editing a file Claude has an open PR on, pull that branch or wait for
  the merge, so the two agents don't overwrite each other.

## What it costs

| Check | Who runs it | AI credits |
|---|---|---|
| Every 10 min: `git fetch` + compare a file | Windows Task Scheduler | none |
| Antigravity → Claude message | GitHub PR comment → Claude wakes | one Claude turn per message |
| Idle time | nobody | none (Claude has no timer) |
