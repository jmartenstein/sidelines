# Future CLI Specification: `sidelines`

This document outlines the proposed Command-Line Interface (CLI) for the `sidelines` NFL Statistics & Simulation Suite. It serves as a blueprint for consolidating existing analysis scripts and implementing a new Monte Carlo simulation engine.

## User Requirements

The CLI must support the following core capabilities:
1.  **Historical Analysis (Visual):** View the `score_over_time` plot of an existing NFL game.
2.  **Historical Analysis (Text):** View the play-by-play text output of an existing NFL game.
3.  **Historical Analysis (Text):** List the game id's for a team in a single season
4.  **Simulation Statistics:** Gather aggregate statistics (win probability, score distributions) from 100+ Monte Carlo simulations.
5.  **Simulation Inspection:** Read detailed play-by-play data for a specific iteration within a Monte Carlo batch.

---

## Proposed Interface: `sidelines`

The interface follows a **Verb-Action Architecture**, prioritizing clear intent: find discovery (`find`), view facts (`view`), and model theories (`sim`).

**Global Flags:**
*   `--format <type>`, `-f <type>`: Sets the output format. Options: `text` (default), `plot`, `json`, `csv`.
*   `--debug`: Enables detailed logging of data distribution and API calls.

### 1. The `find` Subcommand
Discovers historical game IDs for a specific team and season.

**Usage:**
```bash
sidelines find <team> <season> [flags]
```

**Positional Arguments:**
*   `<team>`: The 3-letter team abbreviation (e.g., `KC`).
*   `<season>`: The NFL season year (e.g., `2023`).

**Examples:**
```bash
# List all games for the Kansas City Chiefs in 2023
sidelines find KC 2023
```

### 2. The `view` Subcommand
Analyzes what **actually happened** in a specific historical game.

**Usage:**
```bash
sidelines view <game_id> [flags]
```

**Flags:**
*   `--output`, `-o <path>`: Saves the generated output (e.g., a `.png` plot or `.json` file) to a specific path.

**Examples:**
```bash
# View text play-by-play (default format)
sidelines view 2023_01_DET_KC

# View graphical plot
sidelines view 2023_01_DET_KC --format plot
```

### 3. The `sim` Subcommand
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
*   `--seed <int>`: Sets a random seed for reproducibility.

**Examples:**
```bash
# Run 500 simulations with an injury scenario
sidelines sim 2023_01_DET_KC -n 500 --modify "injure:Mahomes_P"

# View the simulation cone plot
sidelines sim 2023_01_DET_KC --format plot
```

---

## Benefits & Challenges

### Key Benefits
1.  **Intent-Based Design:** The "Find → View → Sim" progression creates a natural workflow for the user.
2.  **Positional Simplicity:** `find` is now extremely fast to type for the most common use case.
3.  **Consistent Presentation:** The global `--format` flag ensures that switching between text, plots, and data exports works identically across all subcommands.
4.  **Shared Infrastructure:** All subcommands leverage the same data-fetching layer (DuckDB/Parquet) and Team Registry, ensuring high performance and data consistency.

### Technical Challenges
1.  **Format Handling Logic:** Each subcommand must implement a handler for the global `--format` flag, even if certain formats (like `plot` for `find`) are not yet supported.
2.  **Data Fetching Efficiency:** `nflreadpy.load_pbp` loads an entire season of data. For `find`, it is critical to use `load_schedules` to maintain responsiveness.
3.  **State Persistence:** Inspecting a specific simulation (`--inspect`) requires either saving massive amounts of temporary data or using strictly deterministic seeds to "re-play" a specific run on demand.
4.  **Visualization Ambiguity:** The `plot` format produces different types of charts in `view` vs. `sim`. Developers must ensure the visual language (colors, legends) remains consistent and clearly labeled to avoid confusion.

---

## Future Iterations
*   **Interactive Selection:** After running `list`, allow users to pick a game by number or interactive prompt to see the plot.
*   **Shell Completion:** Provide auto-completion for team abbreviations (`KC`, `DET`) and game IDs to speed up usage.
*   **Interactive Referencing:** Enable `view` and `sim` to reference previous `find` results by numeric index (e.g., `view 1`) using a local state file or session history.
*   **Interactive Mode:** Consider a REPL or interactive prompt for building complex roster modifications.
*   **Export Formats:** Add `--json` or `--csv` flags to `sim` to allow external tools (Excel, Tableau) to ingest simulation results.
