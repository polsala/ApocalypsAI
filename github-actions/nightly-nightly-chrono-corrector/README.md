# Nightly Chrono-Corrector

## 🕰️ Overview

The `nightly-chrono-corrector` is a whimsical yet highly useful GitHub Action designed to ensure your repository's timeline is perfectly aligned. It scans specified files and directories for outdated year references (specifically, the previous year) and reports them, suggesting an update to the current year. Think of it as your personal temporal guardian, preventing minor anachronisms from creeping into your project's documentation, licenses, or changelogs.

## ✨ Features

*   **Outdated Year Detection**: Identifies instances of the previous year where the current year is likely expected (e.g., in copyright notices).
*   **Configurable Scan Paths**: Allows you to specify which files or directories to scan.
*   **Detailed Reporting**: Provides a clear markdown report of all detected temporal anomalies.
*   **Whimsical Persona**: Delivers reports with a touch of temporal flair.

## 🚀 Usage

To use the `nightly-chrono-corrector` in your workflow, add a step like this:

```yaml
name: Check for Outdated Years
on:
  pull_request:
    branches: [ main ]
  push:
    branches: [ main ]
  schedule:
    - cron: '0 0 * * *' # Run daily at midnight UTC

jobs:
  chrono_correction:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Run Nightly Chrono-Corrector
        id: chrono_check
        uses: polsala/ApocalypsAI/github-actions/nightly-chrono-corrector@main # Replace 'main' with your branch/tag if needed
        with:
          github-token: ${{ secrets.GITHUB_TOKEN }}
          scan-paths: 'README.md,LICENSE,docs/,src/some_module/CHANGELOG.md'
          # current-year: '2024' # Optional: defaults to current year if not provided

      - name: Report Anomalies
        if: ${{ steps.chrono_check.outputs.anomalies-found == 'true' }}
        run: |
          echo "${{ steps.chrono_check.outputs.report }}"
          # Optionally, add a comment to the PR or create an issue
          # For PR comments, you'd need to use the GitHub API via 'github-script' action or similar.
          # Example for PR comment (requires 'pull_requests: write' permission):
          # - uses: actions/github-script@v6
          #   if: github.event_name == 'pull_request' && steps.chrono_check.outputs.anomalies-found == 'true'
          #   with:
          #     script: |
          #       github.rest.issues.createComment({
          #           issue_number: context.issue.number,
          #           owner: context.repo.owner,
          #           repo: context.repo.repo,
          #           body: `${{ steps.chrono_check.outputs.report }}`
          #       })

      - name: No Anomalies Found
        if: ${{ steps.chrono_check.outputs.anomalies-found == 'false' }}
        run: |
          echo "${{ steps.chrono_check.outputs.report }}"
```

## ⚙️ Inputs

*   `github-token`: **(Required)** Your GitHub token for API access. Typically `${{ secrets.GITHUB_TOKEN }}`.
*   `scan-paths`: **(Optional)** A comma-separated string of file paths or directories to scan. Defaults to `README.md,LICENSE`.
*   `current-year`: **(Optional)** The year to check against. If not provided, the action will dynamically determine the current year.

## 📤 Outputs

*   `anomalies-found`: `true` if any outdated year references were found, `false` otherwise.
*   `report`: A markdown string containing a detailed report of findings or a message indicating no anomalies were found.

## 🧪 Development & Testing

To test this action locally, navigate to the `github-actions/nightly-chrono-corrector` directory and run the `tests/test.sh` script. This script simulates the GitHub Actions environment and verifies the action's behavior against various scenarios.

```bash
cd github-actions/nightly-chrono-corrector
bash tests/test.sh
```
