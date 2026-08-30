# Nightly GitHub Action Lint Checker

This GitHub Action provides a whimsical yet robust way to ensure your GitHub Actions workflow YAML files are clean, consistent, and follow best practices. It leverages a simple linting approach to catch common mistakes before they cause unexpected behavior.

## Features

*   **YAML Syntax Check**: Ensures the YAML is valid.
*   **Common Pattern Detection**: Looks for potentially problematic or non-idiomatic patterns.
*   **Customizable Rules (Future)**: While currently opinionated, future versions could allow custom rule sets.
*   **Self-Contained**: Runs as a standard GitHub Action.

## Usage

Add this action to your `.github/workflows/` directory. It's designed to run on pull requests targeting your main branch.

```yaml
name: Lint GitHub Workflows

on:
  pull_request:
    branches: [ main ]
    paths:
      - ".github/workflows/*.yml"

jobs:
  lint_workflows:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Run Nightly GitHub Action Lint Checker
        uses: polsala/ApocalypsAI/utils/nightly-gh-action-lint-checker@main
        with:
          workflow_path: ".github/workflows/"
```

## Inputs

*   `workflow_path` (optional): The directory containing the GitHub Actions workflow YAML files to lint. Defaults to `.github/workflows/`.

## Outputs

This action does not produce explicit outputs, but it will fail the job if any linting errors are found.

## Development & Testing

This utility is built as a self-contained GitHub Action. Tests are included within the `tests/` directory and can be run locally using `act` or within a GitHub Actions environment.
