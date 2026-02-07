---
# side-bhb
title: Update Scatter Plot Colors
status: todo
type: task
priority: normal
created_at: 2026-02-07T01:45:22Z
updated_at: 2026-02-07T01:54:40Z
parent: side-0mn
---

Set the points in the net difference graph to match the team colors, possibly based on which team is currently leading or which team the play favors.

## Instructions
1. In ax1.scatter, instead of a single color, use a list of colors based on the possessionTeam or the leading team.
2. If the play results in a positive expected change for the home team, use the home team color; otherwise, use the visitor team color.

## Checklist
- [ ] Determine color logic for scatter points
- [ ] Update ax1.scatter to use dynamic colors
- [ ] Verify scatter points are distinguishable from the background fills

## Acceptance Criteria
- Play markers (scatters) on the net difference graph reflect the team associated with the play or the current lead status.
- Markers are clearly visible over the background lead fills.
