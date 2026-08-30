# Nightly GitHub Action Lint Bot

A whimsical yet practical GitHub Action designed to automatically lint and validate your `.github/workflows/*.yml` files. It helps catch common errors, enforce best practices, and ensure your automation is as robust as a well-fortified bunker.

## Purpose

In the chaotic landscape of CI/CD, even the most well-intentioned workflows can fall prey to syntax errors, misconfigurations, or suboptimal patterns. This action acts as a vigilant guardian, scanning your workflow files on each commit or pull request to provide early feedback and prevent potential disruptions.

## Features

*   **Syntax Validation**: Checks for basic YAML syntax errors.
*   **Common Pattern Checks**: Identifies potentially problematic or inefficient workflow patterns (e.g., missing `jobs`, redundant steps, insecure defaults).
*   **Best Practice Suggestions**: Offers guidance on improving workflow readability and maintainability.
*   **Customizable Rules**: (Future enhancement) Ability to define custom linting rules.

## Usage

To integrate this action into your repository, add the following to your `.github/workflows/lint_workflows.yml` (or any other workflow file):

```yaml
name: Workflow Linting

on:
  push:
    paths:
      - ".github/workflows/**"
  pull_request:
    paths:
      - ".github/workflows/**"

jobs:
  lint_workflows:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Run Nightly GitHub Action Lint Bot
        uses: polsala/ApocalypsAI/utils/nightly-gh-action-lint-bot@main
        with:
          # Optional: Specify a path to lint if not the entire .github/workflows directory
          # workflow_path: ".github/workflows/my_specific_workflow.yml"
          # Optional: Set to 'true' to fail the job on any linting issues
          fail_on_error: true
```

## Inputs

*   `workflow_path` (optional): A glob pattern or specific path to the workflow file(s) to lint. Defaults to `".github/workflows/*.yml"`.
*   `fail_on_error` (optional): If `true`, the action will fail the job if any linting errors or warnings are found. Defaults to `false`.

## Outputs

This action primarily reports issues as annotations on the relevant lines in your workflow files. If `fail_on_error` is `true`, it will also cause the job to fail.

## Development & Testing

This action is built using a simple shell script and leverages existing GitHub Actions tools. Tests are included to ensure its functionality.

To run tests locally:

1.  Navigate to the `utils/nightly-gh-action-lint-bot/tests` directory.
2.  Execute `bash run_tests.sh`.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
