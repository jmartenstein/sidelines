import pytest
from unittest.mock import patch, MagicMock
import polars as pl
from src.play_by_play import get_play_by_play, display_play_by_play

def test_get_play_by_play_invalid_id():
    assert get_play_by_play("invalid_id") is None
    assert get_play_by_play("not_a_number_week_team_team") is None

@patch("nflreadpy.load_schedules")
def test_get_play_by_play_game_not_in_schedule(mock_load_schedules):
    # Mock schedules to be empty for the given season
    mock_load_schedules.return_value = pl.DataFrame({"game_id": []})
    
    assert get_play_by_play("2023_01_DET_KC") is None
    mock_load_schedules.assert_called_once_with(seasons=[2023])

@patch("nflreadpy.load_pbp")
@patch("nflreadpy.load_schedules")
def test_get_play_by_play_no_plays_found(mock_load_schedules, mock_load_pbp):
    game_id = "2023_01_DET_KC"
    # Mock schedule to contain the game
    mock_load_schedules.return_value = pl.DataFrame({"game_id": [game_id]})
    # Mock PBP to be empty for the season or at least not have this game
    mock_load_pbp.return_value = pl.DataFrame({"game_id": ["2023_01_OTHER_GAME"]})
    
    assert get_play_by_play(game_id) is None

@patch("nflreadpy.load_pbp")
@patch("nflreadpy.load_schedules")
def test_get_play_by_play_success(mock_load_schedules, mock_load_pbp):
    game_id = "2023_01_DET_KC"
    # Mock schedule
    mock_load_schedules.return_value = pl.DataFrame({"game_id": [game_id]})
    # Mock PBP
    mock_pbp_data = {
        "game_id": [game_id, game_id],
        "qtr": [1, 1],
        "desc": ["Play 1", "Play 2"],
        "ep": [0.5, 1.2]
    }
    mock_load_pbp.return_value = pl.DataFrame(mock_pbp_data)
    
    result = get_play_by_play(game_id)
    
    assert result is not None
    assert len(result) == 2
    assert result[0]["desc"] == "Play 1"
    assert result[1]["ep"] == 1.2

def test_display_play_by_play_empty(capsys):
    display_play_by_play([])
    captured = capsys.readouterr()
    assert "No play-by-play data available to display." in captured.out

def test_display_play_by_play_with_data(capsys):
    data = [
        {"qtr": 1, "desc": "Touchdown", "ep": 7.0},
        {"qtr": 2, "desc": "Field Goal", "ep": 3.0},
        {"qtr": None, "desc": "Unknown", "ep": None}
    ]
    display_play_by_play(data)
    captured = capsys.readouterr()
    assert "--- Play-by-Play Data ---" in captured.out
    assert "[  7.00] Q1 - Touchdown" in captured.out
    assert "[  3.00] Q2 - Field Goal" in captured.out
    assert "[   N/A] Q? - Unknown" in captured.out
