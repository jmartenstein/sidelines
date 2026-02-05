#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
import sys
import os
import subprocess
import time
import logging
from typing import Dict, Any, List, Optional

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

# Placeholder for nflreadpy import and its associated functionality
# In a real scenario, this would be imported if available.
# For the purpose of this script, we'll simulate its behavior or expect it to be installed.
try:
    from nflreadpy import read_game
except ImportError:
    print("Error: The 'nflreadpy' library is not installed.")
    print("Please install it using: pip install nflreadpy")

    # In a production script, you might want to exit here or handle this more gracefully.
    # For this example, we'll define dummy functions to allow the script structure to be written.
    class MockGameData:
        def __init__(self):
            self.play_by_play = []

    def read_game(game_id):
        print(f"Mock read_game called with: {game_id}")
        # Simulate some data for testing if nflreadpy is not installed
        if game_id == "2023_01_DET_KC":
            mock_data = MockGameData()
            mock_data.play_by_play = [
                type(
                    "Play",
                    (object,),
                    {"quarter": 1, "time_remaining": "15:00", "text": "Kickoff"},
                ),
                type(
                    "Play",
                    (object,),
                    {
                        "quarter": 1,
                        "time_remaining": "14:30",
                        "text": "A team runs a play.",
                    },
                ),
                type(
                    "Play",
                    (object,),
                    {
                        "quarter": 1,
                        "time_remaining": "14:00",
                        "text": "Another team completes a pass.",
                    },
                ),
            ]
            return mock_data
        else:
            raise ValueError(f"Mock data not available for game ID: {game_id}")


def get_play_by_play(game_id):
    """
    Fetches and returns play-by-play data for a given game ID.
    """
    try:
        # nflreadpy expects game_id in 'YYYY_MM_TEAM_TEAM' format
        # Example: 2023_01_DET_KC
        game_data = read_game(game_id)
        return game_data.play_by_play
    except Exception as e:
        print(f"Error fetching data for game ID {game_id}: {e}")
        return None


def display_play_by_play(play_by_play_data):
    """
    Displays the play-by-play data in a human-readable format.
    """
    if not play_by_play_data:
        print("No play-by-play data available to display.")
        return

    print("--- Play-by-Play Data ---")
    for play in play_by_play_data:
        print(f"Q{play.quarter} {play.time_remaining} - {play.text}")
    print("-------------------------")


def main():
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
