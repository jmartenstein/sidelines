---
# side-v7j
title: Implement Compact Hover Layout
status: completed
type: task
priority: high
created_at: 2026-02-07T01:45:53Z
updated_at: 2026-02-07T02:11:04Z
parent: side-thd
---

Redesign the on_add function in mplcursors to display Down & Distance, Yardline, Score, EP/EPA, and the play description in a well-formatted, compact tooltip.

## Instructions
1. Format the hover string to be more compact.
2. Use textwrap for the play description to keep the tooltip width manageable.
3. Use clear labels for each piece of information.

## Checklist
- [x] Draft new hover text format
- [x] Update on_add callback logic in plot_scores
- [x] Implement textwrap for play description
- [x] Verify hover text is readable and correctly aligned

## Acceptance Criteria
- The hover tooltip displays all required information (Down/Dist, Yardline, Score, EP, EPA, Desc) in a structured multi-line format.
- Tooltip width is capped to prevent it from spanning more than 50% of the graph width.
