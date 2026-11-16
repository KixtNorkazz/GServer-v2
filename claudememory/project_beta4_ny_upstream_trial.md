---
name: project-beta4-ny-upstream-trial
description: beta4-ny = fresh upstream GServer-v2 (25396a18) + beta4's changes on branch fra-beta4; builds, runs; needs default_scriptengine_client = gs2
metadata:
  type: project
---

beta4-ny (git branch `fra-beta4`, commits 14b39525 + a6e248cc) is upstream GServer-v2 25396a18 with beta4's source changes applied (2026-11-10). It BUILDS and runs with beta4's data (world/gs2cache/accounts copied with rsync --ignore-existing, config merged without removing keys; backups `*.before-fyll`).

**Why:** user wants to see whether moving to newer upstream is viable.

**How to apply / pitfalls:**
- Upstream split the engine setting: ny needs `default_scriptengine_client = gs2` in serveroptions.txt (else the GS2 compiler is never used: 0 NPC bytecode, all 7577 gs2cache translations "refused" by gs2cache/CHECK).
- Configure fails on libtommath (develop moved): use `-DFETCHCONTENT_SOURCE_DIR_LIBTOMMATH=beta4/build/local/dependencies/fc/libtommath-src`, plus `-DCMAKE_PREFIX_PATH=beta4/vcpkg_installed/x64-linux`.
- Upstream renamed findInRangeNPCsByDistance -> findNPCsInRangeByDistance.
- ny sends NPCs only from adjacent gmap cells (+-1); beta4 also sent cells at distance 2 (109 NPCs fewer on ganelon_a-1). Probably intended upstream change.
- In Weapon.cpp/File.cpp upstream's own version was kept (beta4's fixes dropped); weapons still reach the app client (15 with bytecode), real GLauncher not tested.
- Tested with real GLauncher 2026-11-12: login, 15 weapons, walking, chat, warp all work; start area pixel-identical to beta4.
- For side-by-side runs ny is set to `serverport = 9096`, `serverip = 192.168.1.31` (LAN), `upnp = false`, name "Valikorlia ny-oppstroms (prove)" (backup `serveroptions.txt.before-prove9096`). The public 91.99.73.49 only forwards 9093/9098, so a GLauncher gets "Couldn't connect" on any other port unless serverip is the LAN address.
- Real regression from the +-1 NPC range: gmap-wide tile prefixes (e.g. `portwolfe_`) are defined only by NPCs in a few levels (a1, b1, b2, d2); a client with an empty `levels/tiledefs/tiledefs<server>.txt` that logs in 2+ cells away (portwolfe_c4) gets wrong tiles in the neighbouring levels. beta4 hides it with its +-2 range (still broken 3+ cells away). `#L` scripts become `level.name` = the PLAYER's level. The -TileDefs weapons do not cover `portwolfe_`; adding gmap prefixes there would fix both servers. Screenshots: beta4-ny/prove_2026-11-12/.
- ScriptSystem.cpp: `//#` engine name is lowercased again (uncommitted on fra-beta4, 2026-11-12).
- Build dir in use: `build/v6` (`ninja -C build/v6` writes bin/gs2emu). Related [[project-v6-server-bin]], [[server-gmap-bounds-patch]], [[reference_v6_client_on_linux]].
