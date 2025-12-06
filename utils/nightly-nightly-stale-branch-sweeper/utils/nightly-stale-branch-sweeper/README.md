# Nightly Stale Branch Sweeper

## Overview

The Nightly Stale Branch Sweeper is a vigilant utility designed to help maintain a tidy and efficient GitHub repository. It scans for branches that haven't seen activity in a specified number of days, flagging them as 'stale' and providing actionable suggestions for cleanup. This helps reduce repository clutter, improve developer focus, and potentially mitigate security risks from long-forgotten branches.

## Features

*   **Stale Branch Detection**: Identifies branches based on their last commit date.
*   **Configurable Stale Threshold**: Allows users to define what 'stale' means for their repository (e.g., 30, 60, 90 days).
*   **Clear Reporting**: Outputs a list of stale branches with their last activity date.
*   **GitHub API Integration**: Leverages the GitHub API to fetch branch information.

## Usage

To run the Stale Branch Sweeper, you'll need a GitHub Personal Access Token with `repo` scope (or `public_repo` for public repositories) set as an environment variable `GITHUB_TOKEN`.

```bash
python src/sweeper.py --repo <owner>/<repo_name> --stale-days <number_of_days>
```

**Example:**

```bash
export GITHUB_TOKEN="ghp_YOUR_TOKEN"
python src/sweeper.py --repo polsala/ApocalypsAI --stale-days 90
```

This will list all branches in `polsala/ApocalypsAI` that have not been updated in the last 90 days.

## Development

### Prerequisites

*   Python 3.11+
*   `requests` library (`pip install requests`)

### Running Tests

Tests are self-contained and use mocks to simulate GitHub API responses, ensuring deterministic and offline execution.

```bash
python -m unittest tests/test_sweeper.py
```
