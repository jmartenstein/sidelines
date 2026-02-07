---
# side-x5m
title: Assign Dynamic Colors in plot_scores
status: todo
type: task
priority: high
created_at: 2026-02-07T01:45:06Z
updated_at: 2026-02-07T01:54:04Z
parent: side-0mn
---

Update the `plot_scores` function in `src/score_over_time.py` to fetch colors for the home and visitor teams using the mapping created in the previous task.

## Instructions
1. Integrate the color mapping logic into `src/score_over_time.py`.
2. In `plot_scores`, use `home_team_name` and `visitor_team_name` to look up their respective colors from the mapping.
3. Handle cases where a team might not be found in the mapping (provide default colors like blue/red).
4. Store these colors in variables for use in plotting.

## Checklist
- [ ] Import/Define color mapping logic in `src/score_over_time.py`
- [ ] Look up colors for home and visitor teams in `plot_scores`
- [ ] Implement default color fallback
- [ ] Verify colors are correctly assigned to variables

## Acceptance Criteria
- `plot_scores` dynamically identifies the primary and secondary colors for the specific teams involved in the game being plotted.
- Missing team data does not cause the script to crash (falls back to defaults).
