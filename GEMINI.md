# Task Tracking

This project uses the *beans* task tracking utility for all task and issue management. Before starting any work, run the command below to understand the agent-specific workflow for *beans*.

!{beans prime}

# Project Overview

This project is designed to analyze NFL game data, specifically focusing on play-by-play statistics and score progressions over time.

## NFL API & Data

We rely on the `nflreadpy` library and the `nflverse` dataset. For detailed information on API usage, data schema, and field mappings, refer to:

@NFLREADPY.md

## Core Scripts

- `src/play_by_play.py`: (In development) Intended to process and analyze play-by-play data.
- `src/score_over_time.py`: (Being refactored) Migrating from local CSV loading to `nflreadpy` for real-time data fetching.
