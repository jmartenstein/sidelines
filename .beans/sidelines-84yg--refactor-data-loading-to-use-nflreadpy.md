---
# sidelines-84yg
title: Refactor Data Loading to use nflreadpy
status: todo
type: task
priority: high
created_at: 2026-02-05T02:48:36Z
updated_at: 2026-02-05T02:49:33Z
parent: sidelines-j49e
blocking:
    - sidelines-xz75
---

Modify  to replace local CSV loading functions ( and ) with  calls.

## Checklist
- [ ] Import nflreadpy in src/score_over_time.py
- [ ] Implement new data fetching logic
- [ ] Handle potential API errors or missing data from nflreadpy