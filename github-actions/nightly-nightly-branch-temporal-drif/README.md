# Nightly Branch Temporal Drift Detector

This GitHub Action helps maintain a healthy repository by identifying and reporting branches that have not been updated within a specified 'stale' period. It's like a temporal anomaly detector for your codebase, ensuring no branch drifts too far into the past.

## Features

*   **Staleness Detection**: Configurable number of days after which a branch is considered stale.
*   **Branch Exclusion**: Ability to ignore critical branches (e.g., `main`, `master`, `develop`) from staleness checks.
*   **JSON Output**: Provides a JSON array of detected stale branch names for easy integration with other workflows.

## Usage

To use this action, add it as a step in your GitHub Actions workflow. It's recommended to run this on a schedule (e.g., nightly) or as part of a repository maintenance workflow.

```yaml
name: Detect Stale Branches Nightly

on:
  schedule:
    - cron: '0 0 * * *' # Run daily at midnight UTC
  workflow_dispatch: # Allow manual triggering

jobs:
  detect_drift:
    runs-on: ubuntu-latest
    steps:
      - name: Run Nightly Branch Temporal Drift Detector
        id: detect_stale_branches
        uses: polsala/ApocalypsAI/github-actions/nightly-branch-temporal-drift@main # Adjust path if needed
        with:
          stale-days: 60 # Branches older than 60 days are considered stale
          ignore-branches: "main,master,develop,release/*" # Comma-separated list of branches to ignore

      - name: Report Stale Branches
        if: steps.detect_stale_branches.outputs.stale-branches != '[]'
        run: |
          echo "The following branches have experienced significant temporal drift and are considered stale:"
          echo "${{ steps.detect_stale_branches.outputs.stale-branches }}"
          # Further actions could be taken here, e.g., opening an issue, sending a notification.

      - name: No Stale Branches Found
        if: steps.detect_stale_branches.outputs.stale-branches == '[]'
        run: |
          echo "All branches are temporally stable. No drift detected!"
```

## Inputs

*   `stale-days` (Required, Default: `30`):
    The number of days after which a branch is considered stale. Must be an integer.
*   `ignore-branches` (Optional, Default: `main,master,develop`):
    A comma-separated string of branch names (or glob patterns like `release/*`) to exclude from the staleness check. These branches will never be reported as stale.

## Outputs

*   `stale-branches`:
    A JSON array of the names of all detected stale branches. If no stale branches are found, it will be an empty JSON array (`[]`).

## How it Works

The action checks out the repository with full history (`fetch-depth: 0`), then iterates through all remote branches. For each branch, it retrieves the timestamp of the last commit. This timestamp is compared against a calculated threshold based on the `stale-days` input. Branches older than this threshold (and not in the `ignore-branches` list) are collected and output as a JSON array.

It uses standard `git` commands and `jq` for JSON processing, which are typically available on GitHub Actions runners.
