# Nightly Dust Bunny Collector

A GitHub Action to automatically prune old workflow runs, keeping your repository's action logs tidy and efficient.

## 🧹 What it Does

This action identifies and deletes GitHub Actions workflow runs that are older than a specified number of days. Over time, workflow runs can accumulate, consuming storage and making it harder to find relevant history. The Dust Bunny Collector helps you maintain a clean and manageable workflow history.

## ✨ Features

*   **Configurable Retention**: Set how many days you want to keep workflow runs.
*   **Automated Cleanup**: Ideal for scheduled runs (e.g., nightly, weekly).
*   **Safe Deletion**: Logs deleted runs and handles individual deletion failures gracefully.
*   **Pagination**: Efficiently handles repositories with a large number of workflow runs.

## 🚀 Usage

To use this action, add a new step or a new workflow file to your repository, typically scheduled to run periodically.

### Example Workflow (`.github/workflows/cleanup.yml`):

```yaml
name: 'Dust Bunny Cleanup'

on:
  workflow_dispatch: # Allows manual triggering
  schedule:
    - cron: '0 0 * * *' # Runs daily at midnight UTC

jobs:
  cleanup:
    runs-on: ubuntu-latest
    steps:
      - name: 'Collect and Sweep Dust Bunnies'
        uses: polsala/ApocalypsAI/github-actions/nightly-dust-bunny-collector@main # Replace 'main' with your branch/tag if needed
        with:
          token: ${{ secrets.GITHUB_TOKEN }}
          retention-days: '30' # Keep runs for 30 days, delete older ones
```

### Inputs

*   `token`: **(Required)** Your GitHub Token. `secrets.GITHUB_TOKEN` is usually sufficient, as it has `repo` scope permissions needed to delete workflow runs.
*   `retention-days`: **(Optional)** The number of days to retain workflow runs. Any run older than this will be deleted. Defaults to `30`.

## ⚠️ Permissions

This action requires `actions: write` permission to delete workflow runs. Ensure that the `GITHUB_TOKEN` or custom token provided has this permission. For `secrets.GITHUB_TOKEN`, this is typically granted by default in `workflow_dispatch` and `schedule` events.

```yaml
permissions:
  actions: write # Required for deleting workflow runs
```

## 🛠️ Development

This action is written in JavaScript and uses the `@actions/core` and `@actions/github` toolkits.

To run tests:

```bash
npm install
npm test
```
