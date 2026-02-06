import sys
import argparse
import textwrap

import nflreadpy
import polars as pl
import pandas as pd
import matplotlib.pyplot as plt
import mplcursors

### FUNCTIONS ###


def get_game_id_and_metadata(target_game_id_str):
    """
    Parses a game ID string (YYYY_WEEK_HOME_AWAY), loads schedules for the season,
    filters to find the specific game, and returns its 10-digit game_id and metadata.
    Returns (None, None) if the game is not found or an error occurs.
    """
    try:
        parts = target_game_id_str.split("_")
        if len(parts) != 4:
            print(
                f"Invalid game ID format: {target_game_id_str}. Expected YYYY_WEEK_HOME_AWAY."
            )
            return None, None

        season = int(parts[0])
        week = int(parts[1])
        home_team_abbr = parts[2]
        visitor_team_abbr = parts[3]

        # Load schedules for the given season
        # nflreadpy.load_schedules takes 'seasons' as an argument.
        schedules_df = nflreadpy.load_schedules(seasons=season)

        # Filter for the specific game using week, home_team, and away_team
        # Note: nflreadpy uses 'home_team' and 'away_team' for abbreviations.
        # The actual game_id column is a 10-digit number.
        game_info_polars = schedules_df.filter(
            (pl.col("game_id") == target_game_id_str)
        )

        if game_info_polars.is_empty():
            print(
                f"Warning: No game info found for game ID: {target_game_id_str} (Season: {season}, Week: {week}, Home: {home_team_abbr}, Away: {visitor_team_abbr})"
            )
            return None, None

        # Assuming only one game matches these criteria, take the first row
        game_row = game_info_polars.row(0, named=True)

        # Extract the 10-digit game_id and convert it to string
        game_id_10_digit = str(game_row["game_id"])

        # Create a Pandas DataFrame for the metadata, similar to original behavior
        metadata_df = pd.DataFrame([game_row])

        return game_id_10_digit, metadata_df

    except (ValueError, IndexError) as e:
        print(f"Error parsing game ID '{target_game_id_str}': {e}")
        return None, None


def get_season_from_game_id(game_id_str):
    """
    Infers the season from the nflverse game ID string (e.g., 'YYYY_WEEK_HOME_AWAY').
    Returns the season as an integer.
    """
    try:
        # Assuming the game_id_str is in the format 'YYYY_...'
        season = int(game_id_str.split("_")[0])
        return season
    except (IndexError, ValueError) as e:
        print(
            f"Could not infer season from game ID '{game_id_str}'. Using default 2023. Error: {e}"
        )
        return 2023  # Defaulting to 2023 season if inference fails


def load_plays_for_game(
    target_game_id_str, season
):  # 'season' parameter is no longer strictly needed but kept for signature compatibility
    """Loads play-by-play data for a specific game using nflreadpy."""
    # Use the helper function to get the 10-digit game_id and metadata
    game_id_10_digit, metadata_df = get_game_id_and_metadata(target_game_id_str)

    if game_id_10_digit is None:
        # get_game_id_and_metadata already prints warnings/errors
        return pd.DataFrame()

    # Corrected: Use 'seasons' parameter and then filter by game_id string
    pbp_df_polars = nflreadpy.load_pbp(seasons=[season])

    if pbp_df_polars.is_empty():
        print(f"Warning: No plays found for season {season}.")
        return pd.DataFrame()

    # Filter the loaded DataFrame for the specific game using the string ID
    game_plays = pbp_df_polars.filter(pl.col("game_id") == target_game_id_str)

    if game_plays.is_empty():
        print(
            f"Warning: No plays found for game ID: {target_game_id_str} (10-digit ID: {game_id_10_digit}) after loading season data."
        )
        return pd.DataFrame()

    # Convert to Pandas DataFrame via list of dicts to avoid pyarrow dependency
    return pd.DataFrame(game_plays.to_dicts())


def load_game_info(
    target_game_id_str, season
):  # 'season' parameter is no longer strictly needed but kept for signature compatibility if called elsewhere
    """Loads game metadata for a specific game using nflreadpy."""
    # Use the helper function to get the 10-digit game_id and metadata
    game_id_10_digit, metadata_df = get_game_id_and_metadata(target_game_id_str)

    if metadata_df is None or metadata_df.empty:
        # get_game_id_and_metadata already prints warnings/errors
        return pd.DataFrame()

    # The helper function returns the metadata as a Pandas DataFrame
    return metadata_df


def get_sorted_plays(df):
    """Sorts plays chronologically by quarter and clock."""
    # nflreadpy provides 'qtr' (float) and 'game_seconds_remaining' (float) directly.
    # We need to calculate 'game_seconds_elapsed' for plotting consistency.

    # Ensure 'qtr' is float for calculation
    df["qtr"] = df["qtr"].astype(float)

    # Calculate game seconds elapsed: Total game seconds (3600) - game_seconds_remaining
    # nflreadpy's game_seconds_remaining is total seconds remaining in the game.
    df["game_seconds_elapsed"] = 3600 - df["game_seconds_remaining"]

    # Sort plays chronologically
    return df.sort_values(by=["qtr", "game_seconds_remaining"], ascending=[True, False])


def plot_scores(
    df,
    target_game_id_str,  # Expecting string game ID
    home_team_name,
    visitor_team_name,
    final_home_score,
    final_visitor_score,
    output_path=None,
    debug=False,
):
    """Generates and displays (or saves) a plot of scores and net difference over time."""

    # Calculate pre-snap scores correctly using posteam_score/defteam_score
    # This avoids "double counting" on scoring plays where total_home_score includes the points.
    def get_presnap_home(row):
        # If posteam matches home, return posteam_score
        if pd.notna(row["posteam"]) and pd.notna(row["posteam_score"]):
            if row["posteam"] == home_team_name:
                return row["posteam_score"]
            elif row["posteam"] == visitor_team_name:
                return row["defteam_score"]
        # Fallback for timeouts, end of quarter, or missing data
        return row["total_home_score"]

    def get_presnap_visitor(row):
        # If posteam matches visitor, return posteam_score
        if pd.notna(row["posteam"]) and pd.notna(row["posteam_score"]):
            if row["posteam"] == visitor_team_name:
                return row["posteam_score"]
            elif row["posteam"] == home_team_name:
                return row["defteam_score"]
        # Fallback
        return row["total_away_score"]

    df["preSnapHomeScore"] = df.apply(get_presnap_home, axis=1)
    df["preSnapVisitorScore"] = df.apply(get_presnap_visitor, axis=1)

    # Rename columns for consistency with the original script's logic
    df = df.rename(
        columns={
            # "total_home_score": "preSnapHomeScore", # Now calculated above
            # "total_away_score": "preSnapVisitorScore", # Now calculated above
            "ep": "expectedPoints",
            "epa": "expectedPointsAdded",
            "posteam": "possessionTeam",
            "qtr": "quarter",  # Rename 'qtr' to 'quarter' for consistency
            # 'game_seconds_remaining' is already used as 'gameClock_seconds' in original plot_scores if needed directly, but we use game_seconds_elapsed
        }
    )

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

    if debug:
        print("\n--- DEBUG INFO: Data Distribution ---")
        print(f"Total plays for {target_game_id_str}: {len(df)}")

        # Check for NaNs in critical columns
        nan_counts = (
            df[
                [
                    "quarter",
                    "game_seconds_remaining",
                    "game_seconds_elapsed",
                    "expectedPoints",
                ]
            ]
            .isna()
            .sum()
        )
        if nan_counts.any():
            print("\nNaN Counts:")
            print(nan_counts[nan_counts > 0])

            if nan_counts["expectedPoints"] > 0:
                print("\nPlays with NaN expectedPoints:")
                nan_plays = df[df["expectedPoints"].isna()]
                print(
                    nan_plays[
                        ["quarter", "game_seconds_remaining", "possessionTeam", "desc"]
                    ].head(10)
                )

        # Summary by Quarter
        summary = df.groupby("quarter").agg(
            {
                "game_seconds_remaining": ["min", "max", "count"],
                "game_seconds_elapsed": ["min", "max"],
                "expectedPoints": ["min", "max", "mean"],
            }
        )
        print("\nQuarterly Summary:")
        print(summary)

        # Check for overlaps or gaps in game_seconds_elapsed
        print("\nQuarter Transitions (game_seconds_elapsed):")
        for q in sorted(df["quarter"].unique()):
            q_data = df[df["quarter"] == q]
            if not q_data.empty:
                start = q_data["game_seconds_elapsed"].iloc[0]
                end = q_data["game_seconds_elapsed"].iloc[-1]
                print(
                    f"Q{q}: Range [{start:7.1f}, {end:7.1f}], Duration: {abs(end-start):6.1f}s, Plays: {len(q_data):3d}"
                )

        print("\nSample Data (First 5 plays):")
        cols = [
            "quarter",
            "game_seconds_remaining",
            "game_seconds_elapsed",
            "possessionTeam",
            "expectedPoints",
            "home_expected",
            "visitor_expected",
        ]
        print(df[cols].head())

        print("\nSample Data (Last 5 plays):")
        print(df[cols].tail())
        print("\n--- END DEBUG INFO ---\n")

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
    # Top (ax1) is Net Difference (larger), Bottom (ax2) is Scores (smaller)
    _, (ax1, ax2) = plt.subplots(
        2, 1, figsize=(10, 7), sharex=True, gridspec_kw={"height_ratios": [3, 1]}
    )

    # --- Top Subplot: Net Difference (Winner is Positive) ---
    ax1.step(
        df["game_seconds_elapsed"],
        df["net_actual"],
        label="Actual Diff",
        where="post",
        color="black",
        alpha=0.2,
    )
    ax1.plot(
        df["game_seconds_elapsed"],
        df["net_expected"],
        label="Expected Diff",
        color="purple",
        linewidth=1.5,
    )

    ax1.fill_between(
        df["game_seconds_elapsed"],
        0,
        df["net_expected"],
        where=(df["net_expected"] >= 0),
        color=pos_color,
        alpha=0.2,
        label=f"{pos_team} Lead",
        interpolate=True,
    )
    ax1.fill_between(
        df["game_seconds_elapsed"],
        0,
        df["net_expected"],
        where=(df["net_expected"] < 0),
        color=neg_color,
        alpha=0.2,
        label=f"{neg_team} Lead",
        interpolate=True,
    )

    ax1.axhline(y=0, color="black", linestyle="-", linewidth=1.0)  # Baseline

    # Plot play-by-play points for hover on Net Difference (ax1)
    plays_with_ep = df.dropna(subset=["expectedPoints"]).copy()
    sc_net = ax1.scatter(
        plays_with_ep["game_seconds_elapsed"],
        plays_with_ep["net_expected"],
        color="purple",
        s=10,
        alpha=0.5,
        label="_nolegend_",
    )

    # Add hover functionality
    cursor = mplcursors.cursor(sc_net, hover=True)

    @cursor.connect("add")
    def on_add(sel):
        row = plays_with_ep.iloc[sel.index]
        ep_val = row["expectedPoints"]
        epa_val = row.get("expectedPointsAdded", 0.0)
        desc = row.get("desc", "No description")

        wrapped_desc = "\n".join(textwrap.wrap(str(desc), width=40))

        sel.annotation.set_text(
            f"EP: {ep_val:.2f}\n" f"EPA: {epa_val:.2f}\n" f"Play: {wrapped_desc}"
        )
        sel.annotation.get_bbox_patch().set(fc="white", alpha=0.9)

    ax1.set_title(
        f"Net Difference and Lead: {visitor_team_name} at {home_team_name} ({target_game_id_str})"
    )
    ax1.set_ylabel(f"Lead Magnitude\n({pos_team} Lead +)")
    ax1.legend(loc="upper right", fontsize="x-small")
    ax1.grid(True, linestyle="--", alpha=0.7)

    # --- Bottom Subplot: Scores ---
    ax2.step(
        df["game_seconds_elapsed"],
        df["preSnapHomeScore"],
        label=f"{home_team_name} Actual",
        where="post",
        color="blue",
        alpha=0.3,
    )
    ax2.step(
        df["game_seconds_elapsed"],
        df["preSnapVisitorScore"],
        label=f"{visitor_team_name} Actual",
        where="post",
        color="red",
        alpha=0.3,
    )

    ax2.plot(
        df["game_seconds_elapsed"],
        df["home_expected"],
        label=f"{home_team_name} Expected",
        color="blue",
        linewidth=2,
    )
    ax2.plot(
        df["game_seconds_elapsed"],
        df["visitor_expected"],
        label=f"{visitor_team_name} Expected",
        color="red",
        linewidth=2,
    )

    ax2.set_ylabel("Points")
    ax2.set_xlabel("Game Seconds Elapsed")
    ax2.legend()
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
    parser.add_argument(
        "game_id", type=str, help="The nflverse game ID (e.g., '2023_01_ARI_WAS')."
    )
    parser.add_argument(
        "-o",
        "--output",
        help="Path to save the output graph file (e.g., 'output.png'). "
        + "If not provided, the graph will be displayed.",
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable debug logging to investigate data distribution.",
    )

    args = parser.parse_args()
    game_id_str = args.game_id  # This is now expected to be a string
    output_arg = args.output
    debug_mode = args.debug

    # Determine season from game_id_str. This is used for signature compatibility
    # with load_game_info and load_plays_for_game, which now re-parse season internally.
    season = get_season_from_game_id(game_id_str)

    # Load game metadata
    # The 'season' parameter is passed for signature compatibility, but load_game_info
    # re-parses it from game_id_str internally.
    df_game = load_game_info(game_id_str, season)
    if df_game.empty:
        # load_game_info (via get_game_id_and_metadata) already prints specific errors/warnings.
        sys.exit(1)

    # Extract team names and final scores from game_info DataFrame
    # Use .iloc[0] as filter should return at most one row.
    try:
        home_team_name = df_game["home_team"].iloc[0]
        visitor_team_name = df_game["away_team"].iloc[0]
        home_final_score = df_game["home_score"].iloc[0]
        visitor_final_score = df_game["away_score"].iloc[0]
    except IndexError:
        print(
            "Error: Could not retrieve team names or scores from game info. Ensure game_id is correct and data is loaded."
        )
        sys.exit(1)
    except KeyError as e:
        print(f"Error: Missing expected column in game info: {e}")
        sys.exit(1)

    # Load plays for the game
    # The 'season' parameter is passed for signature compatibility, but load_plays_for_game
    # re-parses it from game_id_str internally.
    df_plays_pd = load_plays_for_game(game_id_str, season)
    if df_plays_pd.empty:
        # load_plays_for_game (via get_game_id_and_metadata) already prints specific errors/warnings.
        sys.exit(1)

    # Sort plays chronologically
    df_sorted = get_sorted_plays(df_plays_pd)

    # Generate Plot
    plot_scores(
        df_sorted,
        game_id_str,  # Pass the string game ID for display purposes
        home_team_name,
        visitor_team_name,
        home_final_score,
        visitor_final_score,
        output_path=output_arg,
        debug=debug_mode,
    )
