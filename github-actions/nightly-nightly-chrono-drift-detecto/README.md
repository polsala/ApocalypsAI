# Nightly Chrono-Drift Detector

A GitHub Action to detect files whose filesystem modification time is newer than their last commit time. This can indicate uncommitted changes, local modifications after a pull, or build artifacts that are not tracked by Git, leading to "chronological drift" in your repository's state.

## 🌌 Why Chronological Drift Matters

In the chaotic dance of development, files can sometimes get out of sync with their recorded history. A file might appear "newer" on the filesystem than its last recorded commit, creating a temporal anomaly. This action helps you spot these inconsistencies, ensuring your repository's timeline is as pristine as possible.

## ✨ Features

*   **Timestamp Comparison**: Compares a file's last modification timestamp on the filesystem (`mtime`) with the timestamp of its last Git commit.
*   **Drift Detection**: Identifies and reports files where `mtime > commit_time`.
*   **Configurable Path**: Scan the entire repository or a specific subdirectory.
*   **Action Outputs**: Provides boolean flag for drift detection and a list of affected files.

## 🚀 Usage

To use the `nightly-chrono-drift-detector` in your GitHub Actions workflow, add a step like this:

```yaml
name: Check for Chronological Drift

on:
  push:
    branches:
      - main
  pull_request:
    branches:
      - main
  workflow_dispatch:

jobs:
  detect_drift:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Run Chrono-Drift Detector
        id: drift_check
        uses: polsala/ApocalypsAI/github-actions/nightly-chrono-drift-detector@main # Replace 'main' with your branch/tag
        with:
          path: '.' # Optional: specify a subdirectory, e.g., 'src/'

      - name: Report Drift
        if: steps.drift_check.outputs.drift_detected == 'true'
        run: |
          echo "🚨 Chronological drift detected in the following files:"
          echo "${{ steps.drift_check.outputs.drift_files }}"
          echo "Please ensure all changes are committed or that build artifacts are properly ignored."
          exit 1 # Fail the workflow if drift is found
        shell: bash

      - name: No Drift Detected
        if: steps.drift_check.outputs.drift_detected == 'false'
        run: |
          echo "✅ No chronological drift detected. Repository timeline is in harmony."
        shell: bash
```

### Inputs

*   `path` (optional): The path within the repository to check for drift. Defaults to `.` (the entire repository).

### Outputs

*   `drift_detected` (boolean): `true` if any chronological drift was detected, `false` otherwise.
*   `drift_files` (string): A newline-separated list of files exhibiting chronological drift. Empty if no drift is found.

## 🛠️ Development & Testing

The core logic resides in `src/detect_drift.sh`. Tests are implemented in `tests/test_detect_drift.sh`.

To run tests locally:

```bash
cd github-actions/nightly-chrono-drift-detector
./tests/test_detect_drift.sh
```

This will create a temporary Git repository, simulate various drift scenarios, and verify the script's output.

## 📜 License

This utility is released under the [MIT License](LICENSE).
