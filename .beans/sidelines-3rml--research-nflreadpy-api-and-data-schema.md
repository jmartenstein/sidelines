---
# sidelines-3rml
title: Research nflreadpy API and Data Schema
status: in-progress
type: task
priority: high
created_at: 2026-02-05T02:48:12Z
updated_at: 2026-02-05T02:57:53Z
parent: sidelines-j49e
blocking:
    - sidelines-84yg
---

Investigate the  documentation and API to determine how to fetch play-by-play data and game metadata. Specifically, find equivalents for  and  from the Kaggle dataset.

## Checklist
- [ ] Install nflreadpy for research
- [ ] Identify function for fetching play-by-play data by game ID
- [ ] Identify function for fetching game metadata (teams, final scores)
- [ ] Map nflreadpy columns to existing script's expectations (e.g., gameClock, quarter, preSnapHomeScore)