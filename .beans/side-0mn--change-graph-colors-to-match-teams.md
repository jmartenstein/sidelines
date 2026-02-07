---
# side-0mn
title: Change graph colors to match teams
status: completed
type: feature
priority: normal
created_at: 2026-02-07T01:28:43Z
updated_at: 2026-02-07T02:16:09Z
---

Currently, the graphs in @src/score_over_time.py default to red and blue colors. Instead, we want the colors to match those of each team.

## Instructions
1. Implement a robust color mapping system using official NFL data.
2. Integrate these colors into the plotting logic in `src/score_over_time.py`.
3. Ensure visual clarity by handling team color collisions (similar primary colors).

## Checklist
- [ ] Load and Map NFL Team Colors (side-v3l)
- [ ] Assign Dynamic Colors in plot_scores (side-x5m)
- [ ] Implement Color Collision Logic (side-z67)
- [ ] Update Graph Elements with Team Colors (side-3df)
- [ ] Update Scatter Plot Colors (side-bhb)

## Acceptance Criteria
- All graph elements (actual scores, expected scores, lead fills, and play markers) use the official primary colors of the respective teams.
- In cases where two teams have similar primary colors, the visitor team uses its secondary color to maintain contrast.
- The legend accurately reflects the team-specific colors.
