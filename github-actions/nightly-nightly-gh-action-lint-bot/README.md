## Nightly GitHub Action Lint Bot

This utility provides a GitHub Actions workflow that automatically lints and validates other GitHub Actions workflows within the repository. It aims to catch common errors, enforce best practices, and ensure the overall health and reliability of your CI/CD pipelines.

### How it Works

The `nightly-gh-action-lint-bot` workflow is triggered on pushes to the `main` branch and on a daily schedule. It uses a combination of static analysis tools and custom checks to examine `.github/workflows/*.yml` files.

### Features

*   **Syntax Validation**: Checks for valid YAML syntax.
*   **Common Error Detection**: Identifies issues like missing `uses` or `run` keywords, incorrect indentation, and invalid event triggers.
*   **Best Practice Checks**: Flags potential improvements such as using specific versions for actions, avoiding hardcoded secrets, and ensuring clear job names.
*   **Dependency Checks**: Verifies that action versions are specified.

### Usage

This workflow is designed to run automatically. No explicit configuration is required for basic usage. It will automatically scan all files matching `.github/workflows/*.yml`.

### Example Workflow Trigger

```yaml
name: Nightly GitHub Action Lint Bot

on:
  push:
    branches: [ main ]
  schedule:
    # Runs at 03:00 UTC daily
    - cron: '0 3 * * *'

jobs:
  lint_actions:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Run GitHub Actions Lint Bot
        uses: ./utils/nightly-gh-action-lint-bot # This assumes the utility is checked out locally
        # If this were a published action, you'd use: uses: polsala/ApocalypsAI/utils/nightly-gh-action-lint-bot@main

```

### Contributing

Feel free to suggest improvements or add new linting rules by opening an issue or submitting a pull request.
