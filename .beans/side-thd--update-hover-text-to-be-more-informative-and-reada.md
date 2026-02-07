---
# side-thd
title: Update hover text to be more informative and readable
status: completed
type: feature
priority: normal
created_at: 2026-02-07T01:31:53Z
updated_at: 2026-02-07T02:12:19Z
---

The hover text for each play needs changes to the layout, with more information.

## Instructions
1. Extract additional play-by-play metadata from the `nflreadpy` dataset.
2. Modify the `mplcursors` callback in `src/score_over_time.py` to display this data.
3. Optimize the layout for readability and information density.

## Checklist
- [x] Extract Down, Distance, and Yardline (side-9c9)
- [x] Include Overall Game Score in Hover (side-rt9)
- [x] Implement Compact Hover Layout (side-v7j)

## Acceptance Criteria
- Hovering over a play marker displays: Down, Distance, Yardline, Running Score, EP, EPA, and Play Description.
- The tooltip layout is compact and does not obscure large portions of the graph.
- All numerical values (EP/EPA) are formatted to 2 decimal places.
