# bridge/watch_inbox.py — Zero-Credit Bridge Watcher (Claude -> Antigravity)
#
# Claude works in the cloud and never touches D:\zerofilter, so watching the
# local file only fires after someone pulls. This checks GitHub instead:
# one `git fetch` of Claude's branch, then compares the inbox file there with
# the last version seen. No model is called — zero AI credits per check.
#
#   python bridge/watch_inbox.py --once     # one check, for Task Scheduler (every 10 min)
#   python bridge/watch_inbox.py --loop     # check every 10 min in a terminal
#
# Exit code 0 = nothing new, 10 = new message (written to bridge/.claude_says.md).
# If the environment variable ZF_ON_MESSAGE is set, it is run as a shell command
# when a new message arrives (e.g. a script that opens Antigravity on the file).
import hashlib
import os
import subprocess
import sys
import time

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BRANCH = os.environ.get("ZF_CLAUDE_BRANCH", "claude/laughing-mendel-n5txks")
INBOX = "bridge/INBOX_FOR_ANTIGRAVITY.md"
STATE = os.path.join(REPO, "bridge", ".last_seen")
OUT = os.path.join(REPO, "bridge", ".claude_says.md")
INTERVAL = 600  # 10 minutes


def git(*args):
    return subprocess.run(["git", "-C", REPO, *args], capture_output=True, text=True, encoding="utf-8")


def check():
    # Explicit refspec: a shallow or single-branch clone does not track other
    # branches, and a bare `git fetch origin BRANCH` would only fill FETCH_HEAD.
    fetch = git("fetch", "--quiet", "origin", f"+refs/heads/{BRANCH}:refs/remotes/origin/{BRANCH}")
    if fetch.returncode != 0:
        print(f"fetch failed (offline?): {fetch.stderr.strip()[:200]}")
        return False
    show = git("show", f"origin/{BRANCH}:{INBOX}")
    if show.returncode != 0:
        print(f"no {INBOX} on {BRANCH} yet")
        return False
    content = show.stdout
    digest = hashlib.sha256(content.encode("utf-8")).hexdigest()
    seen = open(STATE).read().strip() if os.path.exists(STATE) else ""
    if digest == seen:
        print("no new message from Claude")
        return False
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(content)
    with open(STATE, "w") as f:
        f.write(digest)
    print(f"[NEW] Claude updated {INBOX} on {BRANCH} -> {OUT}")
    print(content[:600] + ("..." if len(content) > 600 else ""))
    hook = os.environ.get("ZF_ON_MESSAGE")
    if hook:
        subprocess.run(hook, shell=True)
    return True


def main():
    if "--loop" in sys.argv:
        while True:
            check()
            time.sleep(INTERVAL)
    sys.exit(10 if check() else 0)


if __name__ == "__main__":
    main()
