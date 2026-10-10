# Nightly Workflow Harmony Enforcer

## Overview

The `nightly-workflow-harmony-enforcer` is a GitHub Action designed to help maintain order and best practices within your repository's GitHub Actions workflows. It scans your workflow `.yml` files for common anti-patterns and missing configurations, providing actionable feedback to improve security, efficiency, and clarity.

## Features

*   **Permissions Check**: Warns if a workflow is missing an explicit `permissions` block, encouraging least-privilege security practices.
*   **Checkout Action Version Check**: Recommends upgrading `actions/checkout` to its latest major version (v3 or higher) for improved security and features.
*   **Concurrency Check**: Suggests adding a `concurrency` group for `push` or `pull_request` triggered workflows to prevent redundant or conflicting runs.

## Usage

To use this action, add it as a step in one of your existing workflows, or create a dedicated workflow to run it periodically.

```yaml
name: Workflow Harmony Scan

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]
  workflow_dispatch:

jobs:
  harmony_check:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Run Workflow Harmony Enforcer
        uses: polsala/ApocalypsAI/.github/actions/nightly-workflow-harmony-enforcer@main # Replace 'main' with your branch/tag
        with:
          workflow-file-glob: '.github/workflows/*.yml'

      # Example: Fail the job if harmony issues are found (optional)
      # - name: Check for Harmony Issues
      #   run: |
      #     if grep -q "::warning::" ${{ steps.harmony_check.outputs.harmony-report }} || grep -q "::error::" ${{ steps.harmony_check.outputs.harmony-report }};
      #     then
      #       echo "Harmony issues detected! See above warnings/errors."
      #       exit 1
      #     else
      #       echo "All workflows are in harmony!"
      #     fi
```

### Inputs

*   `workflow-file-glob` (optional): A glob pattern to specify which workflow files to check. Defaults to `.github/workflows/*.yml`.

## Output

The action will print warnings (`::warning::`) or errors (`::error::`) directly to the GitHub Actions log for any detected issues. It also creates a `harmony_report.txt` file in the workspace root with a summary of findings, accessible via the `harmony-report` output.

## Development

To run tests or contribute, see the `tests/` directory.
