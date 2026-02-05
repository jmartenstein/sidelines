import sys
import os
import argparse
import nflreadpy
import polars as pl

import pandas as pd
import matplotlib.pyplot as plt

### CONSTANTS ###

# RAW_DATA_DIR = "data/kaggle" # No longer needed with nflreadpy

### FUNCTIONS ###

def get_season_from_game_id(game_id_str):
    """
    Infers the season from the nflverse game ID string (e.g., 'YYYY_WEEK_HOME_AWAY').
    Returns the season as an integer.
    """
    try:
        # Assuming the game_id_str is in the format 'YYYY_...'
        season = int(game_id_str.split('_')[0])
        return season
    except (IndexError, ValueError) as e:
        print(f"Could not infer season from game ID '{game_id_str}'. Using default 2023. Error: {e}")
        return 2023 # Defaulting to 2023 season if inference fails

def load_plays_for_game(target_game_id_str, season):
    """Loads play-by-play data for a specific game using nflreadpy."""
    try:
        # Load all play-by-play data for the season
        pbp_df_polars = nflreadpy.load_pbp(season)

        # Filter for the specific game ID using Polars
        game_plays_polars = pbp_df_polars.filter(pl.col("game_id") == target_game_id_str)

        if game_plays_polars.is_empty():
            print(f"Warning: No plays found for game ID: {target_game_id_str} in season {season}")
            return pd.DataFrame() # Return empty Pandas DataFrame

        return game_plays_polars.to_pandas() # Convert to Pandas DataFrame for compatibility

    except Exception as e:
        print(f"Error loading play-by-play data for game {target_game_id_str} in season {season}: {e}")
        return pd.DataFrame()


def load_game_info(target_game_id_str, season):
    """Loads game metadata for a specific game using nflreadpy."""
    try:
        # Load schedules for the season
        schedules_df_polars = nflreadpy.load_schedules(season)

        # Filter for the specific game ID using Polars
        game_info_polars = schedules_df_polars.filter(pl.col("game_id") == target_game_id_str)

        if game_info_polars.is_empty():
            print(f"Warning: No game info found for game ID: {target_game_id_str} in season {season}")
            return pd.DataFrame() # Return empty Pandas DataFrame

        return game_info_polars.to_pandas()

    except Exception as e:
        print(f"Error loading game info for game {target_game_id_str} in season {season}: {e}")
        return pd.DataFrame()


def game_clock_to_seconds(clock_str):
    """Converts mm:ss to total seconds remaining in quarter."""
    if pd.isna(clock_str) or not isinstance(clock_str, str):
        return 0
    parts = clock_str.split(":")
    if len(parts) != 2:
        return 0
    try:
        m, s = map(int, parts)
        return m * 60 + s
    except ValueError:
        return 0

def get_sorted_plays(df):
    """Sorts plays chronologically by quarter and clock."""
    # nflreadpy provides 'qtr' (float) and 'game_seconds_remaining' (float) directly.
    # We need to calculate 'game_seconds_elapsed' for plotting consistency.
    
    # Ensure 'qtr' is float for calculation
    df['qtr'] = df['qtr'].astype(float)
    
    # Calculate game seconds elapsed: (quarter - 1) * 900 + (900 - seconds_remaining_in_quarter)
    # Assuming 900 seconds per quarter (15 minutes).
    df["game_seconds_elapsed"] = (df["qtr"] - 1) * 900 + (900 - df["game_seconds_remaining"])
    
    # Sort plays chronologically
    return df.sort_values(by=["qtr", "game_seconds_remaining"], ascending=[True, False])


def plot_scores(
    df,
    target_game_id_str, # Expecting string game ID
    home_team_name,
    visitor_team_name,
    final_home_score,
    final_visitor_score,
    output_path=None,
):
    """Generates and displays (or saves) a plot of scores and net difference over time."""
    
    # Rename columns for consistency with the original script's logic
    df = df.rename(columns={
        "total_home_score": "preSnapHomeScore",
        "total_away_score": "preSnapVisitorScore",
        "ep": "expectedPoints",
        "posteam": "possessionTeam",
        "qtr": "quarter", # Rename 'qtr' to 'quarter' for consistency
        # 'game_seconds_remaining' is already used as 'gameClock_seconds' in original plot_scores if needed directly, but we use game_seconds_elapsed
    })

    # Ensure that the team names used for comparison are consistent.
    # The `home_team_name` and `visitor_team_name` are expected to be abbreviations.
    # `df['possessionTeam']` should match these if `nflreadpy` data is filtered correctly.

    # Calculate Expected Scores
    df["home_expected"] = df.apply(
        lambda row: row["preSnapHomeScore"]
        + (row["expectedPoints"] if row["possessionTeam"] == home_team_name else 0),
        axis=1,
    )
    df["visitor_expected"] = df.apply(
        lambda row: row["preSnapVisitorScore"]
        + (row["expectedPoints"] if row["possessionTeam"] == visitor_team_name else 0),
        axis=1,
    )

    # Determine leading team (winner) for the Y-axis reference
    if final_home_score >= final_visitor_score:
        pos_team, neg_team = home_team_name, visitor_team_name
        df["net_actual"] = df["preSnapHomeScore"] - df["preSnapVisitorScore"]
        df["net_expected"] = df["home_expected"] - df["visitor_expected"]
        pos_color, neg_color = "blue", "red"
    else:
        pos_team, neg_team = visitor_team_name, home_team_name
        df["net_actual"] = df["preSnapVisitorScore"] - df["preSnapHomeScore"]
        df["net_expected"] = df["visitor_expected"] - df["home_expected"]
        pos_color, neg_color = "red", "blue"

    # Create subplots with shared X axis and different height ratios
    _, (ax1, ax2) = plt.subplots(
        2, 1, figsize=(10, 7), sharex=True, gridspec_kw={"height_ratios": [3, 1]}
    )

    # --- Top Subplot: Scores ---
    ax1.step(
        df["game_seconds_elapsed"],
        df["preSnapHomeScore"],
        label=f"{home_team_name} Actual",
        where="post",
        color="blue",
        alpha=0.3,
    )
    ax1.step(
        df["game_seconds_elapsed"],
        df["preSnapVisitorScore"],
        label=f"{visitor_team_name} Actual",
        where="post",
        color="red",
        alpha=0.3,
    )

    ax1.plot(
        df["game_seconds_elapsed"],
        df["home_expected"],
        label=f"{home_team_name} Expected",
        color="blue",
        linewidth=2,
    )
    ax1.plot(
        df["game_seconds_elapsed"],
        df["visitor_expected"],
        label=f"{visitor_team_name} Expected",
        color="red",
        linewidth=2,
    )

    ax1.set_title(
        f"Score and Expected Points: {visitor_team_name} at {home_team_name} ({target_game_id_str})"
    )
    ax1.set_ylabel("Points")
    ax1.legend()
    ax1.grid(True, linestyle="--", alpha=0.7)

    # --- Bottom Subplot: Net Difference (Winner is Positive) ---
    ax2.step(
        df["game_seconds_elapsed"],
        df["net_actual"],
        label="Actual Diff",
        where="post",
        color="black",
        alpha=0.2,
    )
    ax2.plot(
        df["game_seconds_elapsed"],
        df["net_expected"],
        label="Expected Diff",
        color="purple",
        linewidth=1.5,
    )

    ax2.fill_between(
        df["game_seconds_elapsed"],
        0,
        df["net_expected"],
        where=(df["net_expected"] >= 0),
        color=pos_color,
        alpha=0.2,
        label=f"{pos_team} Lead",
        interpolate=True,
    )
    ax2.fill_between(
        df["game_seconds_elapsed"],
        0,
        df["net_expected"],
        where=(df["net_expected"] < 0),
        color=neg_color,
        alpha=0.2,
        label=f"{neg_team} Lead",
        interpolate=True,
    )

    ax2.axhline(y=0, color="black", linestyle="-", linewidth=1.0)  # Baseline

    ax2.set_ylabel(f"Lead Magnitude\n({pos_team} Lead +)")
    ax2.set_xlabel("Game Seconds Elapsed")
    ax2.legend(loc="upper right", fontsize="x-small")
    ax2.grid(True, linestyle="--", alpha=0.7)

    # Add vertical lines for quarter breaks to both subplots
    for ax in [ax1, ax2]:
        for q in range(1, 5):
            ax.axvline(x=q * 900, color="gray", linestyle="-", alpha=0.5)
            if ax == ax1:
                ax.text(
                    q * 900 - 450,
                    ax.get_ylim()[1] * 0.95,
                    f"Q{q}",
                    horizontalalignment="center",
                )

    plt.tight_layout()
    if output_path:
        plt.savefig(output_path)
        print(f"Graph saved to {output_path}")
    else:
        plt.show()


### MAIN ###

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Plot scores and expected points over time for a specific game."
    )
    # Expecting game_id to be a string in nflverse format, e.g., '2023_01_ARI_WAS'
    parser.add_argument("game_id", type=str, help="The nflverse game ID (e.g., '2023_01_ARI_WAS').")
    parser.add_argument(
        "-o",
        "--output",
        help="Path to save the output graph file (e.g., 'output.png'). " +
             "If not provided, the graph will be displayed.",
    )

    args = parser.parse_args()
    game_id_str = args.game_id # This is now expected to be a string
    output_arg = args.output

    # Determine season from game_id_str.
    season = get_season_from_game_id(game_id_str)

    # Load game metadata
    df_game = load_game_info(game_id_str, season)
    if df_game.empty:
        print(f"Could not find game info for game ID: {game_id_str} in season {season}")
        sys.exit(1)

    # Extract team names and final scores from game_info DataFrame
    # Use .iloc[0] as filter should return at most one row.
    try:
        home_team_name = df_game["homeTeamAbbr"].iloc[0]
        visitor_team_name = df_game["visitorTeamAbbr"].iloc[0]
        home_final_score = df_game["homeFinalScore"].iloc[0]
        visitor_final_score = df_game["visitorFinalScore"].iloc[0]
    except IndexError:
        print("Error: Could not retrieve team names or scores from game info. Ensure game_id is correct and data is loaded.")
        sys.exit(1)
    except KeyError as e:
        print(f"Error: Missing expected column in game info: {e}")
        sys.exit(1)
    

    # Load plays for the game
    df_plays_pd = load_plays_for_game(game_id_str, season)
    if df_plays_pd.empty:
        print(f"No plays found for game ID: {game_id_str}")
        sys.exit(1)
    
    # Sort plays chronologically
    df_sorted = get_sorted_plays(df_plays_pd)

    # Generate Plot
    plot_scores(
        df_sorted,
        game_id_str, # Pass the string game ID
        home_team_name,
        visitor_team_name,
        home_final_score,
        visitor_final_score,
        output_path=output_arg,
    )