---
name: project-mobile-v6-client
description: graal_android app (now 4.10) speaks v6 (G3D0311C) to the modern gs2emu via its own GS2 bytecode VM; where things live and how it was tested
metadata:
  type: project
---

~/Downloads/graal_android (buildozer/Kivy-less SDL2 app, Python) now logs in to the v6 server (port 9093) as `version: "v6"` with `game_server` in app/android_config.json. Server src was untouched at first; since 4.x the user approved ONE server patch (see below).

- Bytecode: app/engine/gs2bc.py (parser/disassembler), gs2vm.py (BCInterp, drop-in for gs2src.Interp), gs2probe.py (tiledef lines from compiled scripts). Format from gs2parser (build/local/dependencies/fc/gs2parser-src: opcodes.h, GS2CompilerVisitor.cpp).
- Protocol: PLO_NPCBYTECODE(131 raw), PLO_NPCWEAPONADD(33)+PLO_LOADSCRIPT(197 line) -> PLI_UPDATESCRIPT(158) -> PLO_NPCWEAPONSCRIPT(140 raw), classes via PLI_UPDATECLASS(161) -> PLO_LOADSCRIPT raw; missing class = PLO_NPCWEAPONSCRIPT line. No id39 for v6.
- Tests in graal_android/tests (vmtest/crosscheck/bulkrun/livev6/ladder_v6/gui_v6/class_v6/weapon_v6); compiler CLI `gs2c` built from libgs2compiler.a (tools/BUILD_GS2C.md).
- Compiled quirks the VM reproduces on purpose: `<`/`>` convert strings to numbers (strings compare as 0); `!(a && b)` in an if-condition is compiled wrongly by gs2parser; one-line loop bodies leave call results on the stack.
- Test account ZzTestV6 must be deleted from servers/default/accounts and ListServer/bin/passwords.txt after tests (never use Kixt).

**Why:** user asked for a mobile version compatible with the v6 server (option B: bytecode VM). **How to apply:** extend gs2vm/gs2npc for new commands; see [[project-v6-server-bin]] and [[project-v6-animated-weapons]].

Later findings (Nov 2026, app 4.1-4.10; details in graal_android/NOTATER.md):
- Server data trap: scripts whose first line is `//#SERVERSIDE` (or a misspelled `//#CLIENTSIDE`) got NO server script because ScriptSystem::getCompiledServerScript read it as an engine name. Patch `graal_reborn/client_rev6/tools/server_patch_unknown_script_marker.patch` is installed in beta4 (backup of the old tree: server-hosting/backup/val-14-4). A copy `beta4-test` was used for testing.
- gs1_to_gs2.py (gs2cache) now closes unterminated `{` blocks (apply_brace_fix.sh); `.none`/`.bad` files in gs2cache mean an NPC has no client script on ALL clients.
- Server sends NPC prop BLOCKFLAGS (1 = server ran dontblock) and CLASS (classes joined server-side); NPCs block by default with their image size. Tile type 3 = chair (sit gani).
- Image-size/touch zones must not cache a fallback while the file is still downloading (phone starts with an empty cache): test with TEST_WORLDS=<empty dir> in tests/walk_v6.py.
- Tileset image valtiles_capital-int2.gif on the server was an incomplete copy; fuller one copied from val_backup (backup kept as .before-fullcopy).
- User compares against the original client (GLauncher.exe) and says what is fine there; mine_rock class has no client bytecode on the server (unexplained how the original shows it).

