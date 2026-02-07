---
# side-3df
title: Update Graph Elements with Team Colors
status: completed
type: task
priority: high
created_at: 2026-02-07T01:45:17Z
updated_at: 2026-02-07T02:13:58Z
parent: side-0mn
---

Update fill_between, step, and plot calls in both subplots to use the assigned team colors instead of hardcoded 'red' and 'blue'.

## Instructions
1. Replace pos_color and neg_color assignments with the dynamic team colors.
2. Update ax1.fill_between calls to use the team-specific lead colors.
3. Update ax2.step and ax2.plot calls for Home/Visitor actual and expected scores to use their respective team colors.
4. Ensure the legend labels still correctly identify which color belongs to which team.

## Checklist
- [x] Update ax1 fill colors (Net Difference)
- [x] Update ax2 line and step colors (Scores)
- [x] Ensure consistent color usage across both subplots
- [x] Verify legend accuracy

## Acceptance Criteria
- The 'Net Difference' subplot (ax1) fills use the leading team's color.
- The 'Scores' subplot (ax2) lines and steps use the home and visitor colors consistently.
