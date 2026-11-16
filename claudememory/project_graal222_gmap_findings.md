---
name: project_graal222_gmap_findings
description: Why Graal_222 (v2) failed on gmaps / showed wrong tiles on the install server (port 9095); four fixes applied 12 Nov 2026 and what to keep on a new build
metadata:
  type: project
---

Found 12 Nov 2026 with Graal_222.exe on an empty cache against `~/server-hosting/beta4/install` (details + pictures: `beta4/NOTAT_graal222-gmap_2026-11-12.md`, `beta4/rapporter/graal222_2026-11-12/`). All four were applied to `install` on 12 Nov 2026 at the user's request (backups: `~/server-hosting/backup/graal222-2026-11-12/`); verified with Graal_222 on an empty cache. Keep them on a new gserver build: config line, gmap-fil-foerst patch, level lines, split TileDefs..TileDefs5. `protectedweapons` must be written WITHOUT spaces after the commas (with spaces only the first weapon was handed out).

1. `Player::sendFile` sends no answer for a missing file unless `warnonmissingfiles = true`; Graal_222 stops asking for files after 4 unanswered ones (the missing `plisticon*.png` of `playerlisticons`).
2. `install/gs2emu` (built 5 Nov) lacks `patches/gmap-fil-foerst.patch`; `bin/gs2emu` has it and, run on the install data, fixes the first-login gmap for Graal_222 too.
3. Graal_222 picks an `addtiledef2` piece per tile by size, not order (`FUN_0052a8dc`: a later piece wins only if smaller in BOTH width and height). A base tileset written as `addtiledef2 X,#L,0,0` (2048x512) hides `val_bridgetontest2.gif` (688x512). Fix in the level NPCs: `addtiledef X,#L,0;`.
4. `weaponTileDefs.txt` client script is 81 KB; the 2-byte length wraps, Graal_222 reads only the first 15,829 bytes. Needs splitting under 28,767 bytes each (as done for v6).

**How to apply:** Graal_222 runs fine under the system Wine 11 on `Xvfb` (unlike v6); copy the client folder, files dated before 2020 = stock, point the copy's `arrays2.dat` line 1 at 127.0.0.1 (the public 91.99.73.49:9111 did not answer from this box). Downloads keep the server's mtime, so `find -newer` does not show them; the client saves tile definitions in `levels/tiledefs/tiledefs<server>.txt`. Related: [[reference_v6_client_on_linux]], [[server_gmap_bounds_patch]].
