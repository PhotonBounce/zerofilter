import urllib.request
import json

token = None
with open(r'C:\Users\user/.git-credentials', 'r') as f:
    for line in f:
        if 'github.com' in line:
            creds = line.strip().split('@')[0].replace('https://', '')
            token = creds.split(':')[1] if ':' in creds else creds
            break

if not token:
    print('No token found')
    exit(0)

headers = {'Authorization': f'Bearer {token}', 'User-Agent': 'ZeroFilter-Deployer', 'Accept': 'application/vnd.github.v3+json'}
req = urllib.request.Request('https://api.github.com/user', headers=headers)
login = None
try:
    with urllib.request.urlopen(req) as resp:
        user_info = json.loads(resp.read())
        login = user_info.get('login')
        print('Authenticated as GitHub user:', login)
except Exception as e:
    print('User check failed:', e)

for owner in ['PhotonBounce', login]:
    if not owner: continue
    req = urllib.request.Request(f'https://api.github.com/repos/{owner}/zerofilter', headers=headers)
    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read())
            print(f'Repo found: {owner}/zerofilter -> {data.get("html_url")}')
    except Exception as e:
        print(f'Repo {owner}/zerofilter: {e}')
