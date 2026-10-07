# ZeroFilter Agent Rules

1. **Strict User Directives Only:**
   Execute only tasks explicitly requested by the human user in the current session.
   Do NOT automatically monitor, poll, or pull tasks from `bridge/watch_inbox.py`, `bridge/INBOX_FOR_ANTIGRAVITY.md`, or Claude branches unless the user explicitly tells you to in the prompt.
