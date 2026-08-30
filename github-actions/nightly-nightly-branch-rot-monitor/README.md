# Nightly Branch Rot Monitor

## 🤖 Overview

The `nightly-branch-rot-monitor` is a whimsical-yet-useful GitHub Action designed to keep your repository tidy by identifying and notifying about stale branches. In the post-apocalyptic landscape of code, forgotten branches can accumulate like digital debris. This monitor acts as a diligent scavenger, ensuring no branch is left to rot in the temporal void.

When a branch is deemed stale (inactive for a configurable number of days), the action will either:
1.  **Comment on an existing Pull Request**: If an open PR is associated with the stale branch, a friendly reminder will be posted there.
2.  **Open a new Issue**: If no open PR exists, a new issue will be created, assigned to the last committer, to bring attention to the forgotten branch.

## ✨ How it Works

1.  The action runs on a schedule (e.g., nightly or weekly).
2.  It fetches all branches in the repository, excluding protected ones (like `main`, `master`, `develop`).
3.  For each non-protected branch, it checks the date of its last commit.
4.  If the last commit is older than the configured `stale-days`, the branch is marked as stale.
5.  The action then attempts to find an open Pull Request for the stale branch.
6.  Based on the presence of a PR, it either comments on the PR or creates a new issue, notifying the relevant parties.

## ⚙️ Inputs

| Name          | Description                                                               | Required | Default |
| :------------ | :------------------------------------------------------------------------ | :------- | :------ |
| `stale-days`  | Number of days without activity for a branch to be considered stale.      | `true`   | `30`    |
| `repo-token`  | GitHub token with permissions to read branches, create issues, and comment on PRs. Typically `${{ github.token }}`. | `true`   |         |

## 🚀 Outputs

| Name                   | Description                                  |
| :--------------------- | :------------------------------------------- |
| `stale-branches-count` | The number of stale branches found and processed. |

## 📝 Example Usage

To integrate the `Nightly Branch Rot Monitor` into your repository, create a workflow file (e.g., `.github/workflows/stale-branch-monitor.yml`):

```yaml
name: 'Branch Rot Monitor'

on:
  schedule:
    - cron: '0 0 * * 0' # Run every Sunday at midnight UTC
  workflow_dispatch: # Allow manual triggering

jobs:
  monitor-stale-branches:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repository
        uses: actions/checkout@v3

      - name: Run Branch Rot Monitor
        uses: polsala/ApocalypsAI/utils/nightly-branch-rot-monitor@main # Adjust path if needed
        with:
          stale-days: 60 # Consider branches stale after 60 days of inactivity
          repo-token: ${{ secrets.GITHUB_TOKEN }}

      - name: Report Stale Branches Count
        run: echo "Found ${{ steps.monitor.outputs.stale-branches-count }} stale branches."
        id: monitor
```

**Note**: Ensure the `repo-token` has sufficient permissions (e.g., `contents: read`, `pull-requests: write`, `issues: write`). The default `GITHUB_TOKEN` usually has these permissions for actions within the same repository.

## 🛠️ Development & Testing

This action is built with Node.js. To set up the development environment and run tests:

```bash
cd utils/nightly-branch-rot-monitor
npm install
npm test
```
