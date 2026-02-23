# Nightly Chrono-Sync Checker

## 🌌 Overview

In the chaotic temporal landscape of the post-apocalyptic world, even your repository's timeline can get a bit... wobbly. The `Nightly Chrono-Sync Checker` is your vigilant guardian against "chrono-desynchronization" – a state where files on your disk appear to have been modified *after* the last recorded commit. This could indicate forgotten `git add` commands, uncommitted build artifacts, or even minor temporal paradoxes. Keep your repository's history pristine and its present in harmony with its past!

## ✨ Features

- **Temporal Anomaly Detection**: Scans all files in your repository for modification timestamps that are significantly newer than the latest commit timestamp.
- **Configurable Tolerance**: Allows you to set a grace period (in seconds) to account for minor clock skews or file system nuances.
- **Clear Reporting**: Fails the GitHub Actions workflow and outputs a list of all desynchronized files, helping you pinpoint and resolve temporal discrepancies.

## 🚀 Usage

To integrate the `Nightly Chrono-Sync Checker` into your GitHub Actions workflow, add a step like this:

```yaml
name: Chrono Sync Check

on: [push, pull_request]

jobs:
  chrono-sync:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4
        with:
          fetch-depth: 0 # Important: Fetch full history to get accurate commit timestamps

      - name: Run Nightly Chrono-Sync Checker
        uses: polsala/ApocalypsAI/github-actions/nightly-chrono-sync-checker@main # Replace 'main' with your branch if needed
        id: chrono_check
        with:
          tolerance_seconds: '10' # Optional: Increase tolerance if needed (default is 5 seconds)

      - name: Report Desynchronization (Optional)
        if: ${{ steps.chrono_check.outputs.desynchronized_files_found == 'true' }}
        run: |
          echo "::warning::Temporal rifts detected! Please investigate the desynchronized files."
          # You might want to add more actions here, like opening an issue or notifying a channel.
```

### Inputs

| Input Name        | Description                                                                 | Type    | Default | Required |
|-------------------|-----------------------------------------------------------------------------|---------|---------|----------|
| `tolerance_seconds` | Time in seconds to tolerate between file modification time and latest commit time. | `string` | `'5'`   | `false`  |

### Outputs

| Output Name              | Description                                        | Type      |
|--------------------------|----------------------------------------------------|-----------|
| `desynchronized_files_found` | `true` if any desynchronized files were found, `false` otherwise. | `boolean` |

## 🧪 Testing

The action includes a self-contained test workflow (`tests/test_workflow.yml`) that demonstrates its functionality in both a "clean" and a "desynchronized" repository state.

To run the tests:

1.  Navigate to the "Actions" tab in your repository.
2.  Select the "Test Nightly Chrono-Sync Checker" workflow.
3.  Click "Run workflow" and choose the `main` branch (or your working branch).

The workflow will execute two jobs:
- `test-clean-repo`: Expected to pass, verifying that a synchronized repository is correctly identified.
- `test-desynchronized-repo`: Expected to fail, verifying that a file modified after the last commit is correctly flagged.

This ensures the action reliably detects temporal anomalies in your file system.
