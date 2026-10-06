# bridge/watch_inbox.py — Zero-Credit Heartbeat Watcher
import os
import time
import sys

INBOX_PATH = r"D:\zerofilter\bridge\INBOX_FOR_ANTIGRAVITY.md"

def get_file_sig(path):
    if not os.path.exists(path):
        return 0, 0
    st = os.stat(path)
    return st.st_mtime, st.st_size

def main():
    print(f"Monitoring {INBOX_PATH} for updates from Claude Code...")
    initial_mtime, initial_size = get_file_sig(INBOX_PATH)
    
    # Sleep 5s intervals — negligible CPU, zero LLM token consumption
    while True:
        time.sleep(5)
        curr_mtime, curr_size = get_file_sig(INBOX_PATH)
        
        # Check if modified and has actual content
        if (curr_mtime > initial_mtime or curr_size != initial_size) and curr_size > 50:
            with open(INBOX_PATH, "r", encoding="utf-8") as f:
                content = f.read()
            print(f"\n[ALERT] Claude has updated INBOX_FOR_ANTIGRAVITY.md ({curr_size} bytes):\n")
            print(content[:500] + ("..." if len(content) > 500 else ""))
            break

if __name__ == "__main__":
    main()
