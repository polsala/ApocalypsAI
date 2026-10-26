# Nightly Temporal Nudge Action

A GitHub Action that gently nudges stale issues or pull requests with a whimsical, time-themed comment to encourage activity. It helps maintain repository hygiene by identifying discussions that have gone quiet and offering a friendly reminder, without automatically closing them.

## Features

*   **Stale Item Detection**: Identifies issues and pull requests that haven't been updated within a configurable number of days.
*   **Whimsical Nudges**: Posts a customizable, time-themed comment to encourage re-engagement.
*   **Label Exclusion**: Allows ignoring items with specific labels (e.g., `wontfix`, `closed`).
*   **Dry Run Mode**: Test the action without actually posting comments.
*   **Idempotent**: Avoids spamming by checking for existing nudge comments.

## Usage

To use this action, add it to one of your repository's workflows (e.g., `.github/workflows/temporal-nudge.yml`). It's typically run on a schedule.

```yaml
name: Temporal Nudge Workflow

on:
  schedule:
    - cron: '0 0 * * *' # Run daily at midnight UTC
  workflow_dispatch: # Allow manual triggering

jobs:
  nudge-stale-items:
    runs-on: ubuntu-latest
    permissions:
      issues: write # Required to list issues/PRs and create comments
      pull-requests: write # Required to list issues/PRs and create comments
    steps:
      - name: Temporal Nudge Action
        uses: polsala/ApocalypsAI/nightly-temporal-nudge-action@main # Replace 'main' with your branch/tag
        with:
          repo-token: ${{ secrets.GITHUB_TOKEN }}
          stale-days: '60' # Nudge items older than 60 days
          nudge-message: 'A faint echo from the past suggests this discussion might be ripe for revival. Has the future brought new perspectives to light?'
          labels-to-ignore: 'wontfix,enhancement,bug' # Ignore items with these labels
          dry-run: 'false' # Set to 'true' to test without posting comments
```

### Inputs

*   `repo-token`: **(Required)** Your GitHub token for API calls. Use `secrets.GITHUB_TOKEN`.
*   `stale-days`: (Optional) Number of days after which an issue/PR is considered stale. Default: `30`.
*   `nudge-message`: (Optional) The whimsical message to post as a comment. Default: 'A whisper from the temporal currents suggests this thread might appreciate a fresh perspective. What new insights have emerged from the time-stream?'
*   `labels-to-ignore`: (Optional) Comma-separated list of labels to ignore. Items with any of these labels will not be nudged. Default: `''`.
*   `dry-run`: (Optional) If `true`, the action will only log what it would do, without posting comments. Default: `false`.

## Development

### Running Tests

1.  **Install Dependencies**:
    ```bash
    npm install
    ```
2.  **Run Tests**:
    ```bash
    npm test
    ```
