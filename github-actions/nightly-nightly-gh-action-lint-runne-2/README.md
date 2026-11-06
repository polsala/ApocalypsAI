# Nightly GitHub Actions Lint Runner

This utility provides a GitHub Action that automatically lints and validates your `.github/workflows/*.yml` files. It helps catch syntax errors, common misconfigurations, and potential issues before they cause runtime problems.

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
  lint-actions:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Run GitHub Actions Lint Runner
        uses: polsala/ApocalypsAI/utils/nightly-gh-action-lint-runner@main
        with:
          # Optional: Specify a path to your workflows directory if not .github/workflows
          # workflows_path: '.github/workflows'
          # Optional: Set to 'true' to fail the job on warnings as well as errors
          # fail_on_warnings: 'false'
```

## Inputs

*   `workflows_path` (optional): The path to the directory containing your GitHub Actions workflow files. Defaults to `.github/workflows`.
*   `fail_on_warnings` (optional): If set to `true`, the action will fail the job even if only warnings are found. Defaults to `false`.

## Outputs

This action does not produce any explicit outputs, but it will fail the job if linting errors are detected.
