import pytest
import pandas as pd
import polars as pl
from unittest.mock import patch, MagicMock
from src.score_over_time import (
    get_game_id_and_metadata,
    get_season_from_game_id,
    load_plays_for_game,
    load_game_info,
    game_clock_to_seconds,
    get_sorted_plays,
    plot_scores
)

def test_get_season_from_game_id():
    assert get_season_from_game_id("2023_01_DET_KC") == 2023
    assert get_season_from_game_id("2024_02_SF_SEA") == 2024
    assert get_season_from_game_id("invalid") == 2023  # Default

def test_game_clock_to_seconds():
    assert game_clock_to_seconds("15:00") == 900
    assert game_clock_to_seconds("00:00") == 0
    assert game_clock_to_seconds("08:30") == 510
    assert game_clock_to_seconds(None) == 0
    assert game_clock_to_seconds("invalid") == 0

@patch("nflreadpy.load_schedules")
def test_get_game_id_and_metadata_success(mock_load_schedules):
    game_id_str = "2023_01_DET_KC"
    mock_row = {
        "game_id": game_id_str,
        "home_team": "KC",
        "away_team": "DET",
        "week": 1,
        "season": 2023
    }
    mock_load_schedules.return_value = pl.DataFrame([mock_row])
    
    game_id, metadata_df = get_game_id_and_metadata(game_id_str)
    
    assert game_id == game_id_str
    assert isinstance(metadata_df, pd.DataFrame)
    assert metadata_df.iloc[0]["home_team"] == "KC"

@patch("nflreadpy.load_schedules")
def test_get_game_id_and_metadata_not_found(mock_load_schedules):
    mock_load_schedules.return_value = pl.DataFrame({"game_id": []})
    game_id, metadata_df = get_game_id_and_metadata("2023_01_DET_KC")
    assert game_id is None
    assert metadata_df is None

def test_get_game_id_and_metadata_invalid_format():
    game_id, metadata_df = get_game_id_and_metadata("invalid_format")
    assert game_id is None
    assert metadata_df is None

@patch("src.score_over_time.get_game_id_and_metadata")
@patch("nflreadpy.load_pbp")
def test_load_plays_for_game_success(mock_load_pbp, mock_get_metadata):
    game_id = "2023_01_DET_KC"
    mock_get_metadata.return_value = (game_id, pd.DataFrame([{"game_id": game_id}]))
    
    mock_pbp_data = {
        "game_id": [game_id, "other_game"],
        "qtr": [1, 1],
        "total_home_score": [0, 0],
        "total_away_score": [0, 0]
    }
    mock_load_pbp.return_value = pl.DataFrame(mock_pbp_data)
    
    df = load_plays_for_game(game_id, 2023)
    
    assert not df.empty
    assert len(df) == 1
    assert df.iloc[0]["game_id"] == game_id

def test_get_sorted_plays():
    data = {
        "qtr": [2, 1, 1],
        "game_seconds_remaining": [900, 450, 900]
    }
    df = pd.DataFrame(data)
    sorted_df = get_sorted_plays(df)
    
    # Expected order: Q1 900, Q1 450, Q2 900
    assert sorted_df.iloc[0]["qtr"] == 1
    assert sorted_df.iloc[0]["game_seconds_remaining"] == 900
    assert sorted_df.iloc[1]["qtr"] == 1
    assert sorted_df.iloc[1]["game_seconds_remaining"] == 450
    assert sorted_df.iloc[2]["qtr"] == 2
    
    # Check game_seconds_elapsed
    # Q1 900 -> (1-1)*900 + (900-900) = 0
    # Q1 450 -> (1-1)*900 + (900-450) = 450
    # Q2 900 -> (2-1)*900 + (900-900) = 900
    assert sorted_df.iloc[0]["game_seconds_elapsed"] == 0
    assert sorted_df.iloc[1]["game_seconds_elapsed"] == 450
    assert sorted_df.iloc[2]["game_seconds_elapsed"] == 900

@patch("matplotlib.pyplot.show")
@patch("matplotlib.pyplot.savefig")
def test_plot_scores_smoke_test(mock_savefig, mock_show):
    # Minimal data to avoid errors in plot_scores
    data = {
        "game_seconds_elapsed": [0, 900],
        "total_home_score": [0, 7],
        "total_away_score": [0, 3],
        "ep": [0.5, 0.5],
        "posteam": ["KC", "DET"],
        "qtr": [1, 2]
    }
    df = pd.DataFrame(data)
    
    # Test showing plot
    plot_scores(df, "2023_01_DET_KC", "KC", "DET", 21, 20)
    mock_show.assert_called_once()
    
    # Test saving plot
    plot_scores(df, "2023_01_DET_KC", "KC", "DET", 21, 20, output_path="test.png")
    mock_savefig.assert_called_once_with("test.png")

@patch("src.score_over_time.get_game_id_and_metadata")
def test_load_game_info_success(mock_get_metadata):
    game_id = "2023_01_DET_KC"
    mock_df = pd.DataFrame([{"game_id": game_id, "home_team": "KC"}])
    mock_get_metadata.return_value = (game_id, mock_df)
    
    df = load_game_info(game_id, 2023)
    assert not df.empty
    assert df.iloc[0]["home_team"] == "KC"

@patch("src.score_over_time.get_game_id_and_metadata")
def test_load_game_info_not_found(mock_get_metadata):
    mock_get_metadata.return_value = (None, None)
    df = load_game_info("invalid", 2023)
    assert df.empty
