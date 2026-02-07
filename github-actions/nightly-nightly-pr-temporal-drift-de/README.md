# Nightly PR Temporal Drift Detector

A GitHub Action that detects "temporal drift" in pull requests, flagging PRs that have been open too long or have stale commits. This helps maintain a healthy, flowing timeline for your repository's development.

## Usage

Add this action to your workflow to automatically check pull requests for temporal anomalies.

```yaml
name: PR Temporal Drift Check

on:
  pull_request:
    types: [opened, reopened, synchronize]

jobs:
  detect_drift:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Detect Temporal Drift
        id: drift_detector
        uses: polsala/ApocalypsAI/github-actions/nightly-pr-temporal-drift-detect@main # Replace 'main' with your branch/tag
        with:
          github-token: ${{ secrets.GITHUB_TOKEN }}
          pr-number: ${{ github.event.pull_request.number }}
          repo-owner: ${{ github.repository_owner }}
          repo-name: ${{ github.event.repository.name }}
          max-open-days: 14 # Flag PRs open for more than 14 days
          max-stale-commit-days: 5 # Flag PRs with no new commits in 5 days

      - name: Report Drift
        if: steps.drift_detector.outputs.drift-detected == 'true'
        run: |
          echo "Temporal Drift Detected! Message: ${{ steps.drift_detector.outputs.drift-message }}"
          # Optionally, add a comment to the PR
          # gh pr comment ${{ github.event.pull_request.number }} --body "${{ steps.drift_detector.outputs.drift-message }}"
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

## Inputs

*   `github-token`: **(Required)** Your GitHub token, usually `${{ secrets.GITHUB_TOKEN }}`. Used for fetching PR data if `_mock-pr-json` is not provided.
*   `pr-number`: **(Required)** The number of the pull request to check.
*   `repo-owner`: **(Required)** The owner of the repository (e.g., `polsala`).
*   `repo-name`: **(Required)** The name of the repository (e.g., `ApocalypsAI`).
*   `max-open-days`: (Optional) The maximum number of days a PR can be open before being flagged for temporal drift. Default: `7`.
*   `max-stale-commit-days`: (Optional) The maximum number of days since the last commit on the PR branch before it's flagged as having stale commits. Default: `3`.
*   `_mock-pr-json`: (Internal/Testing) A JSON string representing PR data to bypass GitHub API calls. This input is primarily for deterministic testing.

## Outputs

*   `drift-detected`: `true` if temporal drift was detected, `false` otherwise.
*   `drift-message`: A descriptive message about the detected drift, if any.
