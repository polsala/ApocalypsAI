# Workflow Prognosticator

## Overview

The `workflow-prognosticator` is a command-line utility designed to bring a touch of apocalyptic whimsy to your GitHub Actions workflow monitoring. It connects to the GitHub API, fetches the recent run history for your workflows, and provides a 'prognosis' on their health. Is your workflow a beacon of stability, or is it teetering on the brink of digital collapse?

This tool is perfect for quickly assessing the operational status of your automation, identifying flaky workflows, or simply adding a bit of fun to your daily development routine.

## Features

*   **Workflow Health Prognosis**: Get a clear, color-coded (in your terminal) assessment of your workflows' stability.
*   **Recent Run Summary**: See the number of successful, failed, and total runs for a quick overview.
*   **Targeted or Broad Analysis**: Check a specific workflow by ID/name or get a prognosis for all workflows in a repository.
*   **Self-contained**: Written in Python 3.11 with minimal dependencies (`requests`).

## Installation

No installation steps are required beyond having Python 3.11 installed. The utility is self-contained within its `src/` directory.

## Usage

To use the `workflow-prognosticator`, you need a GitHub Personal Access Token with `repo` scope (or `workflow` scope for private repositories) exported as an environment variable named `GITHUB_TOKEN`.

```bash
export GITHUB_TOKEN="YOUR_GITHUB_PAT"

# Check a specific workflow by name or ID
python utils/workflow-prognosticator/src/prognosticator.py --repo octocat/Spoon-Knife --workflow "CI"

# Check all workflows in a repository
python utils/workflow-prognosticator/src/prognosticator.py --repo octocat/Spoon-Knife
```

### Arguments

*   `--repo <owner/name>` (Required): The GitHub repository (e.g., `octocat/Spoon-Knife`).
*   `--workflow <id_or_name>` (Optional): The name or ID of a specific workflow to analyze. If omitted, all active workflows in the repository will be analyzed.

## Example Output

```
--- Workflow: CI (ID: 12345) ---
  Recent Runs: 10 total, 10 successful, 0 failed
  Prognosis: Excellent! This workflow is a beacon of stability, ready to weather any digital apocalypse!

--- Workflow: Deploy (ID: 67890) ---
  Recent Runs: 10 total, 6 successful, 4 failed
  Prognosis: Unstable. This workflow is showing signs of digital fatigue. Intervention might be required.

--- Workflow: Documentation (ID: 11223) ---
  Recent Runs: 0 total, 0 successful, 0 failed
  Prognosis: No recent activity. No recent runs detected. Is it hibernating for the end times?
```

## Development

To run tests, navigate to the `utils/workflow-prognosticator` directory and execute:

```bash
python -m unittest tests/test_prognosticator.py
```
