# Nightly Workflow Chronomancer

## 🕰️ A Temporal Mood Ring for Your Workflows 🕰️

Ever wonder if your CI/CD workflows are feeling zippy, sluggish, or just steady? The Nightly Workflow Chronomancer is here to tell you! This GitHub Action monitors the duration of your specified workflows, compares the latest run to a historical average, and reports its 'temporal mood' with a whimsical status.

Keep an eye on performance regressions, celebrate unexpected speed-ups, and ensure your automation is always running at its best.

## ✨ Features

*   **Duration Monitoring**: Tracks the execution time of any GitHub Actions workflow.
*   **Anomaly Detection**: Identifies if the latest run is significantly faster or slower than its historical average.
*   **Whimsical Reporting**: Outputs a 'temporal mood' (zippy, sluggish, steady, unknown) and percentage change.
*   **Configurable Thresholds**: Customize how sensitive the anomaly detection is.

## 🚀 Usage

Add this action to one of your workflows to monitor another workflow. For example, you might run this in a daily cron job or after a critical deployment workflow.

```yaml
name: Monitor CI Workflow Performance
on:
  workflow_dispatch:
  schedule:
    - cron: '0 0 * * *' # Run daily at midnight UTC

jobs:
  monitor-ci:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Chronomancer Check on Main CI
        id: chronomancer
        uses: polsala/ApocalypsAI/github-actions/nightly-workflow-chronomancer@main # Replace 'main' with your branch/tag
        with:
          workflow_id: 'ci.yml' # The file name of the workflow to monitor (e.g., 'ci.yml' or its ID)
          repo_token: ${{ secrets.GITHUB_TOKEN }} # Required for API access
          threshold_percent: 20 # Report if duration changes by more than 20%
          num_runs_for_average: 5 # Use the last 5 successful runs for average

      - name: Report Temporal Mood
        run: |
          echo "The 'ci.yml' workflow is feeling ${{ steps.chronomancer.outputs.status }}!"
          echo "Latest run: ${{ steps.chronomancer.outputs.latest_duration_seconds }}s"
          echo "Average: ${{ steps.chronomancer.outputs.average_duration_seconds }}s"
          echo "Change: ${{ steps.chronomancer.outputs.duration_change_percent }}%"

      - name: Fail if Sluggish (Optional)
        if: steps.chronomancer.outputs.status == 'sluggish'
        run: |
          echo "Workflow is too sluggish! Failing this check."
          exit 1
```

### Inputs

| Name                   | Description                                                                                             | Required | Default                  |
| :--------------------- | :------------------------------------------------------------------------------------------------------ | :------- | :----------------------- |
| `workflow_id`          | The ID or file name of the workflow to monitor (e.g., `my-ci.yml` or `12345`).                          | `true`   |                          |
| `repo_token`           | GitHub token with permissions to read workflow runs.                                                    | `false`  | `${{ github.token }}`    |
| `threshold_percent`    | Percentage threshold for detecting significant duration changes (e.g., `20` for 20% faster/slower).     | `false`  | `15`                     |
| `num_runs_for_average` | Number of recent successful runs to consider for calculating the average duration.                        | `false`  | `10`                     |

### Outputs

| Name                        | Description                                                                                             | Example         |
| :-------------------------- | :------------------------------------------------------------------------------------------------------ | :-------------- |
| `status`                    | The temporal mood of the workflow run (`zippy`, `sluggish`, `steady`, `unknown`).                       | `zippy`         |
| `duration_change_percent`   | Percentage change of the latest run duration compared to the average. Positive for slower, negative for faster. | `-10.50`        |
| `latest_duration_seconds`   | Duration of the latest workflow run in seconds.                                                         | `120.34`        |
| `average_duration_seconds`  | Average duration of recent successful workflow runs in seconds.                                         | `134.78`        |

## 🧙‍♂️ How it Works

The Chronomancer fetches a specified number of recent *successful* runs for the target workflow. It calculates the average duration from these historical runs. Then, it compares the duration of the *latest* successful run against this average. If the deviation exceeds your `threshold_percent`, it declares the workflow's 'temporal mood' accordingly. Otherwise, it's a 'steady' day in the timeline!
