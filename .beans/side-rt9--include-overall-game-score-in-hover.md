---
# side-rt9
title: Include Overall Game Score in Hover
status: todo
type: task
priority: normal
created_at: 2026-02-07T01:45:46Z
updated_at: 2026-02-07T01:54:56Z
parent: side-thd
---

Ensure the running home and away scores are available in the hover tooltip to show the state of the game at the time of each play.

## Instructions
1. Use the existing preSnapHomeScore and preSnapVisitorScore columns.
2. Ensure these values are accessible within the on_add cursor callback function.

## Checklist
- [ ] Verify preSnapHomeScore and preSnapVisitorScore are correctly calculated
- [ ] Ensure score data is available in the plays_with_ep DataFrame
- [ ] Test that scores can be retrieved in the hover callback

## Acceptance Criteria
- Every play hover tooltip displays the home and visitor scores as they were just before the play started.
