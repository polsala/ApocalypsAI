# Nightly GitHub Actions Lint Bot

This utility is a GitHub Action designed to automatically lint and validate your `.github/workflows/*.yml` files. It helps ensure your CI/CD pipelines are well-formed, syntactically correct, and adhere to common best practices.

## Purpose

As the ApocalypsAI project grows, so does the complexity of its GitHub Actions. This bot acts as a vigilant guardian, ensuring that all workflow files are valid and free from common errors before they can cause unexpected issues.

## How it Works

The action uses the `action-validator` tool to perform static analysis on your workflow files. It checks for syntax errors, deprecated syntax, and provides suggestions for improvement.

## Usage

To use this action, add the following to your `.github/workflows/lint_workflows.yml` file:

```yaml
name: Lint Workflows

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

      - name: Run Nightly GitHub Actions Lint Bot
        uses: polsala/ApocalypsAI/.github/workflows/nightly-gh-action-lint-bot@main # Replace 'main' with the branch/tag you want to use
        with:
          # Optional: Specify a path to your workflows if they are not in .github/workflows/
          # workflow_path: 'path/to/your/workflows'
          # Optional: Set to 'true' to fail the job on warnings (default is 'false')
          # fail_on_warnings: 'true'
```

## Inputs

*   `workflow_path` (optional): The directory containing your GitHub Actions workflow files. Defaults to `.github/workflows/`.
*   `fail_on_warnings` (optional): If set to `true`, the action will fail the job even if only warnings are found. Defaults to `false`.

## Outputs

This action does not produce any explicit outputs, but it will fail the job if linting errors are found.

## Testing

This action is tested using a mock GitHub Actions environment. The tests ensure that the action correctly identifies valid and invalid workflow files.
