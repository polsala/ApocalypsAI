# Nightly GitHub Action Lint Reporter

This GitHub Action lints all `.yaml` and `.yml` files within a repository and generates a summary report of any issues found. It's designed to catch common syntax errors and potential misconfigurations in your workflow and configuration files.

## Usage

This action can be used in your GitHub Actions workflows to automatically check your YAML files.

```yaml
name: YAML Lint Check

on: [push, pull_request]

jobs:
  lint-yaml:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Run YAML Lint Reporter
        uses: polsala/ApocalypsAI/nightly-gh-action-lint-reporter@main
        with:
          # Optional: Specify a path to search for YAML files (defaults to root)
          # search_path: '.github/workflows'
          # Optional: Set to 'true' to fail the workflow on any linting errors
          fail_on_error: 'true'
```

## Inputs

*   `search_path` (optional): The directory to search for YAML files. Defaults to the repository root.
*   `fail_on_error` (optional): If set to `true`, the action will fail the workflow if any linting errors are found. Defaults to `false`.

## Outputs

*   `lint_summary`: A string containing a summary of the linting results.
*   `has_errors`: A boolean indicating whether any linting errors were found (`true` or `false`).
