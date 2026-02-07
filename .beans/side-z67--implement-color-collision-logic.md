---
# side-z67
title: Implement Color Collision Logic
status: todo
type: task
priority: normal
created_at: 2026-02-07T01:45:12Z
updated_at: 2026-02-07T01:54:24Z
parent: side-0mn
---

Add logic to detect if the primary colors of both teams are too similar. If they are, use the away team's secondary color instead.

## Instructions
1. Implement a function to convert hex colors to RGB.
2. Implement a distance function to compare two colors in RGB space.
3. Define a threshold for similarity.
4. If home_primary and visitor_primary are below the threshold, switch visitor_color to visitor_secondary.

## Checklist
- [ ] Implement hex-to-RGB conversion
- [ ] Implement color distance comparison logic
- [ ] Define similarity threshold
- [ ] Implement fallback to secondary color for the visitor team

## Acceptance Criteria
- Teams with identical or very similar primary colors are visually distinguishable on the graph.
- The visitor team is the one that switches to their secondary color when a collision is detected.
