import argparse
import nflreadpy
import polars as pl


def fetch_team_games(season, team_abbr):
    """
    Fetches NFL games for a specific team in a given season using nflreadpy.
    """
    try:
        # Load schedules for the season
        schedules = nflreadpy.load_schedules(seasons=[season])

        # Filter for the team (either home or away)
        team_games = schedules.filter(
            (pl.col("home_team") == team_abbr) | (pl.col("away_team") == team_abbr)
        )

        if team_games.is_empty():
            return []

        # Sort by game_id to maintain chronological order
        team_games = team_games.sort("game_id")

        games = []
        for row in team_games.to_dicts():
            home_team = row["home_team"]
            away_team = row["away_team"]

            games.append(
                {
                    "game_id": row["game_id"],
                    "home_team": home_team,
                    "away_team": away_team,
                    "home_score": row.get("home_score"),
                    "away_score": row.get("away_score"),
                }
            )
        return games

    except Exception as e:
        print(f"Error fetching data: {e}")
        return None


def display_team_games(games, season, team_abbr):
    """
    Displays the game information to the console in a tabular format.
    """
    if games is None:
        return

    if not games:
        print(f"No games found for {team_abbr} in {season}.")
        return

    print(f"Games for {team_abbr} in {season}:")
    print(f"{'Game ID':<20} | {'Home':<5} | {'Away':<5} | {'Score'}")
    print("-" * 50)

    for game in games:
        game_id = game["game_id"]
        home = game["home_team"]
        away = game["away_team"]

        if game["home_score"] is not None and game["away_score"] is not None:
            score = (
                f"{home} {int(game['home_score'])} - {away} {int(game['away_score'])}"
            )
        else:
            score = "N/A"

        print(f"{game_id:<20} | {home:<5} | {away:<5} | {score}")


def main():
    parser = argparse.ArgumentParser(
        description="List NFL games for a team in a season."
    )
    parser.add_argument("season", type=int, help="The season year (e.g., 2023)")
    parser.add_argument(
        "team", type=str, help="The 3-letter team abbreviation (e.g., KC)"
    )

    args = parser.parse_args()
    team_abbr = args.team.upper()

    games = fetch_team_games(args.season, team_abbr)
    display_team_games(games, args.season, team_abbr)


if __name__ == "__main__":
    main()
