---
name: project-v6-animated-weapons
description: How custom-gani weapons (GreenDragon3, Claymore) must be written for the v6 client; template in beta4/templates
metadata:
  type: project
---

Template + tools: ~/server-hosting/beta4/templates (weaponTemplate.txt, new_weapon.py, make_frame_ganis.py, README.md). Working examples: weaponGreenDragon3.txt (user: "100%") and weaponClaymore.txt (untested at time of writing).

Facts proven from game_console.log:
- Engine sets ani "walk" on EVERY 0.05 s tick while moving; setani restarts a gani -> looping walk gani stays on frame 1. Fix: set one single-frame gani (`<name>-f0..fN`, cut with make_frame_ganis.py) per tick.
- Standing still the engine leaves the gani alone; `player.ani` works in GS2 and can be compared.
- GS1 `playershootssword` is dropped by the translator; use onKeyPressed(code,key). Weapon key and attack key can be the same press: remember the key, decide in the next tick (onWeaponFired cancels it).
- Weapons: GS2 functions onWeaponFired/onKeyPressed/onTimeOut + setTimer(0.05); avoid temp.* and sleep.

**Why:** the user builds many ganis weapons themselves and wants a template to add more. **How to apply:** start from the template, don't re-derive; see [[project-v6-server-bin]].
