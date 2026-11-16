---
name: reference_v6_client_on_linux
description: How to run the original Graal v6 client (GLauncher/OG_Graal.exe) on this Linux box and log its packets inside gs2emu
metadata:
  type: reference
---

The original v6 client (`~/server-hosting/6.0.3.7/GLauncher.exe`) crashes under the system Wine 11 (new WoW64 mode; the packer's anti-debug tricks fail), but **runs in real 32-bit Wine 8**: docker image `graal-wine32` (i386/debian:bookworm + wine32, built 11 Nov 2026, 1.4 GB, kept) with `--network host`, an `Xvfb :99` on the host, driven with `xdotool`, screenshots with `import -window root`. Exact commands: `client_rev6/NOTAT_v6_pakkefangst_2026-11-11.md` section 1. This replaces the older note in [[project_login_server_prototype]] that v6 cannot run here.

Traps: the client rewrites the key bindings in `game_config.txt` under Wine (arrow keys end up rotated) and replaces `game_console.log`: copy both first, restore the config after. Without a window manager, click the game view before sending keys; an open F1 menu takes the keyboard.

Packet logging without touching the server: start gs2emu under gdb (REA `start_gdb_session`) and `source client_rev6/tools/gdb_pktlog.py`; read with `tools/pktlog_show.py`. The login packet is not logged (no passwords). Stop the server with `kill -TERM <pid>` (SIGTERM set to pass), then close the gdb session.

Guest login from a script is not possible without the guest password the client sends; use a throwaway `ZzTest…` account (a new name registers itself at the ListServer with the password typed), see [[server_saves_account_on_logout]].

Later the same day: Wine 10 in real 32-bit works too, so the cause is the `wow64` USE flag, not the Wine version. Gentoo fix (not run, needs root): `/etc/portage/package.use/wine-vanilla` -> `-wow64 abi_x86_32`, `ABI_X86="64 32"`; `emerge -pv` shows only wine-vanilla rebuilds (make.conf already has ABI_X86="64 32"). Arrow keys: delete the `keyset_` lines from `game_config.txt` (Norwegian Windows key names get misread). Step-by-step guide for the user: https://claude.ai/artifact/6uaLNChNnC6imLRzNfAmxB
