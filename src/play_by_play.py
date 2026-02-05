"""
Fetches and returns play-by-play data for a given game ID.
"""

#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import sys
import logging

import nflreadpy
import polars as pl

# Configure logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Create handlers
if not logger.handlers:
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)


def get_play_by_play(game_id):
    """
    Fetches and returns play-by-play data for a given game ID.
    """
    # Extract season from game_id (YYYY_WEEK_HOME_AWAY)
    parts = game_id.split("_")
    if not parts or not parts[0].isdigit():
        print(f"Invalid game ID format: {game_id}")
        return None

    season = int(parts[0])

    # Validate game exists using schedules (much faster than loading full PBP)
    print(f"Validating game {game_id} in {season} schedule...")
    schedules = nflreadpy.load_schedules(seasons=[season])
    game_info = schedules.filter(pl.col("game_id") == game_id)

    if game_info.is_empty():
        print(f"Game ID {game_id} not found in {season} schedule.")
        return None

    # load_pbp returns a Polars DataFrame for the entire season(s)
    # Note: it does NOT accept game_id directly.
    print(f"Loading play-by-play data for {season} season...")
    df = nflreadpy.load_pbp(seasons=[season])

    # Filter for the specific game
    game_plays = df.filter(pl.col("game_id") == game_id)

    if game_plays.is_empty():
        print(f"No plays found for game ID: {game_id} (though it exists in schedule).")
        return None

    return game_plays.to_dicts()  # Return list of dictionaries


def display_play_by_play(play_by_play_data):
    """
    Displays the play-by-play data in a human-readable format.
    """
    if not play_by_play_data:
        print("No play-by-play data available to display.")
        return

    print("--- Play-by-Play Data ---")
    for play in play_by_play_data:
        # Using correct column names from nflreadpy: qtr, time, desc
        print(f"Q{play.get('qtr')} {play.get('time')} - {play.get('desc')}")
    print("-------------------------")


def main():
    """
    Main function
    """
    parser = argparse.ArgumentParser(
        description="Display NFL play-by-play data for a given game ID."
    )
    parser.add_argument(
        "game_id",
        type=str,
        help="The game ID in the format YYYY_MM_TEAM_TEAM (e.g., 2023_01_DET_KC).",
    )

    args = parser.parse_args()

    play_data = get_play_by_play(args.game_id)
    if play_data is not None:
        display_play_by_play(play_data)


if __name__ == "__main__":
    main()
