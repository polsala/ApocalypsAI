# Nightly Workflow Wellness Report

This GitHub Action generates a wellness report for your repository's workflows, identifying runs that are consistently long-running or frequently failing. It helps maintain a healthy CI/CD pipeline by bringing potential issues to your attention.

## Features

- **Long-Run Detection**: Flags workflow runs that exceed a specified duration threshold.
- **Frequent Failure Identification**: Highlights workflows that have failed a certain number of times within a recent set of runs.
- **Summary Output**: Provides a concise markdown summary that can be used in PR comments, issue reports, or other notifications.

## Usage

To use this action, add it as a step in one of your GitHub Actions workflows. It's ideal for scheduled daily or weekly checks.

```yaml
name: Daily Workflow Wellness Check

on:
  schedule:
    - cron: '0 0 * * *' # Run daily at midnight UTC
  workflow_dispatch: # Allow manual triggering

jobs:
  wellness_check:
    runs-on: ubuntu-latest
    permissions:
      actions: read # Required to list workflow runs

    steps:
      - name: Generate Workflow Wellness Report
        uses: polsala/ApocalypsAI/github-actions/nightly-workflow-wellness-report@main # Adjust path if this action is in a sub-directory
        id: wellness_report
        with:
          token: ${{ secrets.GITHUB_TOKEN }}
          repo: ${{ github.repository }}
          max-runs: 50
          long-run-threshold-minutes: 15
          failure-frequency-threshold: 5

      - name: Output Report Summary
        run: |
          echo "${{ steps.wellness_report.outputs.report-summary }}"
          # Optionally, post this summary to an issue, discussion, or Slack
          # Example: Create an issue with the report
          # if [ -n "${{ steps.wellness_report.outputs.report-summary }}" ]; then
          #   gh issue create --repo ${{ github.repository }} \
          #     --title "Daily Workflow Wellness Report - $(date +'%Y-%m-%d')" \
          #     --body "${{ steps.wellness_report.outputs.report-summary }}"
          # fi
        env:
          GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

## Inputs

| Name                        | Description                                                              | Required | Default |
|-----------------------------|--------------------------------------------------------------------------|----------|---------|
| `token`                     | GitHub token with `actions:read` permission. Usually `${{ secrets.GITHUB_TOKEN }}`. | `true`   |         |
| `repo`                      | The repository to check (e.g., `owner/repo`). Usually `${{ github.repository }}`. | `true`   |         |
| `max-runs`                  | Maximum number of recent workflow runs to analyze.                       | `false`  | `100`   |
| `long-run-threshold-minutes`| Threshold in minutes for a workflow run to be considered "long-running". | `false`  | `10`    |
| `failure-frequency-threshold`| Number of failures within `max-runs` to consider a workflow "frequently failing". | `false`  | `3`     |

## Outputs

| Name             | Description                                   |
|------------------|-----------------------------------------------|
| `report-summary` | A markdown-formatted summary of the wellness report. |

## Dependencies

This action relies on the `gh` (GitHub CLI) and `jq` (JSON processor) tools being available in the runner's environment. GitHub-hosted runners typically have these pre-installed.
