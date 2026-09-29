# GitHub Actions Workflow Linter

This GitHub Action provides a robust way to lint and validate your GitHub Actions workflows (`.github/workflows/*.yml`). It helps catch common syntax errors, potential security issues, and adherence to best practices before they cause problems in your CI/CD pipelines.

## Features

*   **Syntax Validation**: Checks for YAML syntax errors.
*   **Best Practice Checks**: Identifies common anti-patterns and potential improvements.
*   **Security Linting**: Flags potentially insecure configurations.
*   **Customizable**: Supports specifying which linters to run.

## Usage

To use this action in your workflow, add the following to your `.github/workflows/your-workflow.yml` file:

```yaml
name: Lint GitHub Actions Workflows

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  lint-workflows:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Run GitHub Actions Linter
        uses: polsala/ApocalypsAI/nightly-gh-action-lint-runner@main
        with:
          # Optional: Specify linters to run. Defaults to all.
          # linters: "yamllint,actionlint"
          # Optional: Path to workflows directory. Defaults to .github/workflows.
          # workflow_path: ".github/workflows"
