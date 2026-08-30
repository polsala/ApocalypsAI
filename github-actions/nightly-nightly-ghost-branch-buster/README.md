# Nightly Ghost Branch Buster

## 👻 Hunt Down Those Forgotten Branches! 👻

The `nightly-ghost-branch-buster` is a GitHub Action designed to help you maintain a clean and tidy repository by identifying and optionally deleting 'ghost branches' – those forgotten branches that haven't seen any activity in a while.

Keep your repository lean, mean, and free of spectral code remnants!

## ✨ Features

-   **Stale Branch Detection**: Configurable threshold for what constitutes a 'stale' branch.
-   **Exemption List**: Specify branches (e.g., `main`, `develop`) that should never be considered stale.
-   **Dry Run Mode**: Safely preview which branches would be affected without making any changes.
-   **Automated Deletion**: Optionally delete stale branches directly.
-   **Issue Reporting**: Automatically create a GitHub Issue to report identified stale branches, with custom labels and titles.

## 🚀 Usage

To use the Ghost Branch Buster, add a new workflow file (e.g., `.github/workflows/ghost-buster.yml`) to your repository:

```yaml
name: 'Ghost Branch Buster Daily Scan'

on:
  workflow_dispatch: # Allows manual triggering
  schedule:
    - cron: '0 0 * * *' # Runs daily at midnight UTC

jobs:
  bust-ghost-branches:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      issues: write # Required to create issues
      pull-requests: write # Required to delete branches (via git ref delete)

    steps:
      - name: Bust Ghost Branches (Dry Run)
        uses: polsala/ApocalypsAI/nightly-ghost-branch-buster@main # Replace 'main' with your branch/tag if needed
        id: dry_run_buster
        with:
          repo-token: ${{ secrets.GITHUB_TOKEN }}
          stale-days: 90 # Branches older than 90 days are considered stale
          exempt-branches: 'main,master,develop'
          dry-run: true # Set to 'false' to enable deletion
          delete-stale: false # Set to 'true' to enable deletion (only if dry-run is false)
          issue-label: 'stale-branches'
          issue-title: 'Daily Stale Branch Report'

      - name: Output Dry Run Results
        if: steps.dry_run_buster.outputs.stale-branches-count > 0
        run: |
          echo "Found ${{ steps.dry_run_buster.outputs.stale-branches-count }} stale branches:"
          echo "${{ steps.dry_run_buster.outputs.stale-branches-list }}"

      # Example of a separate job or step for actual deletion (use with caution!)
      # - name: Bust Ghost Branches (Actual Deletion)
      #   if: github.event_name == 'workflow_dispatch' && github.event.inputs.delete_confirm == 'true'
      #   uses: polsala/ApocalypsAI/nightly-ghost-branch-buster@main
      #   with:
      #     repo-token: ${{ secrets.GITHUB_TOKEN }}
      #     stale-days: 180
      #     exempt-branches: 'main,master,develop'
      #     dry-run: false
      #     delete-stale: true
      #     issue-label: 'branch-cleanup-completed'
      #     issue-title: 'Stale Branches Cleaned Up'
```

## ⚙️ Inputs

| Input Name        | Description                                                                                             | Required | Default Value           |
| :---------------- | :------------------------------------------------------------------------------------------------------ | :------- | :---------------------- |
| `repo-token`      | GitHub token with permissions to read branches, delete refs, and create issues.                           | `true`   |                         |
| `stale-days`      | Number of days after which a branch is considered stale.                                                | `true`   | `90`                    |
| `exempt-branches` | Comma-separated list of branch names to exempt from being considered stale (e.g., `main, develop`).       | `false`  | `main,master,develop,dev` |
| `dry-run`         | If `true`, only reports stale branches without deleting them.                                           | `false`  | `true`                  |
| `delete-stale`    | If `true` and `dry-run` is `false`, deletes identified stale branches.                                  | `false`  | `false`                 |
| `issue-label`     | Optional label to add to the issue created for stale branches.                                          | `false`  |                         |
| `issue-title`     | Optional title for the issue created for stale branches. Defaults to "Stale Branches Detected".         | `false`  | `Stale Branches Detected` |

## 📤 Outputs

| Output Name           | Description                                     |
| :-------------------- | :---------------------------------------------- |
| `stale-branches-count`| The number of stale branches found.             |
| `deleted-branches-count`| The number of branches deleted.               |
| `stale-branches-list` | A JSON array of the names of stale branches.    |

## ⚠️ Permissions

This action requires the following permissions in your workflow:

```yaml
permissions:
  contents: read
  issues: write # To create issues for reporting
  pull-requests: write # To delete branches (via git ref delete)
```

Ensure your `repo-token` has these permissions, especially `pull-requests: write` for deletion functionality.
