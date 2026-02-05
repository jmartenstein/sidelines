---
# side-fij
title: Implement game ID resolution logic
status: todo
type: task
priority: high
created_at: 2026-02-05T16:51:11Z
updated_at: 2026-02-05T16:51:11Z
parent: side-yba
---

nflreadpy.load_pbp requires a 10-digit numeric game ID. The script currently expects a string like 2023_01_DET_KC. We need to implement lookup logic using nflreadpy.load_schedules.

## Checklist
- [ ] Add logic to parse YYYY_WEEK_HOME_AWAY format.
- [ ] Fetch schedules for the target season.
- [ ] Filter schedules to find the 10-digit game_id.
- [ ] Handle cases where the game cannot be found.