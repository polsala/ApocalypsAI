# Nightly GitHub Actions Lint Runner

This utility is a GitHub Action designed to lint and validate your repository's GitHub Actions workflows (`.github/workflows/*.yml`). It uses the `action-validator` tool to catch common errors and enforce best practices, ensuring your automation is robust and reliable.

## Usage

To use this action, add the following to your workflow file (e.g., `.github/workflows/lint-actions.yml`):

```yaml
name: Lint GitHub Actions Workflows

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  lint_actions:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Run GitHub Actions Lint Runner
        uses: polsala/ApocalypsAI/utils/nightly-gh-action-lint-runner@main
        with:
          workflow_path: '.github/workflows/' # Optional: specify a different path if your workflows are elsewhere
```

## Inputs

*   `workflow_path` (optional): The path to the directory containing your GitHub Actions workflow files. Defaults to `.github/workflows/`.

## Outputs

This action does not produce any explicit outputs, but it will fail the job if any linting errors are found.

## Development & Testing

This utility is built as a self-contained GitHub Action. The core logic is a simple shell script that leverages the `action-validator` tool. Tests are included to verify the script's behavior in isolation.
