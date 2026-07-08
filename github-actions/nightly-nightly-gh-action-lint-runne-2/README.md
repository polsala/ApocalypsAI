# Nightly GitHub Action Lint Runner

This GitHub Action is designed to provide a whimsical yet robust way to lint and validate other GitHub Actions workflows within a repository. It helps ensure that your automation pipelines are well-formed and adhere to best practices, preventing unexpected failures.

## Features

*   **Workflow Validation**: Checks for syntax errors and common misconfigurations in `.github/workflows/*.yml` files.
*   **Linting**: Applies a set of predefined linting rules to ensure consistency and readability.
*   **Customizable Rules**: (Future enhancement) Ability to specify custom linting rules.
*   **Whimsical Output**: Provides friendly and encouraging feedback, even when issues are found.

## Usage

To use this action in your workflow, add the following to your `.github/workflows/your-workflow.yml` file:

```yaml
name: Lint GitHub Actions Workflows

on: [push, pull_request]

jobs:
  lint-actions:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Run GitHub Action Lint Runner
        uses: polsala/ApocalypsAI/utils/nightly-gh-action-lint-runner@main # Replace with the actual path or tag
        with:
          # Optional: Specify a path to lint if not the entire .github/workflows directory
          # workflow_path: '.github/workflows/my-specific-workflow.yml'
```

## Inputs

*   `workflow_path` (optional): A glob pattern or specific path to the workflow file(s) to lint. Defaults to `'.github/workflows/*.yml'`.

## Outputs

*   `lint_status`: The overall status of the linting process ('success' or 'failure').
*   `lint_summary`: A brief summary of the linting results.

## Development & Testing

This utility is built as a self-contained GitHub Action. Tests are included to ensure its functionality.

To run tests locally:

1.  Ensure you have Node.js and npm installed.
2.  Navigate to the `utils/nightly-gh-action-lint-runner` directory.
3.  Run `npm install`.
4.  Run `npm test`.
