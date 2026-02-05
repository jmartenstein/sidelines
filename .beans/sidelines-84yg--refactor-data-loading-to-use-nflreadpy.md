---
# sidelines-84yg
title: Refactor Data Loading to use nflreadpy
status: completed
type: task
priority: high
created_at: 2026-02-05T02:48:36Z
updated_at: 2026-02-05T04:20:04Z
parent: sidelines-j49e
blocking:
    - sidelines-xz75
---

  Modify src/score_over_time.py to replace local CSV loading functions (load_plays_for_game and load_game_info) with nflreadpy calls.

  ## Checklist

  [x] Import nflreadpy in src/score_over_time.py
  [x] Implement new data fetching logic
  [x] Handle potential API errors or missing data from nflreadpy

  ## Research Findings

  - **PBP Data**: Use `nflreadpy.load_pbp(season)`. Returns a Polars DataFrame.
  - **Schedule/Metadata**: Use `nflreadpy.load_schedules(season)`.
  - **Column Mapping**:
    - `gameId` (Kaggle int) needs mapping to nflverse string ID (e.g., '2023_01_ARI_WAS'). The script now infers season and expects string game IDs.
    - `gameClock` (Kaggle mm:ss) -> `game_seconds_remaining` (nflreadpy seconds)
    - `quarter` (Kaggle) -> `qtr` (nflreadpy)
    - `preSnapHomeScore` -> `total_home_score`
    - `preSnapVisitorScore` -> `total_away_score`
    - `expectedPoints` -> `ep`
    - `possessionTeam` -> `posteam`
    - `homeTeamAbbr` -> `home_team`
    - `visitorTeamAbbr` -> `away_team`
    - `homeFinalScore` -> `homeFinalScore` (from schedule df)
    - `visitorFinalScore` -> `visitorFinalScore` (from schedule df)