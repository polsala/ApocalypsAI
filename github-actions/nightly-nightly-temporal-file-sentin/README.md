# Nightly Temporal File Sentinel

The ApocalypsAI Nightly Integrator presents the `nightly-temporal-file-sentinel`, a GitHub Action designed to whisper warnings about files in your repository that have fallen into a state of temporal stasis. In the ever-shifting sands of the apocalypse, even code and documentation can become ancient relics, forgotten and unblessed. This utility helps you identify such files, prompting a "temporal re-blessing" or review to ensure their continued relevance.

## \ud83c\udf0c Purpose

To automatically scan your repository for files that haven't been modified in a specified period, highlighting potential areas of neglect or outdated information. It acts as a gentle reminder from the temporal currents, urging you to keep your digital artifacts fresh and relevant.

## \u2728 How it Works

This GitHub Action uses `git log` to determine the last modification timestamp for each tracked file in your repository. It then compares this timestamp against a configurable `age-threshold-days`. If a file's last modification date exceeds this threshold, it's flagged as "ancient" and reported.

## \ud83d\ude80 Usage

To integrate the Temporal File Sentinel into your workflow, add the following step to your GitHub Actions workflow file (e.g., `.github/workflows/temporal-check.yml`):

```yaml
name: Temporal File Re-blessing Check

on:
  schedule:
    - cron: '0 0 * * *' # Run daily at midnight UTC
  workflow_dispatch: # Allow manual triggering

jobs:
  check_ancient_files:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Run Temporal File Sentinel
        id: sentinel
        uses: polsala/ApocalypsAI/github-actions/nightly-temporal-file-sentinel@main # Adjust 'main' to your branch/tag
        with:
          age-threshold-days: '180' # Flag files older than 180 days

      - name: Report Ancient Files
        if: ${{ steps.sentinel.outputs.stale-files-count > 0 }}
        run: |
          echo "## \ud83d\udcdc Ancient Scrolls Discovered!" >> $GITHUB_STEP_SUMMARY
          echo "The Temporal File Sentinel has detected ${{ steps.sentinel.outputs.stale-files-count }} files that have not been touched in over 180 days:" >> $GITHUB_STEP_SUMMARY
          echo "```" >> $GITHUB_STEP_SUMMARY
          echo "${{ steps.sentinel.outputs.stale-files-list }}" >> $GITHUB_STEP_SUMMARY
          echo "```" >> $GITHUB_STEP_SUMMARY
          echo "Consider giving these files a 'temporal re-blessing' or review." >> $GITHUB_STEP_SUMMARY
          
          # Optionally fail the job if ancient files are found
          # exit 1 
        shell: bash

      - name: All Clear
        if: ${{ steps.sentinel.outputs.stale-files-count == 0 }}
        run: |
          echo "## \u2728 All Temporal Timelines Stable!" >> $GITHUB_STEP_SUMMARY
          echo "No ancient files detected. Your repository is temporally aligned." >> $GITHUB_STEP_SUMMARY
        shell: bash
```

### Inputs

*   `age-threshold-days`:
    *   **Description**: The number of days a file must remain unmodified (based on its last commit date) to be considered "ancient" and flagged by the sentinel.
    *   **Required**: `true`
    *   **Default**: `365` (one year)

### Outputs

*   `stale-files-count`: The total number of ancient files detected.
*   `stale-files-list`: A newline-separated string containing the paths of all detected ancient files.

## \ud83e\uddea Testing

The utility includes a self-contained test script (`tests/test_check_stale_files.sh`) that mocks `git` commands and the `date` command to ensure deterministic results. This allows for offline validation of the core logic without requiring an actual Git repository or network access.

To run the tests:

```bash
cd github-actions/nightly-temporal-file-sentinel
bash tests/test_check_stale_files.sh
```

The tests simulate various file ages and `age-threshold-days` values to confirm the sentinel correctly identifies ancient files.
