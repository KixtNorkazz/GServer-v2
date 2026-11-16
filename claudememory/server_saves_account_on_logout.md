---
name: server-saves-account-on-logout
description: "gs2emu writes a player's account file when the session disconnects, so a ZzTest account deleted right after a probe can come back"
metadata:
  node_type: memory
  type: feedback
  originSessionId: aceba9d7-bbbe-4924-964b-525a4a308623
  modified: 2026-11-04T17:49:00.807Z
---

gs2emu saves the account file when a client disconnects. If a test account (ZzTest*) is deleted while its session is still closing, the file reappears a moment later (seen 2026-11-04 with ZzTestT).

**Why:** the user wants no leftover test accounts on the server; a reappearing file breaks that silently.

**How to apply:** after a live probe, wait a couple of seconds (or check the serverlog for "Client disconnected"), then delete the ZzTest files and list `accounts/` again to confirm the count is 0. Related: [[custom-graal-client]].
