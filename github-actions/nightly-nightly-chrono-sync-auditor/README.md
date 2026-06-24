# Nightly Chrono-Sync Auditor

A GitHub Action to detect chronological inconsistencies in your repository. This utility identifies files whose filesystem modification times (mtime) are *older* than their last recorded commit timestamp in Git.

Such "temporal echoes" can indicate:
- Stale checkouts or partial reverts.
- Build processes that inadvertently touch files with older timestamps.
- Files restored from backups without preserving original mtimes.
- General inconsistencies that might lead to unexpected build behaviors or caching issues.

Ensure your repository's temporal integrity with the Chrono-Sync Auditor!

## Usage

Add this action to your workflow:

```yaml
name: Chrono Sync Check

on: [push, pull_request]

jobs:
  audit:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Run Chrono-Sync Auditor
        id: chrono-audit
        uses: polsala/ApocalypsAI/github-actions/nightly-chrono-sync-auditor@main # Replace 'main' with your branch/tag
        with:
          fail-on-anomaly: 'true' # Set to 'false' to only warn, not fail the workflow

      - name: Report Anomalies (if any)
        if: steps.chrono-audit.outputs.anomalies-found == 'true'
        run: |
          echo "🚨 Chronological Anomalies Detected:"
          echo "${{ steps.chrono-audit.outputs.anomaly-list }}"
          echo "Please investigate these files for temporal inconsistencies."
```

### Inputs

- `fail-on-anomaly`:
  - **Description**: Whether the action should fail the workflow if any chronological anomalies are found.
  - **Required**: `false`
  - **Default**: `'true'`
  - **Type**: `boolean` (`'true'` or `'false'`)

### Outputs

- `anomalies-found`:
  - **Description**: `true` if any chronological anomalies were detected, `false` otherwise.
  - **Type**: `boolean`
- `anomaly-list`:
  - **Description**: A newline-separated string of file paths that exhibit chronological anomalies. Empty if no anomalies are found.
  - **Type**: `string`

## How it Works

The action performs the following steps:
1. It uses `git ls-files -z` to get a null-separated list of all files tracked by Git in the current working directory.
2. For each file, it retrieves:
    - Its last commit timestamp using `git log -1 --format="%ct" -- <file_path>`.
    - Its current filesystem modification time (mtime) using `stat -c %Y <file_path>`.
3. If a file's `mtime` is found to be strictly *less than* its `last commit timestamp`, it's flagged as a chronological anomaly.
4. All detected anomalies are reported as warnings (or errors if `fail-on-anomaly` is `true`), and the list is provided as an output.

This check helps maintain the integrity of your repository's working state relative to its version history.
