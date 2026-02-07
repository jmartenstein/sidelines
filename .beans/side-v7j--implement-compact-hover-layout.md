---
# side-v7j
title: Implement Compact Hover Layout
status: todo
type: task
priority: high
created_at: 2026-02-07T01:45:53Z
updated_at: 2026-02-07T01:55:04Z
parent: side-thd
---

Redesign the on_add function in mplcursors to display Down & Distance, Yardline, Score, EP/EPA, and the play description in a well-formatted, compact tooltip.

## Instructions
1. Format the hover string to be more compact.
2. Use textwrap for the play description to keep the tooltip width manageable.
3. Use clear labels for each piece of information.

## Checklist
- [ ] Draft new hover text format
- [ ] Update on_add callback logic in plot_scores
- [ ] Implement textwrap for play description
- [ ] Verify hover text is readable and correctly aligned

## Acceptance Criteria
- The hover tooltip displays all required information (Down/Dist, Yardline, Score, EP, EPA, Desc) in a structured multi-line format.
- Tooltip width is capped to prevent it from spanning more than 50% of the graph width.
