---
# side-0mn
title: Change graph colors to match teams
status: draft
type: feature
priority: normal
created_at: 2026-02-07T01:28:43Z
updated_at: 2026-02-07T01:31:24Z
---

Currently, the graphs in @src/score_over_time.py default to red and blue colors. Instead, we want the colors to match those of each team.

First, create a data structure of primary and secondary NFL team colors in the python script

Then set the graph colors to each team's primary colors. If the primary colors are too similar, set the away team's color to the secondary team color.

Finally, set the points with hover text in the net difference graph to match the team colors.
