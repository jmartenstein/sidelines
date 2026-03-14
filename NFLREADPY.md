# nflreadpy Research & API Documentation

This document summarizes findings and data mapping for the `nflreadpy` library, which provides access to `nflverse` data, based on usage in this project.

## Core Functions

### Loading Play-by-Play (PBP) Data
- **Function**: `nflreadpy.load_pbp(seasons=[year])`
- **Returns**: A Polars DataFrame containing play-by-play information for the entire specified season(s).
- **Usage Note**: Does **not** accept a specific `game_id`. You must load the full season and then filter.

### Loading Schedule and Metadata
- **Function**: `nflreadpy.load_schedules(seasons=[year])`
- **Returns**: A Polars DataFrame with game metadata, including final scores, team abbreviations, and game IDs.
- **Performance**: Significantly faster than `load_pbp`. Use this for validation or retrieving game metadata (teams, scores, etc.) before loading detailed play data.

## Data Schema Mapping

The following mapping translates field names from generic/Kaggle datasets to their equivalents in `nflreadpy`.

| Concept | nflreadpy Field | Type | Notes |
| :--- | :--- | :--- | :--- |
| Game Identifier | `game_id` | String | Format: `'YYYY_WW_AWAY_HOME'` (e.g., `'2023_01_ARI_WAS'`) |
| Play Description | `desc` | String | Text description of the play |
| Time Remaining | `game_seconds_remaining` | Float | Total seconds remaining in the game. |
| Quarter | `qtr` | Float | Current quarter (1-4, 5 for OT). |
| Home Score (Running) | `total_home_score` | Int | Post-play home score. |
| Away Score (Running) | `total_away_score` | Int | Post-play away score. |
| Expected Points | `ep` | Float | Expected points added/value. |
| Possession Team | `posteam` | String | Abbreviation of the team with possession. (Note: Can be null during timeouts/metadata rows; use forward-fill for continuity). |
| Home Team | `home_team` | String | Abbreviation (found in Schedule & PBP). |
| Away Team | `away_team` | String | Abbreviation (found in Schedule & PBP). |
| Home Final Score | `home_score` | Int | Found in Schedule metadata. |
| Away Final Score | `away_score` | Int | Found in Schedule metadata. |

### Derived Metrics
- **Game Seconds Elapsed**: `(qtr - 1) * 900 + (900 - game_seconds_remaining)` (Assuming 900s quarters).

## Handling Missing Data

Certain fields in the PBP data may contain `null` or `NaN` values during non-play events (e.g., timeouts, quarter breaks, penalties). To ensure visual continuity in plots and accurate metric calculation:

1. **Possession Team (`posteam`)**: Often missing during timeouts. Use forward-fill (`ffill()`) to maintain the context of which team was last in possession for scatter plot coloring and "Expected" lead calculations.
2. **Expected Points (`ep`)**: Can be missing on bridge rows. Use forward-fill on derived "Expected" score columns to prevent artificial "dips" in the graph.
3. **Running Scores (`total_home_score` / `total_away_score`)**: These are **post-play** totals. To get **pre-snap** scores, shift the columns by 1 and forward-fill.

## Common Patterns & Best Practices

### 1. Game Validation Strategy
Since `load_pbp` is heavy, always validate a game's existence using `load_schedules` first.

```python
# Efficient check
schedules = nflreadpy.load_schedules(seasons=[2023])
game_info = schedules.filter(pl.col("game_id") == "2023_01_DET_KC")

if not game_info.is_empty():
    # Proceed to load PBP
    pbp = nflreadpy.load_pbp(seasons=[2023])
```

### 2. Polars to Pandas Conversion
To avoid PyArrow dependency issues or strictly for compatibility with Pandas-based plotting/analysis tools, convert using the dictionary method:

```python
# Robust conversion
df_pandas = pd.DataFrame(pl_dataframe.to_dicts())
```

### 3. Data Extraction
For extracting single-row metadata from Polars (e.g., from the schedule):
```python
game_row = game_info.row(0, named=True)
home_team = game_row["home_team"]
```

## Key Discoveries

- **Data Framework**: `nflreadpy` heavily utilizes **Polars** for its DataFrame operations.
- **Season-Based Loading**: Data is loaded per season. Filtering for a specific game happens *after* loading the season dataset.
- **String IDs**: The `game_id` is consistently a string (e.g., `'2023_01_ARI_WAS'`) across both PBP and schedule datasets, making joins and filtering straightforward.