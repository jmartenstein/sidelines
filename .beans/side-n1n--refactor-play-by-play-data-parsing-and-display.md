---
# side-n1n
title: Refactor play-by-play data parsing and display
status: completed
type: task
priority: normal
created_at: 2026-02-05T16:51:16Z
updated_at: 2026-02-05T17:34:03Z
parent: side-yba
---

The current display logic assumes play objects with .quarter, .time_remaining, and .text attributes. nflreadpy returns a DataFrame with columns like qtr, time, and desc.

## Checklist
- [ ] Update display_play_by_play to iterate over DataFrame rows.
- [ ] Map qtr to quarter display.
- [ ] Map time (or game_seconds_remaining) to time display.
- [ ] Map desc to the play text display.