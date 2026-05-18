# Nightly GitHub Actions Lint Checker

This GitHub Action is designed to automatically lint and validate your `.github/workflows/*.yml` files. It checks for common syntax errors, potential pitfalls, and adherence to best practices, helping to ensure your CI/CD pipelines are robust and reliable.

## Features

*   Validates YAML syntax for workflow files.
*   Checks for common misconfigurations and potential issues.
*   Enforces basic best practices for GitHub Actions.
*   Provides clear error messages to guide remediation.

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

      - name: Run GitHub Actions Lint Checker
        uses: polsala/ApocalypsAI/utils/nightly-gh-action-lint-checker@main
        with:
          # Optional: Specify a path to search for workflow files (defaults to .github/workflows/)
          # workflow_path: '.github/workflows/'
          # Optional: Set to 'true' to fail the job if no workflow files are found
          # fail_if_no_workflows: 'false'
          # Optional: Set to 'true' to enable verbose logging
          # verbose: 'false'
```

## Inputs

| Name | Description | Required | Default | 
|---|---|---|---| 
| `workflow_path` | The directory to search for GitHub Actions workflow files. | `false` | `.github/workflows/` | 
| `fail_if_no_workflows` | If `true`, the action will fail if no workflow files are found in the specified path. | `false` | `false` | 
| `verbose` | If `true`, enable verbose logging for debugging. | `false` | `false` | 

## Outputs

This action does not produce any explicit outputs, but it will fail the job if linting errors are found.

## Development & Testing

This utility is built as a GitHub Action. To test it locally, you can use the `act` tool or run it within a GitHub Actions environment.

Tests are included in the `tests/` directory and can be run using `pytest`.
