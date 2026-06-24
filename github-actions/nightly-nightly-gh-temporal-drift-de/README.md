# Nightly GH Temporal Drift Detector

A GitHub Action to identify files in your repository whose filesystem modification times (`mtime`) are significantly older than their last Git commit times. This can indicate various forms of "temporal drift," such as files being reverted, copied, or restored without their timestamps being updated, or inconsistencies introduced by caching mechanisms.

## 🚀 Features

- Scans all tracked files within a specified path.
- Compares each file's modification timestamp with its last commit timestamp.
- Reports files where `mtime` is older than `commit_time` by a configurable buffer.
- Provides outputs for detected drift status and a list of drifted files.
- Can optionally fail the workflow if drift is detected.

## 💡 Why is this useful?

In a world of continuous integration and deployment, file timestamps are usually expected to be newer than or very close to their last commit time. Discrepancies can point to:

- **Accidental Reversions**: A file was reverted to an older version without a new commit.
- **Copy-Paste Errors**: Files copied from an older backup without proper Git history.
- **CI/CD Cache Issues**: Build artifacts or cached files might have incorrect timestamps.
- **Manual Tampering**: Files modified outside of Git's tracking, then timestamps manually set to an older date.
- **System Clock Skew**: While less common in CI environments, significant clock differences can cause issues.

## ⚙️ Usage

Add the following step to your GitHub Actions workflow:

```yaml
name: Check for Temporal Drift
on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]
  workflow_dispatch:

jobs:
  detect-drift:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
        with:
          fetch-depth: 0 # Important: Needed to get full commit history for accurate timestamps

      - name: Run Temporal Drift Detector
        id: drift_check
        # Replace with the actual path to your action, e.g., 'polsala/ApocalypsAI/github-actions/nightly-gh-temporal-drift-detector@main'
        uses: ./github-actions/nightly-gh-temporal-drift-detector@main
        with:
          path: '.' # Optional: specify a sub-path to scan
          fail_on_drift: true # Optional: set to 'true' to fail the workflow if drift is found

      - name: Report Drift
        if: steps.drift_check.outputs.drift_detected == 'true'
        run: |
          echo "🚨 Temporal Drift Detected! The following files are out of sync with their timelines:"
          echo "${{ steps.drift_check.outputs.drifted_files }}"
          exit 1 # Fail the job explicitly if fail_on_drift was false but drift was found
      
      - name: No Drift Found
        if: steps.drift_check.outputs.drift_detected == 'false'
        run: |
          echo "✅ All timelines stable. No temporal drift detected."
```

## 📥 Inputs

| Name            | Description                                                                 | Type    | Default | Required |
|-----------------|-----------------------------------------------------------------------------|---------|---------|----------|
| `path`          | The path within the repository to scan for temporal drift.                  | `string`| `.`     | `false`  |
| `fail_on_drift` | If `true`, the action will fail the workflow if any temporal drift is detected. | `boolean`| `false` | `false`  |

## 📤 Outputs

| Name             | Description                                                                 | Type      |
|------------------|-----------------------------------------------------------------------------|-----------|
| `drift_detected` | `true` if temporal drift was detected, `false` otherwise.                   | `boolean` |
| `drifted_files`  | A newline-separated string of files with detected temporal drift.           | `string`  |

## 🧪 How it Works

The action uses `git ls-files` to get a list of all tracked files. For each file, it retrieves:

1.  The last commit timestamp using `git log -1 --format=%ct -- <file>`.
2.  The filesystem modification timestamp using `stat -c %Y <file>` (GNU `stat`).

It then compares these two timestamps. A small buffer (currently 5 seconds) is applied to the commit timestamp to account for minor discrepancies during checkout. If the file's modification time is older than the buffered commit time, it's flagged as drifted.

## ⚠️ Important Notes

-   `fetch-depth: 0` is crucial for `actions/checkout@v4` to ensure `git log` has access to the full commit history for accurate timestamp retrieval.
-   The action assumes a Linux-like environment with GNU `stat` available (e.g., `ubuntu-latest` runners).
-   The `BUFFER_SECONDS` value (5 seconds) is a heuristic. Adjustments might be needed based on specific CI/CD environments or filesystem behaviors.
