# 🎶 Nightly Repo Rhythm Analyzer 🎶

## Unearthing the Pulse of Your Repository Before the Great Silence

The `Nightly Repo Rhythm Analyzer` is a whimsical-yet-useful utility designed to reveal the hidden activity patterns within your Git repository. Before the great silence, understand when your team is most active, when the code flows freely, and when the digital dust settles. This insight can help optimize CI/CD schedules, identify peak collaboration times, or simply satisfy your curiosity about your project's heartbeat.

## Features

*   Analyzes commit timestamps to determine activity by hour of day and day of week (UTC).
*   Provides a clear, human-readable report of peak and quiet periods.
*   Supports local repositories or cloning remote ones (requires `git` installed).

## Usage

### Prerequisites

*   Python 3.8+
*   `git` installed and accessible in your PATH.

### Running the Analyzer

1.  **Navigate to the utility directory:**
    ```bash
    cd utils/nightly-repo-rhythm-analyzer
    ```

2.  **Run the analyzer:**

    *   **For a local repository:**
        ```bash
        python src/analyzer.py --path /path/to/your/repo
        ```

    *   **For a remote repository (will clone temporarily):**
        ```bash
        python src/analyzer.py --repo-url https://github.com/polsala/ApocalypsAI.git
        ```

    *   **To specify a branch (default is `main`):**
        ```bash
        python src/analyzer.py --repo-url https://github.com/polsala/ApocalypsAI.git --branch develop
        ```

### Example Output

```
Repo Rhythm Analysis for: /path/to/your/repo

--- Activity by Hour of Day (UTC) ---
Hour 00:00-00:59: 5 commits (1.2%)
Hour 01:00-01:59: 12 commits (2.9%)
...
Hour 09:00-09:59: 85 commits (20.5%)  <-- Peak Activity!
...
Hour 23:00-23:59: 3 commits (0.7%)

Peak Activity Hour (UTC): 09:00-09:59 with 85 commits.

--- Activity by Day of Week (UTC) ---
Monday: 90 commits (21.7%)
Tuesday: 110 commits (26.5%) <-- Peak Activity!
Wednesday: 80 commits (19.3%)
Thursday: 70 commits (16.9%)
Friday: 50 commits (12.0%)
Saturday: 10 commits (2.4%)
Sunday: 5 commits (1.2%)

Peak Activity Day (UTC): Tuesday with 110 commits.

Total Commits Analyzed: 415
```

## Development

### Running Tests

```bash
python -m unittest tests/test_analyzer.py
```
