# 2026 NFL Draft Consensus Board

This project provides an interactive, data-driven visualization of 2026 NFL Mock Draft projections from 10 high-authority experts. It is designed to reveal "Draft Locks" vs. "Draft Chaos" by mapping expert consensus across specific draft slots.

## Core Components

### 1. Data Engine (`src/mock_draft_data.py`)
- **Metadata Registry**: Tracks 10 experts (Daniel Jeremiah, Bucky Brooks, Jordan Reid, Danny Kelly, Field Yates, Dane Brugler, Trevor Sikkema, Ryan Wilson, Diante Lee, and The Athletic Beat Writers).
- **Consolidated Dataset**: A verified list of the Top 15 picks, including player names, positions, and teams.
- **Trade Logic**: Tracks projected trades (e.g., Buffalo at #3) using a comparison between the "Default Order" and mocked team selections.

### 2. Visualization Engine (`src/plot_mocks.py`)
- **Median-Sorted Board**: Players are ordered on the X-axis by their median projected draft slot, creating a clean trend line.
- **Team-Colored Interactivity**: Squares are filled with official primary team colors (via `nflreadpy`).
- **Visual Signals**:
    - **Square Size**: Reflects the number of experts projecting that pairing.
    - **Borders**: Thick black borders signify a "Lock" (7+ experts).
    - **Dotted Borders**: Signify a projected trade-up for that pick.
- **Interactive Tooltips**: Hovering provides a date-sorted list of every expert who made that pick.

### 3. Monitoring Utility (`src/scout.py`)
- **Watchdog**: Scans the 10 source URLs for the keyword "Mock" and checks for page changes to notify when local metadata needs updating.

---

## Technical Challenges & Data Integrity Notes

During the development of the Top 15 board, several critical data integrity issues were identified and resolved. These serve as a reference for future round expansions:

### 1. The "Batch Update" Truncation
- **Issue**: During a batch update to add new experts, several draft slots (specifically Picks 4–11 and 14–15) were accidentally truncated in the source code, leaving only 2 of 10 experts represented.
- **Resolution**: A full manual scrub was performed to restore all 150 data points, ensuring the consensus calculation (the number inside the squares) was mathematically accurate.

### 2. Diante Lee Discrepancies (The Ringer)
- **Issue**: Initial metadata placed Jeremiyah Love (RB) at Pick #9. However, the user identified that in the live "Deep Dive" view, Love was projected at Pick #7.
- **Findings**: Source sites like *The Ringer* often provide two different views: a "Summary Table" and a "Deep Dive/Fit Analysis." Initial automated scrapes/reads pulled from analytical text where Lee discussed Love's *fit* at #9, rather than his *official mock slot*.
- **Correction**: Metadata was locked to the **Official Mock Draft Order** (Styles at #7, Love at #8) to maintain board consistency.

### 3. Source Overlap (ESPN/Athletic)
- **Issue**: Multiple authors from the same source (e.g., Reid and Yates at ESPN) often share similar URLs or profile pages. 
- **Resolution**: The `scout.py` utility and the metadata registry were updated to use specific author-level sub-pages to ensure the most recent unique mock for each individual was being tracked.

---

## Usage Instructions

### View the Interactive Board
```bash
python3 src/plot_mocks.py
```
*Note: This will generate `draft_consensus_2026.html` and automatically open it in your default browser.*

### Check for Expert Updates
```bash
python3 src/scout.py
```

### Data Sources
Full references and publication dates are maintained in the interactive footer of the generated graph and in `src/mock_draft_data.py`.
