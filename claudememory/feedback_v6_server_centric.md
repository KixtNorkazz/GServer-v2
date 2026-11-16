---
name: feedback_v6_server_centric
description: v6 work belongs in the server (beta4/bin) rather than the client; image-only NPCs are normal there
metadata:
  type: feedback
---

For v6 most of the work lives in `/home/Kixt/server-hosting/beta4/bin/*` (server dir `bin/servers/default`), not in the client: weapons, gs2cache, gmaps, serveroptions, source in `beta4/server/src`.

NPCs with an empty or comment-only client script are normal and meant to stay that way: in the new style a plain image on an NPC adds detail to a level. Do not count them as "failed" translations.

**Why:** the user said so after I counted 3 213 empty scripts as untranslated.
**How to apply:** report translation coverage without the empty/comment-only scripts; look for fixes on the server side first. Related: [[project_v6_server_bin]].
