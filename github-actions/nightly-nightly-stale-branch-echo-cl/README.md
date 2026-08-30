# Nightly Stale Branch Echo Cleaner

This GitHub Action helps maintain repository hygiene by identifying and optionally cleaning up stale branches. It prevents "temporal echoes" of old, unused development lines from cluttering your repository, making navigation and management easier.

## Features

*   **Stale Branch Detection**: Configurable `stale_days` to define what constitutes a stale branch.
*   **Exclusion List**: Specify branches (e.g., `main`, `develop`, `release/*`) to always exclude from cleanup.
*   **Flexible Actions**: Choose to merely log stale branches, create GitHub Issues for them, or directly delete them.
*   **Dry Run Mode**: Safely test the action without performing any destructive operations.
*   **Outputs**: Provides a list of found stale branches and the total number of branches processed.

## Usage

To use this action, add it to one of your repository's workflows. It's recommended to run this action on a schedule or via `workflow_dispatch` for manual triggers.

```yaml
name: Stale Branch Cleanup

on:
  schedule:
    - cron: '0 0 * * *' # Daily at midnight UTC
  workflow_dispatch:
    inputs:
      dry_run_input:
        description: 'Run in dry-run mode?'
        required: false
        default: 'true'
        type: boolean
      action_type_input:
        description: 'Action to perform: log, issue, or delete'
        required: false
        default: 'log'
        type: choice
        options:
          - log
          - issue
          - delete

jobs:
  clean_stale_branches:
    runs-on: ubuntu-latest
    permissions:
      contents: write # Required for deleting branches
      issues: write   # Required for creating issues
      pull-requests: write # Required for creating issues (if linked to PRs)
    steps:
      - name: Run Stale Branch Echo Cleaner
        uses: polsala/ApocalypsAI/github-actions/nightly-stale-branch-echo-cleaner@main # Adjust to your repo path and branch
        id: cleaner
        with:
          stale_days: 60
          dry_run: ${{ github.event.inputs.dry_run_input || 'true' }}
          exclude_branches: main,develop,release/*
          action_type: ${{ github.event.inputs.action_type_input || 'log' }}
          issue_labels: stale-branch,cleanup-required
          github_token: ${{ secrets.GITHUB_TOKEN }}

      - name: Report Results
        run: |
          echo "Action completed. Found ${{ steps.cleaner.outputs.stale_branches_found }} stale branches."
          echo "Processed ${{ steps.cleaner.outputs.branches_processed }} branches."
```

## Inputs

| Name             | Description                                                               | Required | Default             |
| :--------------- | :------------------------------------------------------------------------ | :------- | :------------------ |
| `stale_days`     | Number of days after which a branch is considered stale.                  | `true`   | `30`                |
| `dry_run`        | If `true`, only logs actions without performing them.                     | `false`  | `true`              |
| `exclude_branches` | Comma-separated list of branch names to exclude from cleaning (e.g., `main`, `develop`, `feature/*`). | `false`  | `main,develop`      |
| `action_type`    | Action to perform on stale branches: `log` (default), `delete`, `issue`.  | `false`  | `log`               |
| `issue_labels`   | Comma-separated labels to add to issues created for stale branches.        | `false`  | `stale,cleanup`     |
| `github_token`   | GitHub token for API access. Usually `${{ secrets.GITHUB_TOKEN }}`.       | `true`   |                     |

## Outputs

| Name                   | Description                                  |
| :--------------------- | :------------------------------------------- |
| `stale_branches_found` | JSON array of stale branch names found.      |
| `branches_processed`   | Count of branches processed by the action.   |

## Permissions

This action requires specific permissions based on the `action_type` chosen:

*   `contents: write`: Required if `action_type` is `delete`.
*   `issues: write`: Required if `action_type` is `issue`.
*   `pull-requests: write`: May be required if `action_type` is `issue` and the issue creation involves linking to PRs (though not explicitly done by this action, it's good practice for issue-related actions).

Ensure your workflow's `permissions` block is configured correctly.
