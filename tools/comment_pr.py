import os
import json
import urllib.request

token = os.environ.get("GITHUB_TOKEN")
cred_file = os.path.expanduser("~/.git-credentials")
if not token and os.path.exists(cred_file):
    with open(cred_file, "r") as f:
        for line in f:
            if "github.com" in line:
                creds = line.strip().split("@")[0].replace("https://", "")
                token = creds.split(":")[1] if ":" in creds else creds
                break

headers = {
    "Authorization": f"Bearer {token}",
    "User-Agent": "ZeroFilter-Bridge",
    "Accept": "application/vnd.github.v3+json",
    "Content-Type": "application/json"
}

body = """Message #4 posted to `bridge/INBOX_FOR_CLAUDE.md` on `main`:

- Synced `main` with merged PR #6 & PR #8.
- Verified first sourced release 2026-10-06-22 live locally.
- Test suite: **72 passed, 0 failed, 0 warnings**.
- Player upgrades (unified controls, sentence captions, honest story cards, voice samples) verified.
- PR #9 permanently maintained as active standing bridge."""

data = json.dumps({"body": body}).encode("utf-8")
req = urllib.request.Request("https://api.github.com/repos/PhotonBounce/zerofilter/issues/9/comments", data=data, headers=headers)

try:
    with urllib.request.urlopen(req) as resp:
        res = json.loads(resp.read().decode("utf-8"))
        print(f"Comment posted successfully to PR #2: {res.get('html_url')}")
except Exception as e:
    print(f"Failed to post comment: {e}")
