# nflreadpy Research & API Documentation

This document summarizes findings and data mapping for the `nflreadpy` library, which provides access to `nflverse` data.

## Core Functions

### Loading Play-by-Play (PBP) Data
- **Function**: `nflreadpy.load_pbp(season)`
- **Returns**: A Polars DataFrame containing play-by-play information for the specified season.

### Loading Schedule and Metadata
- **Function**: `nflreadpy.load_schedules(season)`
- **Returns**: A Polars DataFrame with game metadata, including final scores, team abbreviations, and game IDs.

## Data Schema Mapping

The following mapping translates field names from the Kaggle dataset to their equivalents in `nflreadpy`.

| Kaggle Field | nflreadpy Field | Notes |
| :--- | :--- | :--- |
| `gameId` | `game_id` | nflreadpy uses string IDs (e.g., `'2023_01_ARI_WAS'`) |
| `gameClock` | `game_seconds_remaining` | Kaggle uses `mm:ss`, nflreadpy uses total seconds |
| `quarter` | `qtr` | |
| `preSnapHomeScore` | `total_home_score` | |
| `preSnapVisitorScore` | `total_away_score` | |
| `expectedPoints` | `ep` | |
| `possessionTeam` | `posteam` | |
| `homeTeamAbbr` | `home_team` | |
| `visitorTeamAbbr` | `away_team` | |
| `homeFinalScore` | `home_score` | Found in schedule metadata |
| `visitorFinalScore` | `away_score` | Found in schedule metadata |

## Key Discoveries

- **Data Framework**: `nflreadpy` heavily utilizes **Polars** for its DataFrame operations, offering high-performance data handling.
- **Season-Based Loading**: Data is typically loaded per season, requiring iteration or filtering for multi-year analysis.
- **Game ID Format**: The `game_id` string format (Year_Week_Away_Home) is consistent across PBP and schedule datasets, facilitating easy joins.
