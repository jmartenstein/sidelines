---
# sidelines-3rml
title: Research nflreadpy API and Data Schema
status: completed
type: task
priority: high
created_at: 2026-02-05T02:48:12Z
updated_at: 2026-02-05T04:12:04Z
parent: sidelines-j49e
blocking:
    - sidelines-84yg
---

  Investigate the nflreadpy documentation and API to determine how to fetch play-by-play
  data and game metadata. Specifically, find equivalents for games.csv and plays.csv from the
  Kaggle dataset.

  ## Checklist

  [x] Install nflreadpy for research
  [x] Identify function for fetching play-by-play data by game ID
  [x] Identify function for fetching game metadata (teams, final scores)
  [x] Map nflreadpy columns to existing script's expectations (e.g., gameClock, quarter, preSnapHomeScore)

  ## Research Findings

  - **PBP Data**: Use `nflreadpy.load_pbp(season)`. Returns a Polars DataFrame.
  - **Schedule/Metadata**: Use `nflreadpy.load_schedules(season)`.
  - **Column Mapping**:
    - `gameId` (Kaggle) -> `game_id` (nflreadpy string ID like '2023_01_ARI_WAS')
    - `gameClock` (Kaggle mm:ss) -> `game_seconds_remaining` (nflreadpy seconds)
    - `quarter` (Kaggle) -> `qtr` (nflreadpy)
    - `preSnapHomeScore` -> `total_home_score`
    - `preSnapVisitorScore` -> `total_away_score`
    - `expectedPoints` -> `ep`
    - `possessionTeam` -> `posteam`
    - `homeTeamAbbr` -> `home_team`
    - `visitorTeamAbbr` -> `away_team`
    - `homeFinalScore` -> `home_score` (from schedule)
    - `visitorFinalScore` -> `away_score` (from schedule)