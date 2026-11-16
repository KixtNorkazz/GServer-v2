---
name: project_server_gs1_guild_commands
description: "beta4-ny server GS1: guild/chat commands must run server-side to be shared; engine fixes and parser limits found 15 Nov 2026"
metadata:
  node_type: memory
  type: project
  originSessionId: aceba9d7-bbbe-4924-964b-525a4a308623
  modified: 2026-11-15T19:55:08.939Z
---

Level NPCs whose guild chat commands (`playerchats && strequals(#g,X)`) sat after //#CLIENTSIDE only changed things for the speaker. On 15 Nov 2026, 47 of them were moved to the server part, in 17 levels:
- Bridgeton guards and doors, Laboo/Athedia fires, Staghorn archers, Mournhold trees, Valikorlian gates in val-new-city_c4, and the Thistletop traps.
- The traps now use a client `triggeraction x+1,y+.1,spring` with a server `setshape 1,48,16`.
- Backups and the convert.py tool are in `servers/default/backup_guildkommandoer_2026-11-15/`.
- Touch-based guild passes, hat and armor givers, and the selnic note stay client-side on purpose, because they are per-player.

**Engine fixes in beta4-ny (patches/):**
- `gs1-spiller-g-c` patch: #g and #c read the player.
- `gs1-guild-nick-grammatikk` patch, part 1: the same nick as the saved one skipped setNick, so #g stayed empty after logging in again with the same tag.
- Part 2: the grammar now accepts nested `{{`.
- Part 3: script load rewrites `elseif` to `else if` and `#P(1)` to `#P1`.

**Pitfalls:**
- A new .nw file is only found after a server restart. A level that is already loaded does not reread edits.
- gclient `set_nickname` cuts nicks at 30 characters, so a test can wrongly look like a guild rejection.
- Server `sprite =` does not reach clients.
- Server shape (setshape) is server-only and needed for triggeraction hits on non-character NPCs.

Guild files: `guilds/guild<Name_with_underscores>.txt`, with `#leader Kixt`, `Kixt` and `KixtNorkazz` (any nick). Related: [[project_v6_server_bin]], [[project_beta4_ny_upstream_trial]].
