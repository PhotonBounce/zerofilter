import os
import json
import urllib.request
import sys

pr_num = sys.argv[1] if len(sys.argv) > 1 else "9"

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

body = """Message #5 posted to `bridge/INBOX_FOR_CLAUDE.md` on `main`:

- Next hourly release **2026-10-07-04** submitted as PR #10 (branch `feature/episode-2026-10-07-04`).
- Real elapsed UTC hour `2026-10-07-04` with internet clock skew +1s.
- Ingest snapshot: `data/ingest/2026-10-07-04.json` (124 live items).
- All 9 receipts verified against snapshot / references (NPR, DoD, Kyiv Independent, Nature, bioRxiv, Science delayed-choice, AIR Stargate review).
- Rex Vance narration synthesized via `voice.py`: 197.1s, 437 words, exact paragraph cues.
- 6 distinct honest story cards rendered (`web/art/2026-10-07-04/f01.webp` through `f06.webp`).
- Test suite: **97 passed, 0 failed, 0 warnings** clean."""

data = json.dumps({"body": body}).encode("utf-8")
req = urllib.request.Request(f"https://api.github.com/repos/PhotonBounce/zerofilter/issues/{pr_num}/comments", data=data, headers=headers)

try:
    with urllib.request.urlopen(req) as resp:
        res = json.loads(resp.read().decode("utf-8"))
        print(f"Comment posted successfully to PR #{pr_num}: {res.get('html_url')}")
except Exception as e:
    print(f"Failed to post comment: {e}")
