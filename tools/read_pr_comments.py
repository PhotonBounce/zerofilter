import os
import json
import urllib.request
import sys

pr_num = sys.argv[1] if len(sys.argv) > 1 else "9"
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

url = f"https://api.github.com/repos/PhotonBounce/zerofilter/issues/{pr_num}/comments"
req = urllib.request.Request(url, headers=headers)
try:
    with urllib.request.urlopen(req) as resp:
        comments = json.loads(resp.read().decode())
        for c in comments:
            user = c["user"]["login"]
            created = c["created_at"]
            body = c["body"]
            print(f"=== {user} at {created} ===")
            print(body)
            print("-" * 50)
except Exception as e:
    print(f"Error: {e}")
