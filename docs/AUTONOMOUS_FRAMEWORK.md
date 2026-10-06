# Universal Autonomous DevOps & 24/7 Agent Keep-Awake Framework
## ZeroFilter Architecture & Execution Contract

---

### 1. Zero-Branch-Switching Deployment Engine
All production portal releases are deployed directly from the active working tree to GitHub Pages via low-level Git plumbing in [`tools/deploy_to_gh_pages.py`](file:///d:/zerofilter/tools/deploy_to_gh_pages.py):
* **Target:** Confined to `photon-bounce.com/zerofilter/` (under branch `gh-pages` of repository `PhotonBounce/photonbounce`).
* **Root Protection:** Absolute isolation. Root files (`/index.html`, `/assets/`, `/zbilli/`, `/titry/`) are never touched or modified.
* **Mechanism:**
  1. Build clean production tree from `web/` into a temporary isolated index (`GIT_INDEX_FILE`).
  2. Fetch remote parent commit on `gh-pages`.
  3. Mount clean portal subtree under prefix `zerofilter/` without branch checkout.
  4. Create commit object (`git commit-tree`) directly on top of remote parent.
  5. Push headless commit directly to `origin/gh-pages`.

---

### 2. 24/7 Keep-Awake Heartbeat Daemon
To prevent agent idle halts and keep throughput continuous overnight:
* **Cadence:** Every 5 minutes (`*/5 * * * *`).
* **Invocation:** `schedule(CronExpression="*/5 * * * *", IsDaemon=true, Prompt="...")`.
* **Execution:** Inspects `data/queue.json`, checks `bridge/INBOX_FOR_ANTIGRAVITY.md`, verifies production state on disk, and advances the next release.

---

### 3. State-on-Disk Architecture ("Dropped Brain" Defense)
To ensure full resilience against context truncations, state is persisted to disk on every single item:
* [`status/pipeline_state.json`](file:///d:/zerofilter/status/pipeline_state.json): Active stage, current episode ID, completed episodes count, last deploy commit, timestamps, and error flags.
* [`data/queue.json`](file:///d:/zerofilter/data/queue.json): Priority-ordered backlog of pending hourly broadcasts.
* [`data/registry.json`](file:///d:/zerofilter/data/registry.json): Historical ledger of published broadcasts with runtime metadata.

---

### 4. Zero-Approval Autonomous Execution Contract
Per project directive, interactive confirmation modals and approval requests are waived:
1. Make proactive architectural and bug-fixing choices automatically.
2. Advance items through the verification loop:
   $$\text{Process Queue Item} \longrightarrow \text{Run Unit Tests (48/48)} \longrightarrow \text{Deploy to Production} \longrightarrow \text{Commit to Git} \longrightarrow \text{Next Item}$$
