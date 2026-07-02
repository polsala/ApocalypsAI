# Nightly Branch Archivist

A GitHub Action that helps maintain repository hygiene by identifying and reporting on stale branches. It's time to throw a 'Branch Retirement Party' for those long-forgotten branches!

## Features

*   **Stale Branch Detection**: Configurable threshold for what constitutes a 'stale' branch.
*   **Protected Branch Exclusion**: Automatically ignores specified critical branches (e.g., `main`, `develop`) using glob patterns.
*   **Whimsical Reporting**: Provides a fun, yet informative, summary of branches ready for archiving or deletion.
*   **Action Outputs**: Provides JSON and count of stale branches for further automation.

## Usage

To use this action, add a step to your GitHub Actions workflow. It's recommended to run this on a schedule (e.g., nightly or weekly).

```yaml
name: Branch Cleanup Check

on:
  schedule:
    - cron: '0 0 * * *' # Run daily at midnight UTC
  workflow_dispatch: # Allows manual triggering

jobs:
  check-stale-branches:
    runs-on: ubuntu-latest
    steps:
      - name: Find Stale Branches
        uses: polsala/ApocalypsAI/utils/nightly-branch-archivist@main # Replace 'main' with your branch if testing
        id: archivist
        with:
          repo-token: ${{ secrets.GITHUB_TOKEN }}
          stale-days: 90 # Branches not updated in 90 days are considered stale
          protected-branches: 'main,master,develop,release/*,hotfix/*'

      - name: Report Stale Branches
        if: steps.archivist.outputs.stale-branches-count > 0
        run: |
          echo "🎉 Branch Retirement Party Alert! 🎉"
          echo "The Nightly Branch Archivist has found ${{ steps.archivist.outputs.stale-branches-count }} branches that are ready for their grand send-off."
          echo "Details:"
          echo "${{ steps.archivist.outputs.stale-branches-message }}"
          echo "Stale branches (JSON): ${{ steps.archivist.outputs.stale-branches-json }}"

      - name: No Stale Branches Found
        if: steps.archivist.outputs.stale-branches-count == 0
        run: |
          echo "✨ All branches are fresh and lively! No retirement parties needed today. ✨"
```

## Inputs

*   `repo-token` (required):
    The GitHub token used to authenticate API requests. Typically `${{ secrets.GITHUB_TOKEN }}`. This token needs `contents: read` permission.
*   `stale-days` (optional, default: `90`):
    The number of days after which a branch is considered stale if it has no new commits.
*   `protected-branches` (optional, default: `main,master,develop`):
    A comma-separated string of branch names or glob patterns (e.g., `release/*`, `feature-*`) to exclude from stale branch detection. These branches will always be ignored.

## Outputs

*   `stale-branches-json`:
    A JSON array string of the names of all identified stale branches.
*   `stale-branches-count`:
    The total number of stale branches found.
*   `stale-branches-message`:
    A human-readable, whimsical message detailing the stale branches.

## Development

This action is written in JavaScript and uses `@actions/core`, `@actions/github`, and `minimatch` for GitHub API interaction and pattern matching. For local development or bundling, `npm install` and `ncc build` would typically be used.
