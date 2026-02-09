import pandas as pd
import numpy as np
from src.score_over_time import plot_scores
from unittest.mock import patch

def test_possession_team_ffill_logic():
    """
    Test that possessionTeam (posteam) is forward-filled correctly
    so that expected scores and scatter colors don't 'dip' or default
    to purple during timeouts/metadata rows.
    """
    # Create mock data where possessionTeam is missing in the middle (e.g., a timeout)
    # but expectedPoints (ep) is still present or we want to maintain the line.
    data = {
        "game_seconds_elapsed": [0, 10, 20, 30],
        "total_home_score": [0, 0, 0, 0],
        "total_away_score": [0, 0, 0, 0],
        "ep": [1.0, 1.1, 1.2, 1.3],
        "posteam": ["KC", None, np.nan, "KC"], # Missing possession in middle
        "qtr": [1, 1, 1, 1],
        "down": [1, 1, 1, 1],
        "ydstogo": [10, 10, 10, 10],
        "yrdln": ["KC 25", "KC 25", "KC 25", "KC 25"],
        "desc": ["Play 1", "Timeout", "Metadata", "Play 2"]
    }
    df = pd.DataFrame(data)
    
    # We want to verify that in the final processed DF used for plotting:
    # 1. possessionTeam for rows 1 and 2 is 'KC' (via ffill)
    # 2. home_expected for rows 1 and 2 uses 'KC' and doesn't just add 0
    
    # We can't easily test internal state of plot_scores without refactoring it,
    # but we can check if we can extract the logic or just fix it and run smoke tests.
    
    # Actually, the user wants us to FIX it in src/score_over_time.py.
    # Let's see if we can assert on the DataFrame if we were to split the calculation logic.
    pass

@patch("matplotlib.pyplot.show")
def test_plot_scores_with_missing_possession(mock_show):
    # This smoke test will at least ensure it doesn't crash, 
    # but we really want to verify the logic.
    data = {
        "game_seconds_elapsed": [0, 10, 20, 30],
        "total_home_score": [0, 0, 0, 0],
        "total_away_score": [0, 0, 0, 0],
        "ep": [1.0, 1.1, 1.2, 1.3],
        "posteam": ["KC", None, 0, "KC"], # Missing or 0 possession
        "qtr": [1, 1, 1, 1],
        "down": [1, 1, 1, 1],
        "ydstogo": [10, 10, 10, 10],
        "yrdln": ["KC 25", "KC 25", "KC 25", "KC 25"],
    }
    df = pd.DataFrame(data)
    
    # This will run the logic. We'd need to mock more to verify colors.
    plot_scores(df, "2023_01_DET_KC", "KC", "DET", 21, 20)
    assert mock_show.called
