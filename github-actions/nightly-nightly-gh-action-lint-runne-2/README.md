# Nightly GitHub Actions Lint Runner

This utility is a GitHub Action designed to lint and validate your repository's GitHub Actions workflows. It helps ensure your workflows are syntactically correct and adhere to best practices, preventing potential runtime errors and unexpected behavior.

## Features

*   **Workflow Validation**: Checks for syntax errors in `.github/workflows/*.yml` files.
*   **Best Practice Checks**: Identifies common anti-patterns and potential issues.
*   **Customizable**: Allows specifying which workflows to include or exclude.

## Usage

To use this action in your workflow, add the following to your `.github/workflows/lint_workflows.yml` (or any other workflow file):

```yaml
name: Lint GitHub Workflows

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  lint_workflows:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Run Workflow Linter
        uses: polsala/ApocalypsAI/nightly-gh-action-lint-runner@main
        with:
          # Optional: Specify a glob pattern to include specific workflow files
          # include_workflows: "**/*.yml"
          # Optional: Specify a glob pattern to exclude specific workflow files
          # exclude_workflows: ".github/workflows/generated-*.yml"
```

## Inputs

*   `include_workflows` (optional): A glob pattern to specify which workflow files to lint. Defaults to all `.github/workflows/*.yml`.
*   `exclude_workflows` (optional): A glob pattern to specify which workflow files to exclude from linting.

## Outputs

*   This action does not produce any explicit outputs, but it will fail the job if any linting errors are found.
