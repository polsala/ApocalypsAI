# Nightly GitHub Action Lint Runner

This GitHub Action provides a whimsical yet robust way to lint and validate your GitHub Actions workflow YAML files. It ensures your automation is not only functional but also adheres to best practices, preventing unexpected `404`s from the void.

## Features

*   **YAML Linting**: Checks for basic YAML syntax errors.
*   **Workflow Validation**: Uses `action-validator` to check for common issues and best practices in your GitHub Actions workflows.
*   **Customizable**: Allows specifying which directories to scan.

## Usage

To use this action in your workflow, add the following to your `.github/workflows/your_workflow.yml` file:

```yaml
name: Lint GitHub Actions Workflows

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

      - name: Run Nightly GitHub Action Lint Runner
        uses: polsala/ApocalypsAI/utils/github-actions/nightly-gh-action-lint-runner@main
        with:
          workflow_paths: ['.github/workflows'] # Optional: Specify paths to scan, defaults to ['.github/workflows']
```

## Inputs

*   `workflow_paths` (Optional): A comma-separated string of paths to directories containing your GitHub Actions workflow YAML files. Defaults to `'.github/workflows'`.

## Outputs

This action does not produce any explicit outputs, but it will fail the job if any linting or validation errors are found.
