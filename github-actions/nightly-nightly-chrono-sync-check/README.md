# Nightly Chrono-Sync Check GitHub Action

This GitHub Action, `nightly-chrono-sync-check`, acts as a 'Temporal Anomaly Detector' for your repository's branches. It compares the timestamp of the latest commit on the current branch with the actual workflow run time. This helps in identifying:

- **Stale Branches**: Commits that are significantly older than the workflow run, indicating a potentially neglected or outdated branch.
- **Future Commits (Temporal Anomalies)**: Commits with timestamps that are in the future relative to the workflow run, which could point to misconfigured developer clocks or more mysterious temporal distortions.

By integrating this action into your CI/CD pipelines, you can ensure your branches are chronologically aligned and prevent issues arising from outdated code or time-traveling developers.

## Usage

Add this action to your GitHub Workflow (`.github/workflows/your-workflow.yml`):

```yaml
name: Chrono Sync Workflow
on:
  push:
    branches:
      - main
  pull_request:
    branches:
      - main
  workflow_dispatch:

jobs:
  chrono_check:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Run Nightly Chrono-Sync Check
        id: chrono_sync
        uses: polsala/ApocalypsAI/github-actions/nightly-chrono-sync-check@main # Replace 'main' with your branch/tag if needed
        with:
          max-stale-hours: '48' # Flag as stale if commit is older than 48 hours
          fail-on-stale: 'true' # Fail the workflow if a stale commit is found
          fail-on-future: 'true' # Fail if commit is in the future (default is true)

      - name: Report Chrono-Sync Status
        if: always()
        run: |
          echo "Is Stale: ${{ steps.chrono_sync.outputs.is-stale }}"
          echo "Is Future: ${{ steps.chrono_sync.outputs.is-future }}"
          echo "Time Difference (Hours): ${{ steps.chrono_sync.outputs.time-difference-hours }}"
          if [ "${{ steps.chrono_sync.outputs.is-stale }}" == "true" ]; then
            echo "🚨 Warning: Branch is chronologically adrift!"
          fi
          if [ "${{ steps.chrono_sync.outputs.is-future }}" == "true" ]; then
            echo "🌌 Anomaly Detected: Commit from the future!"
          fi
```

## Inputs

| Input Name          | Description                                                                 | Type    | Default | Required |
|---------------------|-----------------------------------------------------------------------------|---------|---------|----------|
| `max-stale-hours`   | Maximum hours a commit can be older than the workflow run time before flagging as stale. | `string`| `'24'`  | `false`  |
| `fail-on-stale`     | If `true`, the action will fail the workflow if the latest commit is detected as stale. | `string`| `'false'`| `false`  |
| `fail-on-future`    | If `true`, the action will fail the workflow if the latest commit timestamp is in the future. | `string`| `'true'` | `false`  |

## Outputs

| Output Name           | Description                                                                 |
|-----------------------|-----------------------------------------------------------------------------|
| `is-stale`            | `true` if the latest commit is older than `max-stale-hours`, `false` otherwise. |
| `is-future`           | `true` if the latest commit timestamp is in the future, `false` otherwise. |
| `time-difference-hours`| The time difference in hours between the workflow run time and the latest commit time (positive if past, negative if future). |

## How it works

The action fetches the epoch timestamp of the current workflow run and the latest commit on the checked-out branch. It then calculates the difference and compares it against the configured `max-stale-hours` and checks for future timestamps. Depending on the `fail-on-stale` and `fail-on-future` inputs, it will either warn or fail the workflow.
