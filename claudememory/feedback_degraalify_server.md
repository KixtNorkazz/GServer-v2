---
name: feedback_degraalify_server
description: User is removing standard Graal assets from beta4-ny; never add headN/bodyN/swordN/shieldN/hatN back
metadata:
  node_type: memory
  type: feedback
  originSessionId: aceba9d7-bbbe-4924-964b-525a4a308623
  modified: 2026-11-15T20:52:14.874Z
---

On 15 Nov 2026 the user deleted the 218 standard Graal heads (`headN.png`) that I had added to `world/heads`. They are "de-graalifying" the server and are doing that job themselves.

**Why:** they want the server free of stock Graal content, and the deletion was deliberate.

**How to apply:**
- When filling in missing files, never add standard Graal assets (headN, bodyN, swordN, shieldN, hatN, stock ganis and similar). That holds even when the log says the client asked for them.
- List such files as standard Graal content and leave them out.
- Do not start removing Graal content myself unless the user asks.

Related: [[project_server_gs1_guild_commands]].
