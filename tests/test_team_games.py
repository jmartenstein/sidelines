import pytest
from unittest.mock import patch
import polars as pl
from src.team_games import fetch_team_games, display_team_games

@patch("nflreadpy.load_schedules")
def test_fetch_team_games_success(mock_load_schedules):
    # Mock schedule data
    mock_data = {
        "game_id": ["2023_01_DET_KC", "2023_02_KC_JAX"],
        "home_team": ["KC", "JAX"],
        "away_team": ["DET", "KC"],
        "home_score": [20, 9],
        "away_score": [21, 17]
    }
    mock_load_schedules.return_value = pl.DataFrame(mock_data)
    
    games = fetch_team_games(2023, "KC")
    
    assert len(games) == 2
    assert games[0]["game_id"] == "2023_01_DET_KC"
    assert "opponent" not in games[0]
    assert games[1]["away_team"] == "KC"

@patch("nflreadpy.load_schedules")
def test_fetch_team_games_no_results(mock_load_schedules):
    mock_load_schedules.return_value = pl.DataFrame({
        "game_id": [], "home_team": [], "away_team": [], "home_score": [], "away_score": []
    })
    
    games = fetch_team_games(2023, "NON")
    assert games == []

def test_display_team_games_empty(capsys):
    display_team_games([], 2023, "KC")
    captured = capsys.readouterr()
    assert "No games found for KC in 2023." in captured.out

def test_display_team_games_with_data(capsys):
    games = [{
        "game_id": "2023_01_DET_KC",
        "home_team": "KC",
        "away_team": "DET",
        "home_score": 20,
        "away_score": 21
    }]
    display_team_games(games, 2023, "KC")
    captured = capsys.readouterr()
    assert "Games for KC in 2023:" in captured.out
    assert "Game ID              | Home  | Away  | Score" in captured.out
    assert "2023_01_DET_KC       | KC    | DET   | KC 20 - DET 21" in captured.out
