# Nightly GitHub Actions Dependency Checker

This GitHub Action scans your repository's `.github/workflows/` directory to identify and report on outdated dependencies used within your GitHub Actions workflows.

## Purpose

Keeping GitHub Actions workflows up-to-date with the latest dependency versions is crucial for security and performance. This action automates the process of identifying potential outdated actions, allowing you to proactively manage your CI/CD pipeline.

## Inputs

*   `workflow_path`:
    *   Description: The path to the directory containing your GitHub Actions workflows.
    *   Required: `true`
    *   Default: `.github/workflows/`

## Outputs

*   `outdated_dependencies`:
    *   Description: A JSON string listing any outdated dependencies found.
    *   Example: `{"actions/checkout": "v3", "actions/setup-node": "v2"}`

## Usage

```yaml
name: Dependency Check

on: [push, pull_request]

jobs:
  check_dependencies:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Run Dependency Checker
        id: dependency_check
        uses: polsala/ApocalypsAI/nightly-gh-action-dependency-check@main # Replace with actual repo/tag
        with:
          workflow_path: '.github/workflows/'

      - name: Report Outdated Dependencies
        run: |
          echo "Outdated Dependencies Found: ${{ steps.dependency_check.outputs.outdated_dependencies }}"
        if: steps.dependency_check.outputs.outdated_dependencies != ''
```

## Development & Testing

This action is built using JavaScript and Node.js. Tests are included to ensure its functionality.

To run tests locally:

1.  Install dependencies: `npm install`
2.  Run tests: `npm test`
