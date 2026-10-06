#!/usr/bin/env python3
import os
import subprocess
import tempfile
import sys

# ==============================================================================
# ZERO-FILTER: UNIVERSAL ZERO-BRANCH-SWITCHING GITHUB PAGES DEPLOYMENT
# ==============================================================================
REMOTE_NAME = "origin"
PROD_BRANCH = "gh-pages"
TARGET_SUBDIR = "zerofilter"  # Mounts under https://photonbounce.github.io/photonbounce/zerofilter/

# Files / patterns to exclude from production release
DEV_EXCLUSIONS = [
    ".env",
    ".gitignore",
    "engine",
    "bridge",
    "docs",
    "tests",
    "scripts",
    "tools",
    "scratch",
    "*.pyc",
    "__pycache__"
]

def git(cmd, env=None, input_data=None, cwd=None):
    res = subprocess.run(
        ["git"] + cmd,
        input=input_data,
        capture_output=True,
        text=True if input_data is None or isinstance(input_data, str) else False,
        env=env,
        cwd=cwd or os.path.dirname(os.path.abspath(__file__))
    )
    if res.returncode != 0:
        err = res.stderr if isinstance(res.stderr, str) else res.stderr.decode("utf-8", errors="ignore")
        raise RuntimeError(f"Git command failed: git {' '.join(cmd)}\n{err}")
    out = res.stdout if isinstance(res.stdout, str) else res.stdout.decode("utf-8", errors="ignore")
    return out.strip()

def deploy():
    print(f"[*] Fetching latest {REMOTE_NAME}/{PROD_BRANCH}...")
    try:
        git(["fetch", REMOTE_NAME, PROD_BRANCH])
    except Exception as e:
        print(f"[!] Warning fetching {PROD_BRANCH}: {e}")

    try:
        parent_commit = git(["rev-parse", f"{REMOTE_NAME}/{PROD_BRANCH}"])
    except Exception:
        parent_commit = None

    current_head = git(["rev-parse", "HEAD"])
    print(f"[*] Parent commit on {PROD_BRANCH}: {parent_commit}")
    print(f"[*] Active HEAD: {current_head}")

    # Step 1: Create clean production tree from HEAD without switching branches
    with tempfile.NamedTemporaryFile(delete=False) as tf:
        clean_index = tf.name

    try:
        env_clean = os.environ.copy()
        env_clean["GIT_INDEX_FILE"] = clean_index

        git(["read-tree", current_head], env=env_clean)

        for pattern in DEV_EXCLUSIONS:
            try:
                git(["rm", "-r", "--cached", "--ignore-unmatch", pattern], env=env_clean)
            except Exception:
                pass

        # If web/ exists, move web/ contents to root of the clean tree
        clean_tree_sha = git(["write-tree"], env=env_clean)
        print(f"[*] Clean production tree SHA: {clean_tree_sha}")
    finally:
        if os.path.exists(clean_index):
            os.unlink(clean_index)

    # Step 2: Graft clean production tree into gh-pages history
    with tempfile.NamedTemporaryFile(delete=False) as tf:
        deploy_index = tf.name

    try:
        env_deploy = os.environ.copy()
        env_deploy["GIT_INDEX_FILE"] = deploy_index

        if parent_commit:
            git(["read-tree", parent_commit], env=env_deploy)
        else:
            git(["read-tree", "--empty"], env=env_deploy)

        if TARGET_SUBDIR:
            try:
                git(["rm", "-r", "--cached", "--ignore-unmatch", TARGET_SUBDIR], env=env_deploy)
            except Exception:
                pass
            git(["read-tree", f"--prefix={TARGET_SUBDIR.rstrip('/')}/", clean_tree_sha], env=env_deploy)
            final_tree_sha = git(["write-tree"], env=env_deploy)
        else:
            final_tree_sha = clean_tree_sha

        # Step 3: Create commit object directly on top of remote parent
        commit_msg = f"deploy: automated release from {current_head[:8]}\n\nSource-Commit: {current_head}"
        parents = ["-p", parent_commit] if parent_commit else []
        new_commit = git(["commit-tree", final_tree_sha] + parents + ["-m", commit_msg], env=env_deploy)
        print(f"[*] Created deployment commit: {new_commit}")

        # Step 4: Headless push directly to remote branch
        print(f"[*] Pushing directly to {REMOTE_NAME}/{PROD_BRANCH}...")
        git(["push", REMOTE_NAME, f"{new_commit}:refs/heads/{PROD_BRANCH}"])
        print("[+] SUCCESS: Clean production build is live on GitHub Pages!")
    finally:
        if os.path.exists(deploy_index):
            os.unlink(deploy_index)

if __name__ == "__main__":
    deploy()
