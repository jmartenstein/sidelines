---
# side-9c9
title: Extract Down, Distance, and Yardline
status: completed
type: task
priority: high
created_at: 2026-02-07T01:45:38Z
updated_at: 2026-02-07T02:07:10Z
parent: side-thd
---

Ensure 'down', 'ydstogo', and 'yrdln' fields are included in the play-by-play data fetched from nflreadpy.

## Instructions
1. Inspect the columns returned by nflreadpy.load_pbp().
2. Map the relevant fields: down, ydstogo (yards to go), and yrdln (yardline string).
3. Ensure these columns are preserved during any filtering or transformation steps in get_sorted_plays.

## Checklist
- [x] Verify down, ydstogo, and yrdln availability in nflreadpy data
- [x] Update data extraction logic to include these fields
- [x] Verify fields are present in the final DataFrame used for plotting

## Acceptance Criteria
- The internal DataFrame used by the plotting function contains valid data for 'down', 'ydstogo', and 'yrdln' for at least 95% of standard plays.
