# Nightly Stale Issue Gardener

This GitHub Action helps maintain a tidy issue "garden" by automatically identifying and managing stale issues. It can mark issues as stale after a period of inactivity, post a customizable message, and then close them if no further activity occurs.

## Features

*   **Automatic Stale Labeling**: Adds a configurable 'stale' label to issues that have been inactive for a specified number of days.
*   **Customizable Messages**: Allows you to define the messages posted when an issue is marked stale or closed.
*   **Automatic Closing**: Closes issues that remain inactive for an additional period after being marked stale.
*   **Exemption**: Excludes issues with specific labels (e.g., `bug`, `enhancement`, `pinned`) from being processed.
*   **Targeted Processing**: Optionally processes only issues that have one of a specified set of labels.
*   **Skips Pull Requests**: Ensures only issues are processed, not pull requests.

## Usage

To use the Stale Issue Gardener, add a new workflow file (e.g., `.github/workflows/stale-gardener.yml`) to your repository:

```yaml
name: 'Stale Issue Gardener'

on: 
  schedule:
    - cron: '0 0 * * *' # Runs daily at midnight UTC
  workflow_dispatch: # Allows manual triggering

jobs:
  stale:
    runs-on: ubuntu-latest
    steps:
      - name: 'Run Stale Issue Gardener'
        uses: polsala/ApocalypsAI/github-actions/nightly-stale-issue-gardener@main # Replace 'main' with your branch if needed
        with:
          repo-token: ${{ secrets.GITHUB_TOKEN }}
          stale-issue-label: 'stale-garden'
          days-before-stale: 60
          days-before-close: 14
          stale-issue-message: |
            This issue has been sitting in our garden for a while without activity. 
            It will be gently pruned (closed) if no further activity occurs within the next 14 days.
            Please provide an update if this is still relevant!
          close-issue-message: |
            This issue has been pruned from our garden due to prolonged inactivity. 
            Feel free to plant a new one (reopen) if it's still a blooming concern!
          exempt-labels: 'bug,enhancement,security,pinned'
          # only-labels: 'feature,discussion' # Uncomment to only process issues with 'feature' or 'discussion' labels
```

## Inputs

| Input                 | Description                                                                                                                               | Required | Default             |
| :-------------------- | :---------------------------------------------------------------------------------------------------------------------------------------- | :------- | :------------------ |
| `repo-token`          | **Required**. Token for the GitHub API. Usually `${{ secrets.GITHUB_TOKEN }}`.                                                            | `true`   |                     |
| `stale-issue-label`   | Label to apply to stale issues.                                                                                                           | `false`  | `stale`             |
| `days-before-stale`   | Number of days of inactivity before an issue is marked stale.                                                                             | `false`  | `30`                |
| `days-before-close`   | Number of days after an issue is initially considered stale (total inactivity) before it is closed.                                       | `false`  | `7`                 |
| `stale-issue-message` | Message to post when an issue is marked stale. Supports multi-line strings.                                                               | `false`  | (See `action.yml`)  |
| `close-issue-message` | Message to post when an issue is closed. Supports multi-line strings.                                                                     | `false`  | (See `action.yml`)  |
| `exempt-labels`       | Comma-separated list of labels that exempt an issue from being marked stale or closed.                                                    | `false`  | `bug,enhancement,pinned,security` |
| `only-labels`         | Comma-separated list of labels. If provided, only issues with *at least one* of these labels will be considered for staleness/closing. | `false`  | `''` (empty)        |

## How it Works

1.  The action fetches all open issues in the repository.
2.  For each issue, it checks its `updated_at` timestamp.
3.  If an issue has been inactive for `days-before-stale` days and does *not* have the `stale-issue-label` (and is not exempt/matches `only-labels` if specified), it will be marked with the `stale-issue-label` and a `stale-issue-message` comment will be added.
4.  If an issue *already* has the `stale-issue-label` and its total inactivity (from `updated_at`) exceeds `days-before-stale` + `days-before-close` days, it will be closed with a `close-issue-message` comment.
5.  Pull requests are always ignored.

## Development

This action is implemented in JavaScript using Node.js. Tests are written with Jest.

To run tests locally:

```bash
npm install
npm test
```
