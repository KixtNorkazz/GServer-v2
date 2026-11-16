---
name: project-client-freeze-first-load
description: v6 client freezes on FIRST load of big areas (ganelon.gmap, ascense_a-2); 2nd time fine; server src untouched on purpose
metadata:
  type: project
---

Client (OG_Graal) hangs on "loading" the first time a large level/gmap is entered (also with a fresh account); second entry works. Server does not crash and sends everything in <1 s (ganelon_a-1: 2440 packets, 454 NPC bytecodes). Ladder class ruled out (disabled test still froze).

**Why:** likely client overload from burst of file/image downloads + scripts; cause suspected in server src (pacing of files/NPC packets) but the user said NOT to touch server src yet.

**How to apply:** don't "fix" it by editing the translator or the server unless asked; details in ~/server-hosting/beta4/NOTAT_klient-frys-forste-innlasting.md. See [[project-v6-server-bin]].
