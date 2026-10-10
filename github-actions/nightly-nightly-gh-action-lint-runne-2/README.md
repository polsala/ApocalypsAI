# Nightly GitHub Actions Lint Runner

This GitHub Action is designed to automatically lint and validate your `.github/workflows/*.yml` files. It helps ensure your CI/CD workflows are syntactically correct and adhere to best practices, preventing common errors before they cause issues.

## Features

*   Validates YAML syntax for GitHub Actions workflows.
*   Checks for common misconfigurations and potential issues.
*   Provides clear error messages to guide remediation.

## Usage

To use this action, add the following to your GitHub Actions workflow file (e.g., `.github/workflows/lint-workflows.yml`):

```yaml
name: Lint Workflows

on:
  push:
    branches: [ main ]
  pull_request:

jobs:
  lint_workflows:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Run Workflow Linting Action
        uses: polsala/ApocalypsAI/nightly-gh-action-lint-runner@main
        with:
          workflow_path: '.github/workflows/'
```

## Inputs

| Name | Description | Required | Default |
|---|---|---|---|
| `workflow_path` | The directory containing the GitHub Actions workflow files to lint. | no | `.github/workflows/` |

## Outputs

This action does not produce any explicit outputs, but it will fail the job if any linting errors are found.

## Development & Testing

This utility is built as a Docker container and tested using `docker build` and `docker run` commands. The tests simulate different scenarios of valid and invalid workflow files.
