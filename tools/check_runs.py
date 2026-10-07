import os
import json
import urllib.request

cred_file = os.path.expanduser("~/.git-credentials")
token = None
if os.path.exists(cred_file):
    with open(cred_file, "r") as f:
        for line in f:
            if "github.com" in line:
                creds = line.strip().split("@")[0].replace("https://", "")
                token = creds.split(":")[1] if ":" in creds else creds
                break

headers = {
    "Authorization": f"Bearer {token}",
    "User-Agent": "ZeroFilter-Bridge",
    "Accept": "application/vnd.github.v3+json"
}

req = urllib.request.Request("https://api.github.com/repos/PhotonBounce/zerofilter/actions/runs?per_page=6", headers=headers)
try:
    with urllib.request.urlopen(req) as resp:
        runs = json.loads(resp.read().decode())
        for r in runs["workflow_runs"]:
            msg = r["head_commit"]["message"].split("\n")[0] if r.get("head_commit") else ""
            print(f"Run #{r['id']}: [{r['status']}/{r['conclusion']}] {r['name']} ({r['head_branch']}) -> {msg[:50]}")
except Exception as e:
    print(f"Error checking runs: {e}")
