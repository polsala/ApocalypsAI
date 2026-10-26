# GitHub Actions Workflow Linter

This GitHub Action provides a robust way to lint and validate your GitHub Actions workflow files (`.github/workflows/*.yml`). It helps catch common syntax errors, potential issues, and enforces best practices before your workflows are even triggered.

## Features

*   Validates YAML syntax for workflow files.
*   Checks for common misconfigurations and potential pitfalls.
*   Provides clear error messages to guide remediation.

## Usage

To use this action in your workflow, add the following to your `.github/workflows/lint-workflows.yml` (or any other workflow file):

```yaml
name: Lint Workflows

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Run Workflow Linter
        uses: polsala/ApocalypsAI/nightly-gh-action-lint-runner@v1.0.0 # Replace with actual tag/branch
        with:
          workflow_path: '.github/workflows/' # Optional: Specify a directory to lint

```

## Inputs

| Name | Description | Required | Default | 
|---|---|---|---| 
| `workflow_path` | The path to the directory containing your GitHub Actions workflow files. | no | `.github/workflows/` | 

## Outputs

This action does not produce any explicit outputs. It will fail the job if any linting errors are found.

## Development & Testing

This action is built using a simple shell script and relies on `yamllint`. To test locally:

1.  Clone the repository.
2.  Install `yamllint`: `pip install yamllint`
3.  Run the `lint_workflows.sh` script from the root of the repository.

Tests are included in the `tests/` directory and can be run using `pytest` (install with `pip install pytest`).
