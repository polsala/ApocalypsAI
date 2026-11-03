# nightly-apocalypse-readiness-report

Generates a "readiness report card" for a GitHub repository by checking for essential project files and best practices. This action helps maintain project health and ensures your repository is well-documented and prepared for any cosmic eventuality.

## 🚀 Usage

To use the `nightly-apocalypse-readiness-report` action in your workflow, add a step like this:

```yaml
name: Repository Readiness Check

on:
  push:
    branches:
      - main
  pull_request:
    branches:
      - main
  workflow_dispatch:

jobs:
  readiness_check:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Generate Apocalypse Readiness Report
        id: readiness_report
        uses: polsala/ApocalypsAI/github-actions/nightly-apocalypse-readiness-report@main # Replace 'main' with your branch/tag
        with:
          report-level: 'full' # Options: 'basic', 'standard', 'full'

      - name: Output Report to Job Summary
        run: |
          echo "${{ steps.readiness_report.outputs.report }}" >> $GITHUB_STEP_SUMMARY

      - name: (Optional) Post Report as PR Comment
        if: github.event_name == 'pull_request'
        uses: actions/github-script@v6
        with:
          github-token: ${{ secrets.GITHUB_TOKEN }}
          script: |
            const report = `${{ steps.readiness_report.outputs.report }}`;
            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: report
            });
```

### Inputs

*   `report-level` (Optional, default: `standard`):
    *   `'basic'`: Checks for `README.md`, `LICENSE`.
    *   `'standard'`: Includes `basic` checks plus `CONTRIBUTING.md`, `SECURITY.md`, `CODE_OF_CONDUCT.md`.
    *   `'full'`: Includes `standard` checks plus `.github/workflows/`, `.github/ISSUE_TEMPLATE/`, `.github/PULL_REQUEST_TEMPLATE/`, `CHANGELOG.md`.

### Outputs

*   `report`: A markdown string containing the generated readiness report card.

## 🧪 How it Works

The action executes a bash script that scans the repository for the presence of key files and directories based on the specified `report-level`. It then compiles a markdown report, including a readiness score and status, which is made available as an action output.

## 🛠️ Development & Testing

The core logic resides in `src/generate_report.sh`. Tests are implemented in `tests/test_report_generator.sh` using a temporary file system to simulate various repository states.

To run tests locally:

```bash
cd github-actions/nightly-apocalypse-readiness-report
bash tests/test_report_generator.sh
```
