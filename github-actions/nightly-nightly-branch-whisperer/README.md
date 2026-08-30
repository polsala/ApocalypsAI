# Nightly Branch Whisperer

A GitHub Action that gently nudges forgotten branches from their slumber, identifying those that haven't seen activity in a while and offering whimsical suggestions for their fate. It reports on stale branches without taking any destructive actions.

## 🌟 Features

*   **Staleness Detection**: Configurable number of days to consider a branch "stale."
*   **Exclusion List**: Ignore important branches (e.g., `main`, `develop`, `release/*`) from the check.
*   **Whimsical Suggestions**: Provides lighthearted advice for each stale branch.
*   **Non-Destructive**: Only reports; never deletes or modifies branches.
*   **Markdown Report**: Generates a formatted report suitable for issue comments or PR descriptions.

## 🚀 Usage

To use the Nightly Branch Whisperer, add it to your GitHub Actions workflow. It's recommended to run this on a schedule (e.g., nightly or weekly) or as part of a larger monitoring workflow.

```yaml
name: Stale Branch Check

on:
  schedule:
    - cron: '0 0 * * 1' # Run every Monday at midnight UTC
  workflow_dispatch: # Allow manual triggering

jobs:
  check-stale-branches:
    runs-on: ubuntu-latest
    permissions:
      contents: read # Required for actions/checkout
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4
        with:
          fetch-depth: 0 # Important: Fetch all history for accurate git commit dates

      - name: Run Nightly Branch Whisperer
        id: branch-whisperer
        uses: polsala/ApocalypsAI/github-actions/nightly-branch-whisperer@main # Replace 'main' with your branch/tag
        with:
          stale-days: '90' # Branches older than 90 days are considered stale
          exclude-branches: 'main,master,develop,release/*' # Comma-separated list
          repo-token: ${{ secrets.GITHUB_TOKEN }}

      - name: Output Stale Branches Report
        run: |
          echo "Found ${{ steps.branch-whisperer.outputs.stale-branches-count }} stale branches."
          echo "${{ steps.branch-whisperer.outputs.stale-branches-report }}" >> $GITHUB_STEP_SUMMARY
          # You could also create an issue or comment on a discussion with the report
          # For example, using `peter-evans/create-or-update-issue-comment@v3`
```

## ⚙️ Inputs

| Name             | Description                                                                 | Type   | Default                 | Required |
| :--------------- | :-------------------------------------------------------------------------- | :----- | :---------------------- | :------- |
| `stale-days`     | Number of days after which a branch is considered stale.                    | `string` | `'90'`                  | `false`  |
| `repo-token`     | GitHub token for API access. Usually `${{ github.token }}`.                 | `string` | `${{ github.token }}`   | `true`   |
| `exclude-branches` | Comma-separated list of branch names to exclude from the staleness check. | `string` | `'main,master,develop'` | `false`  |

## 📤 Outputs

| Name                    | Description                                                                 | Type   |
| :---------------------- | :-------------------------------------------------------------------------- | :----- |
| `stale-branches-count`  | The number of stale branches found.                                         | `string` |
| `stale-branches-report` | A markdown-formatted report of stale branches and whimsical suggestions.    | `string` |

## 🧪 Testing

The action includes a `tests/test_branch_whisperer.sh` script that uses mocked `date` and `git` commands to ensure deterministic and offline testing.

To run tests:

```bash
cd github-actions/nightly-branch-whisperer
bash tests/test_branch_whisperer.sh
```

The tests simulate different scenarios, including no stale branches, some stale branches, and branches excluded from the check.
