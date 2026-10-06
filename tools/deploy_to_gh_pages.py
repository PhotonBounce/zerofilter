# tools/deploy_to_gh_pages.py — Universal Zero-Branch-Switching Deployer
import os
import subprocess
import tempfile
import uuid
import sys

REPO_DIR = r"D:\photonbounce"
TARGET_SUBDIR = "zerofilter"
SOURCE_WEB_DIR = r"D:\zerofilter\web"
PROD_BRANCH = "gh-pages"

def get_auth_remote_url():
    token = None
    cred_file = os.path.expanduser(r"~\.git-credentials")
    if os.path.exists(cred_file):
        with open(cred_file, "r") as f:
            for line in f:
                if "github.com" in line:
                    creds = line.strip().split("@")[0].replace("https://", "")
                    token = creds.split(":")[1] if ":" in creds else creds
                    break
    if token:
        return f"https://x-access-token:{token}@github.com/PhotonBounce/photonbounce.git"
    return "https://github.com/PhotonBounce/photonbounce.git"

def git(cmd, cwd=REPO_DIR, env=None, input_data=None):
    base_env = os.environ.copy()
    base_env["GIT_TERMINAL_PROMPT"] = "0"
    if env:
        base_env.update(env)
    
    res = subprocess.run(
        ["git"] + cmd,
        input=input_data,
        capture_output=True,
        text=True if input_data is None or isinstance(input_data, str) else False,
        cwd=cwd,
        env=base_env
    )
    if res.returncode != 0:
        err = res.stderr if isinstance(res.stderr, str) else res.stderr.decode("utf-8", errors="ignore")
        raise RuntimeError(f"Git command failed: git {' '.join(cmd)}\n{err}")
    out = res.stdout if isinstance(res.stdout, str) else res.stdout.decode("utf-8", errors="ignore")
    return out.strip()

def deploy():
    print(f"[*] Starting Zero-Branch-Switching Deploy to {PROD_BRANCH}...", flush=True)
    auth_url = get_auth_remote_url()

    # Step 1: Fetch remote branch parent commit
    print(f"[*] Fetching remote parent commit for {PROD_BRANCH}...", flush=True)
    git(["fetch", auth_url, f"{PROD_BRANCH}:refs/remotes/origin/{PROD_BRANCH}"])
    parent_commit = git(["rev-parse", f"refs/remotes/origin/{PROD_BRANCH}"])
    print(f"[*] Parent commit on {PROD_BRANCH}: {parent_commit}", flush=True)

    # Step 2: Build clean tree from SOURCE_WEB_DIR into a temporary isolated index
    clean_index = os.path.join(tempfile.gettempdir(), f"git_clean_idx_{uuid.uuid4().hex}")
    if os.path.exists(clean_index): os.unlink(clean_index)

    try:
        env_clean = {"GIT_INDEX_FILE": clean_index, "GIT_WORK_TREE": SOURCE_WEB_DIR}
        git(["add", "-A", "."], cwd=REPO_DIR, env=env_clean)
        clean_tree_sha = git(["write-tree"], cwd=REPO_DIR, env=env_clean)
        print(f"[*] Clean portal production tree SHA: {clean_tree_sha}", flush=True)
    finally:
        if os.path.exists(clean_index):
            os.unlink(clean_index)

    # Step 3: Mount clean production tree under target prefix in gh-pages index
    deploy_index = os.path.join(tempfile.gettempdir(), f"git_deploy_idx_{uuid.uuid4().hex}")
    if os.path.exists(deploy_index): os.unlink(deploy_index)

    try:
        env_deploy = {"GIT_INDEX_FILE": deploy_index}
        git(["read-tree", parent_commit], env=env_deploy)

        if TARGET_SUBDIR:
            try:
                git(["rm", "-r", "--cached", "--ignore-unmatch", TARGET_SUBDIR], env=env_deploy)
            except Exception:
                pass
            git(["read-tree", f"--prefix={TARGET_SUBDIR.rstrip('/')}/", clean_tree_sha], env=env_deploy)
            final_tree_sha = git(["write-tree"], env=env_deploy)
        else:
            final_tree_sha = clean_tree_sha

        print(f"[*] Final merged tree SHA for gh-pages: {final_tree_sha}", flush=True)

        # Step 4: Create cryptographic commit object directly on top of remote parent
        commit_msg = (
            f"deploy(zerofilter): automated zero-branch-switch release\n\n"
            f"Target: /{TARGET_SUBDIR}/\n"
            f"Tree: {final_tree_sha}\n"
            f"Parent: {parent_commit}"
        )
        new_commit = git(["commit-tree", final_tree_sha, "-p", parent_commit, "-m", commit_msg], env=env_deploy)
        print(f"[*] Created deployment commit: {new_commit}", flush=True)

        # Step 5: Direct headless push to remote gh-pages
        print(f"[*] Pushing directly to {PROD_BRANCH}...", flush=True)
        git(["push", auth_url, f"{new_commit}:refs/heads/{PROD_BRANCH}"])
        print(f"[+] SUCCESS: ZeroFilter is live at https://photon-bounce.com/{TARGET_SUBDIR}/", flush=True)
    finally:
        if os.path.exists(deploy_index):
            os.unlink(deploy_index)

if __name__ == "__main__":
    deploy()
