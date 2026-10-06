import urllib.request
import json
import subprocess
import os

token = None
with open(r'C:\Users\fucktrumpandrednecks\.git-credentials', 'r') as f:
    for line in f:
        if 'github.com' in line:
            creds = line.strip().split('@')[0].replace('https://', '')
            token = creds.split(':')[1] if ':' in creds else creds
            break

headers = {
    'Authorization': f'Bearer {token}',
    'User-Agent': 'ZeroFilter-Deployer',
    'Accept': 'application/vnd.github.v3+json',
    'Content-Type': 'application/json'
}

payload = json.dumps({
    'name': 'zerofilter',
    'description': 'ZeroFilter — Unfiltered Geopolitics, Quantum Reality & Frontier Science (Hourly 3-Minute Intel Releases)',
    'private': False,
    'has_issues': True,
    'has_wiki': True
}).encode('utf-8')

# Try creating under user / org
req = urllib.request.Request('https://api.github.com/user/repos', data=payload, headers=headers, method='POST')
try:
    with urllib.request.urlopen(req) as resp:
        data = json.loads(resp.read())
        repo_url = data.get('html_url')
        clone_url = data.get('clone_url')
        print(f'Successfully created repository: {repo_url}')
except Exception as e:
    print('Failed to create repo:', e)
    if hasattr(e, 'read'):
        print(e.read().decode('utf-8'))
