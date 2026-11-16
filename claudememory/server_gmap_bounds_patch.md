---
name: server-gmap-bounds-patch
description: Local gs2emu fix (gmap cell bounds check) applied 2026-11-03 to ~/server-hosting/beta4; must be re-checked/re-applied when the user builds a new gserver version
metadata:
  node_type: memory
  type: project
  originSessionId: aceba9d7-bbbe-4924-964b-525a4a308623
  modified: 2026-11-03T09:11:06.734Z
---

On 2026-11-03 I patched the user's gs2emu (`~/server-hosting/beta4`, upstream beta4 commit 365bbd29, Debug Ninja build `cmake --build build --target gs2emu` -> `bin/gs2emu_d`, runs in tmux `gserver`).

Bug: a client sending GMAPLEVELX/Y outside the gmap (e.g. -1 when walking off the west edge) was stored as unsigned byte 255 in the account (`MAPX 255`); next login `enterLevel` found no sub-level -> PLO_WARPFAILED, no level, account locked. Also `Level::getSubLevelAtPosition` computes y*width+x so x==width wraps into the next row. Accounts Kixt and KixtNorkazz were hit and repaired by hand (MAPX 0, X 1).

Fix (3 places): `server/include/level/Level.h` new `Level::isValidMapPosition()`; `server/src/player/PlayerProps.cpp` GMAPLEVELX/GMAPLEVELY -> `SETPROP_RETURN_REVERT` when outside; `server/src/player/PlayerClient.cpp` `PlayerClient::warp()` on a gmap falls back to cell (0,0) and logs `** [Warp] ...`. Patch: `~/server-hosting/beta4/patches/gmap-grensesjekk.patch`; note: `~/server-hosting/beta4/NOTAT_gmap-grensesjekk.md` (Norwegian). Live-tested with throwaway ZzTestM.

`PlayerClient.cpp` also carries the user's own older local change (null check of subLevel in `enterLevel`) — never `git checkout` that file. Other local user changes: ServerList.cpp, config files; user keeps their own log in `changes_done_log`.

**Why:** the user asked me to remember this because a new gserver release is coming.
New upstream baf0ba1 (2026-11-02): only getSubLevelAtPosition bounds fixed; props/warp still unchecked and enterLevel lacks the null check (crash). Ported patch: `patches/gmap-grensesjekk-baf0ba1.patch` (includes null check).

Also 2026-11-03: server-side link bounce fix (`patches/lenke-hopp.patch`, PlayerProps.cpp: skip testForTouch when |delta| > 64 px; a stale Y2 from the old level looked like a walk and re-triggered the link back). Installed into `install/gs2emu` (backup `install/gs2emu.before-linkfix`). Server now runs from `install/` (data in `install/servers/default`). New upstream tree with all fixes + user changes: `~/server-hosting/beta4-ny` branch `lokale-endringer` (not built). Known unfixed: `Level::getLink` uses `<=` (one extra row/col).

2026-11-03 assets: the extracted backups (`~/Downloads/val_backup2/x_2014_full`, `x_2015_in`, `x_2017`) are full of 0-byte files (failed extraction); the real files are inside `valbackups/valbackup.rar` and the nested 2015/2017 rars. Restored 78 TileDefs tilesets + 374 referenced pictures/ganis into `world/images`, `world/ganis` (install and bin); lists in `gjenopprettede_tilesett.txt`, still missing in `mangler_fortsatt.txt` (server folder). Test accounts need `WEAPON TileDefs` to see level tilesets.

Also 2026-11-03 evening: file watcher fix (`patches/filovervaker.patch`, FileSystem.cpp: is_regular_file + error_code variants; my moving files into a new folder inside the server dir crashed the server with file_size on a directory) - installed in `install/gs2emu` (backup `install/gs2emu.before-fswatch`), equivalent commit in beta4-ny. Fixed missing comma in serveroptions `gmaps` (crossroads.gmap, bridgeton.gmap). Broken case-twins moved to `~/server-hosting/karantene_world_files/`. Lesson: never create folders/move files inside the running server's tree; stage outside it.

2026-11-04: added a `//PORT WOLFE` block (addtiledef/addtiledef2 ...,portwolfe_,... - the same lines as the NPC in portwolfe_b2) to `install/servers/default/weapons/weaponTileDefs.txt` before `//PORT SERIAH (TEST)`, so portwolfe_alley2 and the portwolfe_ interiors always get their tiles. Backup: `/tmp/zz/weaponTileDefs.before-portwolfe.txt`. The server picked it up without a restart. Data change, not a code patch: keep it when moving to a new gserver build.

2026-11-04 guilds: `patches/guild-rangering.patch` (GuildManager ranks via `#leader`/`#officer` lines + checked `gr.guild` trigger commands), built in `build/local`, installed `install/gs2emu` (backup `install/gs2emu.before-guilds`); `globalguilds = false` in serveroptions; ListServer `verifyGuild` NO_MYSQL guard returned 0=Valid (every tag accepted) -> fixed to Invalid (`patches/listserver-guild-ugyldig.patch`, rebuilt `ListServer/bin/listserver`). Note: `NOTAT_guilds.md`. 2026-11-04 evening: `verifyAccount` now uses ListServer LocalAccounts (register on first login, PBKDF2 hashes in `ListServer/bin/passwords.txt`, reloaded when edited; patch `patches/listserver-kontoer-passord.patch`; backup `bin/listserver.before-passwords`). Test passwords must be 4+ chars now (not "x"); after tests also delete the ZzTest lines from passwords.txt.

2026-11-04: serveroptions `newtilesetlevels = ironcaps_, ironcaptunnel, poorknights_, tileset2test, val_merc-cave1.nw, val_merc-cave2.nw, echobaseint_church1.nw` (type-1 tilesets; backup `/tmp/zz/serveroptions.before-newtilesetlevels.txt`). Data change: keep it on a new gserver build.

2026-11-05: crash fix `patches/flis-koordinat-233.patch` (PropertyTileCoordinate::serialize wrote byte 233 for x=-11.5 -> writeGCharUnsafe threw -> server abort on that account's login); clamp to -40..215 half tiles and 233->234. Installed `install/gs2emu` (backup `.before-tilecoord`). Also class edits: scripts/world_ladder.txt and scripts/ladder.txt (backups in /tmp/zz). Upstream bug: re-check on new gserver.

2026-11-05: SECURITY `patches/filnedlasting-las.patch` - Player::sendFile served any existing path to clients (confirmed: config/serveroptions.txt, accounts/*.txt); now non-RC only by filename from game folders and never .nw/.graal. serveroptions clientsidelinks/clientsidesigns = true (client no longer downloads levels). Installed install/gs2emu (backup .before-filelock). Re-apply on every new gserver build.

2026-11-05 security review: `patches/brettendring-grense.patch` (client BOARDMODIFY only <=2x2 or 4x4, tile count must match; installed, backup .before-boardlimit); triggerhack_groups=false; listserver gserver port 9098 open on 0.0.0.0 without server auth (recommend firewall). Full list in NOTAT_guilds.md 'Sikkerhetsgjennomgang'.

**How to apply:** when the user builds a new gserver, check whether upstream fixed the bounds (look at the GMAPLEVELX/Y cases and warp()), re-apply the patch if not, rebuild, ask the user to restart (auto mode blocks me restarting the server), then re-test with a ZzTest account saved with MAPX 255. Related: [[custom-graal-client]].
