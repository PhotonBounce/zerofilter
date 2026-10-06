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
    "Accept": "application/vnd.github.v3+json"
}

req = urllib.request.Request("https://api.github.com/repos/PhotonBounce/zerofilter/pulls?state=all", headers=headers)
try:
    with urllib.request.urlopen(req) as resp:
        pulls = json.loads(resp.read().decode())
        for p in pulls:
            title = p['title'].encode('ascii', 'replace').decode('ascii')
            print(f"PR #{p['number']}: [{p['state']}] {title} (head: {p['head']['ref']})")
except Exception as e:
    print(f"Error querying pulls: {e}")
