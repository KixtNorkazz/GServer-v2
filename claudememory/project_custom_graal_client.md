---
name: project-custom-graal-client
description: "Goal is a custom Graal client built from reverse-engineered Graal_222/231.exe against the user's own Valikorlia Reborn gserver; where the protocol notes and test setup live"
metadata:
  node_type: memory
  type: project
  originSessionId: 387df431-8321-4e79-9763-91abb77e0d50
  modified: 2026-10-30T05:16:35.939Z
---


**Layout since 2026-11-03 (commit bd07674):** client_re code is in `engine/`, tests in `tests/` (`python3 tests/run_tests.py`), tools in `tools/` (export: `python3 tools/export_public.py ~/Downloads/graal_python_client`); top level only `start.py`/`build.py`, launchers, paths.json/settings.json/login.json. Downloads go to `worlds/<server name>/{heads,bodies,hats,swords,shields,tilesets,ganis,sounds,levels,images}` (paths.json `worlds_dir`). Android app: `app/main.py` + `app/engine/`. Older notes below that name top-level files (viewer.py, play.py ...) now mean `engine/` or `tools/`.


User is building their own customized Graal client. They run their own gserver (gs2emu, 0.0.0.0:9093) and a local listserver (client port 9111, server port 9098) for "Valikorlia Reborn Test". Test account for that server: Kixt (user supplied the password in chat; not stored here).

Protocol findings, crypto/framing, send-path addresses for 2.22 and 2.31, and the server->client dispatch table are in `client_re/README.md`; `client_re/graalproto.py` is a working codec verified by replaying captures (`client_re/replay_test.py`).

**Why:** the point of the RE work is to reproduce the client side of the protocol, not just to understand it.
**How to apply:** build on `graalproto.py` rather than re-deriving framing; treat packet-id names as unverified unless README says confirmed. The user explicitly allowed driving wine clients and working against their own server automatically; the desktop has no DISPLAY in the Claude shell, so use `Xvfb :99` for GUI clients and a rewriting listserver proxy (arrays2.dat copy pointing at it) for captures. Don't touch the original client dir's `arrays2.dat`.

**Update (client now renders):** the real server source is at `/home/Kixt/server-hosting/beta4` (gs2emu; `dependencies/fc/gs2lib-src/include/IEnums.h` has all packet ids) — read it instead of guessing. `client_re/` now has a working Python client (login, chat, links, gmap edges, PIL renderer with GANI/GFX/lights); `play.py` is the end-to-end demo. Warping/walking changes the saved position of account Kixt (accounts/Kixt.txt: LEVEL/X/Y/MAPX/MAPY) — always restore it (start was portwolfe_b3.nw, local px 96,304, cell 2,1). Never log in twice as Kixt at once (a second session kicks the first / gets no data).

`client_re/viewer.py` = interactive SDL2 window (ctypes, no tkinter/pygame installed); test it headless with `Xvfb :99` + xdotool (focus the window id from `xdotool search --onlyvisible --name ''`, it has no WM title). Don't run two sessions as Kixt at once; always restore the account to portwolfe_b3.nw px (96,304).

**Goal clarified:** the user wants the client to recreate their RP server Valikorlia. Backup: `/home/Kixt/Downloads/val_backup2/valbackups.rar` (nested rars: valbackup.rar 2014 = 52k files/levels/npcs/weapons/scripts, valbackup2015.rar, valbackup2017.rar). Extracted so far (untrusted data, own dirs): `x_2017/`, `x_2015_in/`, `x_2014_scripts/` (scripts only; levels of 2014 not extracted). Content is GS1 (2014: 4 trivial GS2 files of 1,978) — GS1 breadth matters more than a GS2 VM. GS2 tooling: `client_re/gs2dis.py`, compiler built at scratchpad `gs2build/bin/gs2test`.

**Valikorlia scripts live in** `val_backup2/x_oldval_scripts/` (from `x_2014_full/valbackup/oldval/oldval.zip`, 2013): the weapons/npcs/scripts folders in the 2014/2015/2017 backups are empty files. `join` (class include) is the biggest missing GS1 feature. GS2: now done as a source interpreter (see Step 12). Running server = beta4, generation newmain, gs2default=true (user thinks it is 'the newest'; g6 dir exists but is not running).

**Roadmap status (Valikorlia):** done: join (server-side, nothing needed), triggeraction (verified via gr.serverlist), weapon runtime commands batch 1 (set/unset/tokenize/arrays/say2/showtext/seteffect/colour/hideimg...). Next: shoot/setshootparams (PLI_SHOOT), play (audio), putnpc2/addweapon, loading Valikorlia levels (x_2014_full), NPC runtime in levels. Scripts: `gs1survey.py` measures coverage; test corpus = `val_backup2/x_oldval_scripts`.

**Levels (step 4 done):** real Valikorlia levels are only in `oldval.zip` (extracted to `val_backup2/x_oldval_levels/`); the `levels/` dirs of the 2014/15/17 backups are empty shells. `client_re/nwlevel.py` + `offline.py` (`viewer.py --offline <x.gmap|x.nw>`) load/draw/walk them without a server. User asked for levels before audio; next: play/sound, shoot, message, putnpc2, addweapon, settimer.

**Steps 5-6 done:** audio (`audio.py`, play/playlooped/stopmidi, 342/412 wavs) and live level NPC scripts (`npcrt.py`, events created/playerenters/timeout/playertouchsme/playerchats; `npcsurvey.py` 0 errors on 12.8k NPCs). Unsupported most: GS2 `function` NPCs (deferred), showpoly, putbomb, seteffectmode, wraptext2, shoot/PLI_SHOOT, putnpc2, addweapon.

**Step 7-8 done:** small visual commands (showpoly/setgifpart/seteffectmode/wraptext2) and projectiles (`projectiles.py`, PLI_SHOOT 40 / PLO_SHOOT 175, physics from gs2emu LevelShoot.h). Next candidates: putbomb, spawn, change, trail, loadmap, stopsound, GS2 (deferred).

**Step 9 done:** user `function` definitions/calls (change(), spawn() were user functions, not built-ins), onwall, movementfinished, putbomb (`bombs.py`). Remaining unsupported by count: removetiledefs, loadmap, stopsound, resetfocus, say, puthorse, attachplayertoobj.

**Step 10 done:** loadmap (offline gmap switch) and removetiledefs/prefix tiledefs from NPC scripts (`render.tileset_for` rewritten). Remaining unsupported: stopsound, resetfocus, say, puthorse, attachplayertoobj.

**Step 11 done:** stopsound, setfocus/resetfocus. Remaining unsupported: say, puthorse, attachplayertoobj, sleep2, hurt, setbackpal, showlocal.

**Step 12 done (GS2):** `gs2src.py` (source interpreter) + `gs2npc.py` (NPC host bridging to GS1 commands); `test_gs2src.py`; 437 GS2 NPCs dry-run 0 errors. Server sends source not bytecode, so no VM needed. Not done: GS2 weapons, classes/new, emitters (addlocalmodifier), key/mouse events; online GS2 unverified (live server has none).

**Step 13 done:** particle emitters (`particles.py`, GS2 `findimg(n).emitter`); units/modes inferred, see README. Next candidates: GS2 weapons, classes/new, key/mouse events, particle animation.

**Step 14 done:** GS2 weapons (`WeaponHost`, snow weapon works; `gs2weapons_survey.py` 24 weapons 0 errors). Remaining GS2: GUI system (new GuiWindowCtrl), key/mouse events, classes. Online GS2 still unverified.

**Step 15 done:** keyboard/mouse events (`inputs.py`, `test_inputs.py`, viewer SDL mouse, `--weapon FILE`). GS1 `a in |lo,hi|` added. Remaining GS2: GUI system (new GuiWindowCtrl), classes, key repeat/shift chars.

**Step 16 done:** GS2 GUI (`gui.py`, `gs2sched.py` waitfor, evg generator evaluator, `test_gui.py`). Remaining GS2: server-side introspection API (clientfunction2, makevar, findplayer...), classes, MLText markup, scrolling, key repeat/shift chars. Online GS2 still unverified.

**Step 17 done:** GS2 classes (enum, this.method, makevar()(), join on GUI controls, TStaticVar, script objects by weapon name) and GUI scrolling (scrollbar, wheel). GS2 weapons run onCreated/onPlayerEnters. Remaining: server introspection API, MLText markup, horizontal scroll, online GS2 unverified.

**Step 18 done:** server introspection API as a local NPC server (`npcserver.py`, `weaponlib.py`, `test_npcserver.py`): server parts of GS2 weapons run offline, loopback triggers, type()/getvarnames/makevar, sandboxed files in `server_files/`. Remaining: other players, level NPC server parts, loadvars/savevars, persistence, online use.

**Step 19 done:** other players + NPC database in the local NPC server (shared `NpcServer`, `RemoteSrv`, `NpcSrv`, `LevelSrv`, real PMs, static `this`/dynamic with-player). Live check `simulate_two.py`: accounts Kixt and KixtNorkazz (password given by the user via GRAAL_PASSWORD, never stored) may be online together; both saved positions must stay unchanged (the script compares account files and restores).

**Step 20 done:** server moves other players (`Session.teleport`, PlayerSrv setters x/y local, gmapx/gmapy, level, setlevel2, chat, ani); live-verified with simulate_two.py, positions restored and account files unchanged. Remote-only players cannot be moved.

**Step 21 done:** smooth server-commanded walking (A* `pathing.py`, `Session.walk_to`, `walkTo` + WalkDone) and checked teleports (`setPos`); `Session.poll()` now ticks everything. Live-verified with simulate_two.py; it restores saved account fields (ANI may change swim->idle).

**Step 22 done:** walking avoids other players (soft-cost A*, replan, wait), `avoidPlayers` switch; live-verified with simulate_two.py (Kixt placed on the route, closest approach 24 px).

**Step 23 done:** prediction of other players' movement (position history, median velocity, tcost A*). Live run shows no overlap but no measurable advantage over current-position avoidance (timing); offline test shows the difference. simulate_two.py restores saved account fields (ANI may change).

**Step 24 done:** turn prediction (heading-based estimate, wall-slide hypotheses, peer routes, union with static zone). Lesson: arrival-time velocity under network jitter was worse than static avoidance; heading-only fixed it (jitter test in test_walk.py).

**Step 25 done:** NPC prediction (script tweens + PLO_MOVE queues, `npc_motion`, `_npc_tcost`, moving shapes planned around / waited for, NPC runtime on Session.clock). Live server NPCs are static, so PLO_MOVE untested live; test_npcmotion.py covers it.

**Step 26 done:** PLO_MOVE2 parsing and NPC look-ahead (`NpcRuntime.lookahead` shadow-session simulation of timeouts/moves). Corpus NPCs are player-triggered, so accuracy is shown by test_npcmotion.py only. Limitations: running sleeps, touch-triggered movers, GS2 NPCs.

**Step 27 done:** look-ahead for GS2 NPCs (interpreter clone) and touch-triggered openers (`opens_on_touch`, doors planned through, walker waits). Fixed: step-26 bug where any NPC mentioning `move` was passable; shadow session now isolated (own collision + npcrt, deep-copied GS2 vars).

**Step 28 done:** chat-command and flag doors (`door_way`/`flag_setter`/`doors`, mission prelude, `say_line`, door pricing, `door_commands`). Fixed a long-standing GS1 bug: string literals in conditions were mangled (strequals(#c,...) never matched). Session.chat is the chat log LIST: never name a method `chat`.

**Step 29 done:** item/key/grab doors (`door_way` modifiers, pickups, key holds), GS1 player stats (playerrupees...), engine push mechanic (`canbepushed`, `Session._push`, planner price 60). Touch event now re-fires when keys/flags/inventory change while touching.

**Step 29 perf:** shadow simulations have a command budget (weapons.yield_command raises), door answers cached 30 s by (flags, inventory, keys) signature, doors() limited to the walk's focus box.

**Step 30 done:** weapons / items not on the ground (shops, chests, server inventory) and several kinds at once: GS1 stat assignment + `hasweapon`/`addweapon`/`removeweapon`, server part of level NPCs now kept and run on player events (Valikorlia shops are server-side grab shops), `NpcRuntime.sources`, `Session.acquire_plan` + mission step `get`, `CHEST` parsing / PLO_LEVELCHEST / PLI_OPENCHEST. No live chest test (would change the account's inventory/savedChests: back up and restore the account file first).

**Step 31 done:** NPC hit events: sword (`attack()` -> `washit` via `hit_npcs`/`sword_rect`), bombs (`wasexploded` in `Bombs.tick` via `blast_hits`), planner ways `hit` and `bomb`. Not done: `wasshot` (arrows), `wasthrown`/carrying (658 corpus mentions), pulling.

**Step 32 done:** arrow hits (`wasshot` in `Projectiles._hit`, planner way `shot`). Next candidate: carrying/throwing NPCs (`canbecarried`, `wasthrown`).

**Step 33 done:** carrying/throwing NPCs (`lift`/`throw`/`_carry_tick`, `wasthrown`, glove items, planner way `carry`). Test lesson: a test obstacle must be tall enough that the A* cannot go around it (use a 2000 px shape starting at ay-60).

**Step 34 done:** server notifications for sword hits (PLI_HITOBJECTS 36), pushed NPCs (PLI_NPCPROPS 3 X2/Y2), carry/throw (CARRYNPCID prop 24 not on gmaps, PLI_THROWCARRIED 11). Offline-tested only.

**Step 35 done:** followplayer, attachplayertoobj, enable/disableweapons, NPC `say` (stored only). Remaining unsupported by count: truncated `drawoverplaye`, a few attachplayertoobj, join.

**Step 36 done:** fixed attachplayertoobj semantics (moves with the NPC, not blocked by it; rope-bridge scripts), `playerattached`, `detachplayer`, playerx/playery/playerdir assignment, `=<`/`=>` operators.

**Step 37 done:** normal NPCs y-sorted against the player (bottom edge), NPC `say` bubbles drawn; drawunder/overplayer were already right.

**Step 38 done:** one back-to-front depth sort for NPC images, #c# characters, other players and us (render.py).

**Step 39 done:** GS2 bridge for attach/detach/followplayer/say/canbecarried/enable/disableweapons. Leftover unsupported is data typos, missing class files (housedoors etc. are NOT in the backup), puthorse, hurt, showstats.

**Step 40 done:** canpush-canpull class works (actionpushed/actionpulled events from walking into / pulling with A held, imgwidth/imgheight/#f). Server scripts dir has no new classes (housedoors etc. missing from everything).

**Step 41 done:** hurt/setplayerdir/showstats/showlocal/noplayerkilling/puthorse accepted (state only). Command coverage of the corpus is now essentially complete; remaining work is fidelity (horses, HUD, death) and live verification.

**Step 42 done:** HUD (hearts + counters, render.draw_hud), horses drawn. Live simulate_two.py re-run after steps 30-41: RESULT ok. Next candidates: death at 0 hearts, riding, live checks of chests/hits on the server.

**Step 43 done:** death at 0 hearts (`death_tick`, `playerdies`), offline respawn at the session start.

**Step 44 (live chest check) done:** PLO_LEVELCHEST parsing and PLI_OPENCHEST verified on the real server (Kixt, onlinestartlocal.nw chest 20,24: GRALATS 5->6, chest opened). Account file backed up/restored (only APCOUNTER/ONSECS differ). Procedure for live tests that change inventory: copy accounts/Kixt.txt first, restore after logout. Horse sprite sheets are 96x576 with irregular frames: riding render layout unknown.

**Steps 45-47 done (autonomous run, notes in client_re/NOTES.md):** horse mount/dismount (no rider drawing), planner pushes class crates, persistent offline state (--state), walk_survey.py. User asked to keep taking steps automatically and leave notes: log in NOTES.md.

**Step 48 done (user asked):** NPC state persistence in the offline --state file (baseline diff, script-hash guard, GS1 this + GS2 bag).

**Step 49 done:** item loss on death modelled after gs2emu dropItemsOnDeath (offline).

**Steps 50-51 done (autonomous):** run_tests.py + ARCHITECTURE.md; online death via STATUS DEAD bit + hearts sent to the server (gs2emu drives deaths/drops/revival from the client's STATUS prop). Notes in client_re/NOTES.md.

**Step 52 done:** set/unset flags sent to the server (PLI_FLAGSET/FLAGDEL, live-verified), incoming flags handled. Unsent PLI packets list in README step 52.

**Step 53 done:** horses sent; incoming NPCDEL/NPCDEL2/HURTPLAYER/BOMBADD/BOMBDEL/EXPLOSION/HORSEADD/HORSEDEL handled (audit of unhandled PLO ids continues: PUSHAWAY, HITOBJECTS, ARROWADD, THROWCARRIED, FREEZEPLAYER2...).

**Step 55 (perf):** live simulate_two crossing check is a performance alarm: it failed (8 px) after many per-tick features; fixed with caches (read_gmap, collision buckets, door cost bbox, npc_motion). Always run `run_tests.py --live` after planner/collision/tick changes. Never `pkill -f simulate_two` from the shell tool (kills its own command).

**Step 56 done:** remote arrows, start message; packet audit complete.

**Step 57 done:** approximate rider drawing (horse sheet = 9 rows x 64 px; frame table guessed).

- Step 58: timers and tweens persist in save_state (timeout_in / tween). client_re is now a git repo (.gitignore keeps passwords out; commit with the Co-Authored-By line).

- Step 59: classes/housedoors.txt + classes/lamp_post.txt reconstructed from the user's description (housedoors: overlay hides when player near; lamp_post: light when player near). Server-part `join` now expands too. Bug to fix: `x-2` without spaces parsed as a word.

- Step 60: `x-2` (no spaces) now arithmetic in weapons.evaluate (was ~59k text words in the backup); showimg index/image bug in npcrt fixed.

- Step 61: GS1 arrays (setarray this.x, a[i] read/write, arraylen) and `^` power; evalfail_survey.py lists expressions that still fail (silently 0).

- Step 62: list literals `a = {..}`, `x in list`, hex, tiles[x,y] in GS1 evaluate.

- Step 63: unset arrays read 0 (_Zero), multi-line conditions, `; or` typo in GS1 evaluate.

- Step 64: keydown2/keycode/keypressed (Input.vk_down). Open: evalfail_survey `alpha==.6; or` line not reproduced.

- Step 65: stray `;` before ||/&& dropped (level typo). Live simulate_two ok after step 64.

- Step 66: strcontains, onwater in GS1 evaluate; remaining evalfail entries are data typos / zero divisions.

- Step 67: classes lamppost/lantern/nightlamp reconstructed; timevar + strreplace in evaluate. Still missing: taghelper, bomymooncontrols, baddy_test, empyria_housing.

- Step 68: empyria_housing original (found in Downloads/home/Kixt/val_update/.../Empyria/Files/Text/Script/Classes) in classes/ with //#SERVERCLASS; its door/key/sign in reference/empyria_housing/. That val_update tree is a second backup: look there for other missing classes. Remaining missing: taghelper, bomymooncontrols, baddy_test.

- Step 69: real class is scripts/lamp-post.txt (always lit); class_text now ignores _/-/space; my lamp_post guesses deleted. Guesses remain: housedoors, lantern, nightlamp.

- Step 70: live death verified (Kixt, account restored bytewise: files are CRLF!). Fixed Session.local_inventory default. Next live checks need a test NPC: ask the user first.

- Step 71: live NPC checks done with a scratch level (user allowed test NPCs anywhere; backups exist). HITOBJECTS and carry/throw OK; PLI_NPCPROPS ignored by the server. Fixed: bare GS1 scripts now run `created`. All scratch files removed, accounts restored.

- Step 72: paths.json + config.py replace hard-coded folders; window.load_sdl for Windows/macOS; start.bat; requirements.txt (Pillow only). Windows untested.

- Step 73: login GUI (login_gui.py, logos-1.jpg; viewer.py without --account opens it; start.sh/start.bat). Session.set_nickname sends prop 0. Test server accepts ANY password. xdotool tests: run viewer and xdotool in ONE bash call (background jobs die at call end).

- Step 74: Windows tested via Windows Python 3.12 embeddable + Pillow wheel + SDL2.dll under wine (scratchpad win/). Tests ALL OK, login GUI and live login OK. Never `pkill -f wine` (kills the tool shell); use `wineserver -k`.

- Step 75: online pushes via PLI_TRIGGERACTION pushed,<dir> (found by REA: FUN_0053085c/FUN_0053e7a8); verified live, both clients see the move. Server caches levels: new file name for each scratch level.

## Step 76 (2026-10-31): files from the server
User tried the client on Windows without server files: black screen/crash. Cause: everything was looked up locally; `render.read_gmap` raised TypeError when the gmap file was missing. Now `filefetch.py` fetches files on demand (WANTFILE/UPDATEFILE, cache/<host>_<port>/), `builtin/` holds pics1.png + sprites.png (server lacks them). Test with `GRAAL_PATHS` pointing to a json with `asset_dirs: []` and an empty cache_dir. Still unconfirmed on a real Windows machine (crash text never seen).

## Steps 85+ (public repo phase)
- Repo cleaned for public release: branch `public` (git author graal_reborn), old history in `main` + copy in `../private_notes/`; paths.json is gitignored (local, has the user's paths); comments stripped from .py; README rewritten. Default list server 91.99.73.49:9111 (user's Graal Reborn server, also in arrays2.dat of the original client). Login screen shows a server list (minclient.list_servers_full / parse_server_entry).
- Player list F7 + PMs: `playerlist.py`, `Session.online`, `send_pm(ids, text)`, `pm_log`; gs2emu sends all online players as OTHERPLPROPS (DISCONNECT prop 51 = left the server); PM limit 1 per 4 s; verified live with ZzTestA/B (deleted).
- Never `pkill -f` (kills own shell); don't kill processes without asking.
- Level editor (user request, REA of Graal_222.exe "Training"/editor: entry FUN_0051416c at 0x51416c, "cannot open the editor in online mode" at 0x504108; UI feature list taken from languages/languageEnglish.txt MainWindow-/EditLink-/EditSigns-/EditChest-/EditBaddy- keys): `editor.py` (UI), `editor_forms.py` (Form/Chooser), `leveldoc.py` (model, .nw writer, undo, fill, clipboard), tests test_leveldoc/test_editor. Verified: 150 real levels round trip; Play launches viewer --offline with GRAAL_PATHS temp json. Not done: layers >0 editing, zoom, predefined NPC/object palette, editor control NPCs, gmap/map making (M), flags editor.
- Build = the editor (user wants it named Build, not Training): build.sh/build.bat, editor.py, login-screen "Build" button; layers 0-7, zoom, object/NPC library in build_data/ (gitignored), text cursor in forms. Windows check = Windows Python 3.12 embeddable under Wine in scratchpad win/ (needs `sys.path.insert(0, HERE)` in every entry script/test because embeddable python ignores the script dir; xdotool needs windowraise+windowfocus and keydown/keyup under Wine).
- M map: worldmap.py. gs2emu sends a gmap player with LEVEL = the gmap name (not the level file), GMAPLEVELX/Y = cell, X2/Y2 = pixel position in the level; account file keeps MAPX/MAPY. Far players' positions are only what the server last sent. Live test accounts ZzTestA/B deleted.
- Appearance window (F): appearance.py; lists come from heads.txt/bodies.txt in the server world folder (made by server/make_appearance_lists.py, already run once on the user's server: 11149 heads, 3957 bodies; rerun when heads/bodies are added); Done sends props 11 (len+100) and 35. Server `*.txt` files are fetchable by clients (foldersconfig `file *.txt`).
- Public repo workflow: work stays in client_re (branch `public`); `python3 export_public.py ~/Downloads/graal_python_client` copies committed files into the user's own repo there (has .git, remote on their GitHub, their own LICENSE kept; pics1.png/sprites.png/logos are left out on purpose); the user runs git add/commit/push themselves. gs2emu: server NPC script reply path = Control-NPC `actionserver<x>` + `sendpm` (used by the map).

- 2026-11-02: user runs the exported copy on real Windows (OneDrive folder), with no server world locally. Test "like Windows" with GRAAL_PATHS pointing at a paths.json with empty asset_dirs and a scratch cache_dir. Bugs only seen there: NPCs on non-gmap levels were skipped by render (no GMAPLEVELX from gs2emu), float mouse coords from scaled windows used as indexes. gs2emu (NPC-server) never sends level links/signs; client fetches the .nw for them (verified live).

- 2026-11-02: separate Android project at ~/Downloads/graal_android (user wants it kept separate from client_re; app/ = scrubbed snapshot + main.py, mobile_ui.py, android window.py, bz2_ctypes.py; NOTATER.md in Norwegian). Build: ./build_apk.sh (kivy/buildozer Docker, p4a python 3.14, sdl2 bootstrap). p4a gotchas: no `bz2` module (use libbz2 via ctypes), `import ctypes.util` crashes (needs p4a 'android' module), same version number = new files not extracted on reinstall. Emulator: ~/Android/Sdk, AVD graaltest (API 24 x86_64), no KVM on this PC -> `-accel off`, ~10 fps. A position jump back to the login spot after ~1 min (or on chat) was a client bug: every own PLAYERPROPS packet reset pos from stale me X2/Y2; fixed in _own_pos(props), regression test in test_hardening. The app remembers the account in login.json, so test scripts must clear the field before typing (else gs2emu auto-creates a new account like ZzTestDZzTestD).

**Update 11 Nov 2026:** `client_rev6` now speaks v6 (G3D0311C): gs2bc/gs2vm/gs2probe and the v6 parts were ported from `graal_android/app/engine`; a server that refuses 2.22 ("client version is not allowed", the v7 server allows only 5.12-6.037) is retried as v6 by itself. Changes are uncommitted in `client_rev6` (branch v6). Capture of the original client and what is still missing: `client_rev6/NOTAT_v6_pakkefangst_2026-11-11.md`; see [[reference_v6_client_on_linux]].
