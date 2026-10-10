# Nightly Branch Bloom Pruner

This GitHub Action helps maintain a tidy repository by identifying and optionally pruning stale, unmerged branches. It acts as a digital gardener, ensuring your branch "garden" doesn't get overgrown with forgotten blooms.

## Features

*   **Stale Branch Detection**: Identifies branches that haven't had activity for a configurable number of days.
*   **Unmerged Check**: Ensures only branches *not* merged into the default branch are considered for pruning.
*   **Protected Branch Awareness**: Skips any protected branches, ensuring critical branches are safe.
*   **Dry Run Mode**: Allows you to preview which branches would be pruned without actually deleting them.
*   **Configurable**: Easily adjust stale days and the default branch name.

## Usage

To use the `Nightly Branch Bloom Pruner` in your workflow, add a step like this:

```yaml
name: Prune Stale Branches

on:
  schedule:
    - cron: '0 0 * * *' # Runs daily at midnight UTC
  workflow_dispatch: # Allows manual triggering

jobs:
  prune-branches:
    runs-on: ubuntu-latest
    permissions:
      contents: write # Required to delete branches
      pull-requests: read # Needed for some branch checks

    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Run Branch Bloom Pruner (Dry Run)
        id: dry_run_pruner
        uses: polsala/ApocalypsAI/utils/nightly-branch-bloom-pruner@main # Replace 'main' with your branch/tag
        with:
          github-token: ${{ secrets.GITHUB_TOKEN }}
          stale-days: '60' # Branches older than 60 days
          default-branch: 'main'
          dry-run: 'true' # Set to 'false' to actually delete branches

      - name: Report Dry Run Results
        if: steps.dry_run_pruner.outputs.pruned-branches != '[]'
        run: |
          echo "--- Branches that would be pruned (Dry Run) ---"
          echo "${{ steps.dry_run_pruner.outputs.pruned-branches }}" | jq .
          echo "-------------------------------------------------"
        shell: bash

      # Example of running with actual pruning (use with caution!)
      # - name: Run Branch Bloom Pruner (Actual Pruning)
      #   if: github.event_name == 'workflow_dispatch' # Only allow actual pruning via manual trigger
      #   uses: polsala/ApocalypsAI/utils/nightly-branch-bloom-pruner@main
      #   with:
      #     github-token: ${{ secrets.GITHUB_TOKEN }}
      #     stale-days: '90'
      #     default-branch: 'main'
      #     dry-run: 'false' # THIS WILL DELETE BRANCHES!

      # - name: Report Pruning Results
      #   if: steps.pruner.outputs.pruned-branches != '[]'
      #   run: |
      #     echo "--- Branches that were pruned ---"
      #     echo "${{ steps.pruner.outputs.pruned-branches }}" | jq .
      #     echo "---------------------------------"
      #   shell: bash
```
