# Future CLI Specification: `sidelines`

This document outlines the proposed Command-Line Interface (CLI) for the `sidelines` NFL Statistics & Simulation Suite. It serves as a blueprint for consolidating existing analysis scripts and implementing a new Monte Carlo simulation engine.

## User Requirements

The CLI must support the following core capabilities:
1.  **Historical Analysis (Visual):** View the `score_over_time` plot of an existing NFL game.
2.  **Historical Analysis (Text):** View the play-by-play text output of an existing NFL game.
3.  **Simulation Statistics:** Gather aggregate statistics (win probability, score distributions) from 100+ Monte Carlo simulations.
4.  **Roster Modifications:** Run simulations with modified rosters (e.g., simulating the impact of an injury or a mid-season trade).
5.  **Simulation Inspection:** Read detailed play-by-play data for a specific iteration within a Monte Carlo batch.

---

## Proposed Interface: `sidelines`

The interface follows a **Two-Pillar Architecture**, separating "Historical Truth" (`game`) from "Predictive Modeling" (`sim`).

### 1. The `game` Subcommand
Analyzes what **actually happened** in a historical game. Consolidates `play_by_play.py` and `score_over_time.py`.

**Usage:**
```bash
sidelines game <game_id> [flags]
```

**Flags:**
*   `--plot`, `-p`: Toggles from the default text-based play-by-play to a graphical score progression plot.
*   `--output`, `-o <path>`: Saves the generated plot to a specific file (e.g., `graph.png`).
*   `--debug`: Enables detailed logging of data distribution and API calls.

**Examples:**
```bash
# View text play-by-play
sidelines game 2023_01_DET_KC

# View graphical plot
sidelines game 2023_01_DET_KC --plot
```

### 2. The `sim` Subcommand
Models what **could have happened** using a Monte Carlo engine.

**Usage:**
```bash
sidelines sim <game_id> [flags]
```

**Flags:**
*   `--iterations`, `-n <int>`: Number of Monte Carlo runs to execute (Default: 100).
*   `--modify <action:player_id>`: Applies a roster modification. Can be used multiple times.
    *   `injure:Mahomes_P`: Removes a player from the active roster.
    *   `trade:Jefferson_J`: Adds a player from another team to the current roster.
*   `--inspect <index>`: Displays the full text-based play-by-play for a specific simulation run (e.g., iteration #42).
*   `--plot`: Generates a "simulation cone" plot showing the range of possible score outcomes vs. the actual game.
*   `--seed <int>`: Sets a random seed for reproducibility.

**Examples:**
```bash
# Run 500 simulations with an injury scenario
sidelines sim 2023_01_DET_KC -n 500 --modify "injure:Mahomes_P"

# Inspect the PBP of the 10th simulation run
sidelines sim 2023_01_DET_KC --inspect 10
```

---

## Benefits & Challenges

### Key Benefits
1.  **Logical Separation:** Creates a clear mental model: `game` for facts, `sim` for theories.
2.  **Shared Infrastructure:** Both commands leverage the same data-fetching layer (DuckDB/Parquet) and Team Registry, ensuring high performance and data consistency.
3.  **Extensible "What-If" Logic:** The `--modify` flag allows for complex scenario testing without cluttering the basic analysis commands.
4.  **High Discoverability:** New users can explore capabilities via `sidelines --help` and drill down into advanced simulation flags as needed.

### Technical Challenges
1.  **State Persistence:** Inspecting a specific simulation (`--inspect`) requires either saving massive amounts of temporary data or using strictly deterministic seeds to "re-play" a specific run on demand.
2.  **Modification Syntax:** Defining a robust, string-based syntax for roster changes (`--modify "action:id"`) is difficult to make intuitive without a GUI.
3.  **Visualization Ambiguity:** The `--plot` flag produces different types of charts in `game` vs. `sim`. Developers must ensure the visual language (colors, legends) remains consistent and clearly labeled to avoid confusion.
4.  **Roster Data Integrity:** Accurate "What-If" simulations depend on high-quality player-level stats and depth charts, which adds a dependency on `nflreadpy.load_rosters`.

---

## Future Iterations
*   **Interactive Mode:** Consider a REPL or interactive prompt for building complex roster modifications.
*   **Export Formats:** Add `--json` or `--csv` flags to `sim` to allow external tools (Excel, Tableau) to ingest simulation results.
