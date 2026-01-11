# Nightly Stale Branch Whisperer

A GitHub Action that identifies branches in your repository that haven't been updated or merged into the default branch for a configurable period, and gently reminds maintainers by creating a GitHub Issue. Keep your repository tidy and focused!

## ✨ Features

*   **Stale Branch Detection**: Flags branches based on their last commit date.
*   **Merged Branch Awareness**: Skips branches that have already been merged into the default branch, even if they are old.
*   **Configurable Stale Threshold**: Define what "stale" means for your repository.
*   **Branch Exclusion**: Ignore specific branches or patterns (e.g., `dev`, `release-*`).
*   **Dry Run Mode**: Test the action without creating actual issues.
*   **Whimsical Reminders**: Creates a friendly issue to prompt cleanup.

## 🚀 Usage

To use the Stale Branch Whisperer, add it as a step in one of your GitHub Actions workflows. It's recommended to run this on a schedule, for example, weekly or monthly.

```yaml
name: Stale Branch Cleanup

on:
  schedule:
    - cron: '0 0 * * 0' # Run every Sunday at midnight UTC
  workflow_dispatch: # Allow manual triggering

jobs:
  whisper_stale_branches:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      issues: write # Required to create issues
      pull-requests: read # Required to check for merged PRs

    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Run Stale Branch Whisperer
        uses: polsala/ApocalypsAI/nightly-stale-branch-whisperer@main # Replace 'main' with your branch/tag if needed
        with:
          github-token: ${{ secrets.GITHUB_TOKEN }}
          stale-days: '60' # Consider branches stale after 60 days
          default-branch: 'main'
          issue-label: 'repository-maintenance'
          exclude-branches: 'develop,feature/long-term-.*' # Exclude 'develop' and branches starting with 'feature/long-term-'
          dry-run: 'false' # Set to 'true' to only log without creating issues
```

### Inputs

| Name               | Description                                                                                             | Required | Default              |
| :----------------- | :------------------------------------------------------------------------------------------------------ | :------- | :------------------- |
| `github-token`     | **Required.** GitHub token with `issues:write` and `pull-requests:read` permissions. Use `secrets.GITHUB_TOKEN`. | `true`   |                      |
| `stale-days`       | Number of days after which a branch is considered stale.                                                | `false`  | `30`                 |
| `default-branch`   | The main branch to compare against (e.g., `main`, `master`).                                            | `false`  | `main`               |
| `issue-label`      | Label to add to the created issue for stale branches.                                                   | `false`  | `stale-branch`       |
| `dry-run`          | If `'true'`, only logs stale branches, does not create issues.                                          | `false`  | `false`              |
| `exclude-branches` | Comma-separated list of branch names or regex patterns to exclude from checks (e.g., `"dev,release-.*"`). | `false`  | `''`                 |

### Outputs

| Name                  | Description                                 |
| :-------------------- | :------------------------------------------ |
| `stale-branches-count` | The number of stale branches found.         |
| `stale-branches-list`  | A JSON array of stale branch names.         |

## 🧪 Development & Testing

The action's logic is implemented in `src/main.js`. Unit tests are provided in `tests/test.js` using Jest.

To run tests locally:

1.  Navigate to the `nightly-stale-branch-whisperer` directory.
2.  Install dependencies: `npm install`
3.  Run tests: `npm test`

The tests mock GitHub API calls and `@actions/core` functions to ensure deterministic and offline execution.

## 📜 License

This utility is released under the [MIT License](LICENSE).
