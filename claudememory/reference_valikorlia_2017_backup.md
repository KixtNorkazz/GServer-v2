---
name: reference_valikorlia_2017_backup
description: "Where the Valikorlia 2017 backup (GS2/v6 style) is and how to unpack it (unrar, not 7z)"
metadata:
  node_type: memory
  type: reference
  originSessionId: aceba9d7-bbbe-4924-964b-525a4a308623
  modified: 2026-11-05T14:06:11.090Z
---

The 2017 Valikorlia backup is `~/Downloads/val_backup2/valbackups.rar` -> `valbackups/valbackup2017.rar` (48 MB, 4917 files, written for v6: GS2 events, Gui*Ctrl).

**Unpack with `unrar x`, never 7z.** 7z lacks the RAR5 method and silently makes 0-byte files (3596 errors). `~/Downloads/val_backup2/x_2017` is exactly such a broken extraction and can be deleted. `unrar t` says "All OK" on the archive.

`data/` and `logs/` inside hold account lists and server logs: do not read them or let them into exported code.

Survey results and the gaps found are in `client_rev6/NOTES_KILDKODER.md` chapter 7.4. See [[project_custom_graal_client]].
