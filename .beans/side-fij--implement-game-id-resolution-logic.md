---
# side-fij
title: Implement game ID resolution logic
status: completed
type: task
priority: high
created_at: 2026-02-05T16:51:11Z
updated_at: 2026-02-05T17:21:19Z
parent: side-yba
---

  nflreadpy.load_pbp does NOT appear to accept a 'game_id' argument in the
  current version. It only takes 'seasons'. Once the full season data is
  loaded, it contains both 'game_id' (string format like '2023_01_DET_KC') and
  'old_game_id' (10-digit numeric string).

  I found that src/score_over_time.py is currently calling
  nflreadpy.load_pbp(game_id=...), which fails with a TypeError.

  Findings:

  1. nflreadpy.load_pbp(seasons=2023) returns a Polars DataFrame for the whole
  season.
  2. The returned DataFrame has both 'game_id' and 'old_game_id' columns.
  3. Filtering by 'game_id' (e.g. '2023_01_DET_KC') is possible after loading
  the season.
  4. src/play_by_play.py currently uses a mock read_game function which
  doesn't exist in nflreadpy.

  ## Checklist

  [x] Fetch schedules for the target season to validate game exists.
  [x] Add logic to parse YYYY_WEEK_HOME_AWAY format.
  [x] Implement loading of full season PBP data and filtering by game_id.
  [x] Handle cases where the game cannot be found.