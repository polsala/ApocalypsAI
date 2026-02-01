# Nightly Branch Tombstone Marker

This GitHub Action helps maintain a clean repository by identifying and listing branches that have not been updated for a specified period, effectively marking them as 'stale' or 'forgotten'. It's a gentle nudge towards tidying up your branch graveyard.

## Features

*   **Staleness Detection**: Configurable threshold for what constitutes a 'stale' branch.
*   **Exclusion List**: Skip important branches (e.g., `main`, `master`, `develop`) from the staleness check.
*   **Output**: Provides a comma-separated list of identified stale branches.

## Usage

To use this action, add a step to your GitHub Actions workflow:

```yaml
name: Find Stale Branches
on:
  schedule:
    - cron: '0 0 * * *' # Runs daily at midnight UTC
  workflow_dispatch:

jobs:
  identify-stale-branches:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4
        # Fetch all branches to ensure accurate staleness detection
        with:
          fetch-depth: 0

      - name: Run Branch Tombstone Marker
        id: tombstone_marker
        uses: polsala/ApocalypsAI/nightly-branch-tombstone-marker@main # Replace 'main' with your branch/tag if needed
        with:
          stale-days: '60' # Branches older than 60 days are considered stale
          exclude-branches: 'main,master,develop,release/*' # Comma-separated list of branches to ignore

      - name: Process Stale Branches
        if: steps.tombstone_marker.outputs.stale-branches != ''
        run: |
          echo "The following branches are stale: ${{ steps.tombstone_marker.outputs.stale-branches }}"
          # Further actions could be taken here, e.g., opening an issue, sending a notification,
          # or even initiating a branch deletion process (use with caution!)
          # For example, to delete:
          # echo "Deleting stale branches..."
          # IFS=',' read -r -a STALE_BRANCHES_ARRAY <<< "${{ steps.tombstone_marker.outputs.stale-branches }}"
          # for branch in "${STALE_BRANCHES_ARRAY[@]}"; do
          #   echo "Deleting branch: $branch"
          #   git push origin --delete "$branch"
          # done
```

### Inputs

*   `stale-days` (optional, default: `30`):
    The number of days after which a branch is considered stale. Branches with their last commit older than this threshold will be identified.

*   `exclude-branches` (optional, default: `main,master`):
    A comma-separated string of branch names or patterns (e.g., `release/*`) to exclude from the staleness check. These branches will never be marked as stale, regardless of their age.

### Outputs

*   `stale-branches`:
    A comma-separated string of branch names that have been identified as stale. If no stale branches are found, this output will be empty.
