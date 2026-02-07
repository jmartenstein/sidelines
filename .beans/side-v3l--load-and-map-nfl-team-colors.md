---
# side-v3l
title: Load and Map NFL Team Colors
status: todo
type: task
priority: high
created_at: 2026-02-07T01:45:01Z
updated_at: 2026-02-07T01:53:56Z
parent: side-0mn
---

Use `nflreadpy.load_teams()` to fetch official team colors and create a mapping (dictionary) from team abbreviations to their primary and secondary hex colors.

## Instructions
1. Call `nflreadpy.load_teams()` to get the team metadata.
2. Iterate through the resulting Polars DataFrame and extract `team_abbr`, `team_color`, and `team_color2`.
3. Build a dictionary where keys are team abbreviations and values are another dictionary containing `primary` and `secondary` hex codes.
4. Cache this mapping to avoid repeated API calls.

## Checklist
- [ ] Call `nflreadpy.load_teams()`
- [ ] Extract `team_abbr`, `team_color`, and `team_color2`
- [ ] Build the color mapping dictionary
- [ ] Verify the mapping contains all 32 NFL teams

## Acceptance Criteria
- A function or utility exists that returns a dictionary mapping team abbreviations (e.g., "KC", "PHI") to their official hex colors.
- Both primary and secondary colors are captured for each team.
