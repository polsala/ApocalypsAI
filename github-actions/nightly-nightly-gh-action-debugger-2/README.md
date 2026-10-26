# Nightly GitHub Actions Debugger

This utility provides a GitHub Actions workflow designed to help diagnose issues within other GitHub Actions workflows. It captures and displays crucial environment variables, runner details, and context information, making it easier to pinpoint the source of unexpected behavior.

## Purpose

When a GitHub Actions workflow behaves unexpectedly, it can be challenging to understand the exact environment it's running in. This workflow acts as a diagnostic tool, printing out a comprehensive snapshot of the execution context. This information can then be used to compare against expected conditions or to identify subtle differences that might be causing problems.

## Usage

To use this workflow, simply add it to your repository's `.github/workflows/` directory. You can trigger it manually or integrate it into other workflows as a debugging step.

**Example Workflow Integration:**

```yaml
name: My Workflow

on: [push]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Run my build steps
        run: echo "Building..."

      - name: Debugging step (optional)
        uses: polsala/ApocalypsAI/.github/workflows/nightly-gh-action-debugger@main
        with:
          # Optional: Add specific context or messages
          debug_message: "Checking environment after build"
```

## Inputs

*   `debug_message` (optional): A custom message to display at the beginning of the debug output.

## Outputs

This workflow does not produce any explicit outputs that are consumed by other jobs. Its primary function is to log detailed information to the GitHub Actions run logs.

## How it Works

The workflow leverages a simple shell script that prints out a variety of environment variables and context information available within a GitHub Actions runner. This includes:

*   Standard environment variables (`GITHUB_` prefixed variables).
*   Runner environment details.
*   Current working directory.
*   Git information.

## Testing

This workflow includes a basic test that verifies the presence of key environment variables when the workflow is executed. The test is designed to be deterministic and run offline by relying on the standard GitHub Actions environment variables.
