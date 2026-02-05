---
# side-nk4
title: Update nflreadpy API usage in play_by_play.py
status: completed
type: task
priority: high
created_at: 2026-02-05T16:51:02Z
updated_at: 2026-02-05T17:34:14Z
parent: side-yba
---

The script currently attempts to use a non-existent read_game function. This needs to be replaced with nflreadpy.load_pbp.

## Checklist
- [x] Remove MockGameData and simulated read_game logic.
- [x] Import nflreadpy correctly.
- [x] Update get_play_by_play to call nflreadpy.load_pbp.
