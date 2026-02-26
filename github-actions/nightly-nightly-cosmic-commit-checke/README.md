# Nightly Cosmic Commit Checker

A GitHub Action to ensure your commit messages are in 'cosmic alignment' with your project's celestial standards. This utility allows you to define required and forbidden keywords, helping maintain consistent and meaningful commit history.

## Features

*   **Keyword Enforcement**: Define keywords that must be present in at least one commit message within a range.
*   **Forbidden Terms**: Specify keywords that must not appear in any commit message.
*   **Configurable Failure**: Choose whether the action should fail the workflow on misalignment.
*   **Mockable for Tests**: Supports reading commit messages from a file for deterministic testing.

## Usage

To use the `nightly-cosmic-commit-checker` in your workflow, add a step like this:

```yaml
name: Check Cosmic Alignment
on:
  push:
    branches:
      - main
  pull_request:
    branches:
      - main

jobs:
  check_commits:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Perform Cosmic Commit Check
        uses: polsala/ApocalypsAI/github-actions/nightly-cosmic-commit-checker@main # Replace 'main' with your branch/tag
        id: cosmic_check
        with:
          commit_range: 'HEAD~5..HEAD' # Check the last 5 commits
          required_keywords: 'feat,refactor'
          forbidden_keywords: 'WIP,temp'
          fail_on_mismatch: 'true'

      - name: Report Status
        run: |
          echo "Cosmic Alignment Status: ${{ steps.cosmic_check.outputs.alignment_status }}"
          echo "Required Keywords Found: ${{ steps.cosmic_check.outputs.required_found }}"
          echo "Forbidden Keywords Found: ${{ steps.cosmic_check.outputs.forbidden_found }}"
          if [ "${{ steps.cosmic_check.outputs.alignment_status }}" == "misaligned" ]; then
            echo "Warning: Commit messages are misaligned!"
          fi
```

## Inputs

*   `commit_range` (optional, default: `HEAD~5..HEAD`):
    The Git commit range to analyze (e.g., `HEAD~5..HEAD` for the last 5 commits, `main..HEAD` for changes on the current branch relative to `main`). This input is ignored if `commit_messages_file` is provided.
*   `required_keywords` (optional, default: `""`):
    A comma-separated list of keywords. At least one of these keywords MUST be present in at least one commit message within the `commit_range` for the check to pass.
*   `forbidden_keywords` (optional, default: `""`):
    A comma-separated list of keywords. NONE of these keywords MUST be present in ANY commit message within the `commit_range` for the check to pass.
*   `fail_on_mismatch` (optional, default: `true`):
    If `true`, the action will fail (exit with a non-zero code) if any required keywords are missing or any forbidden keywords are found. If `false`, it will only report the status.
*   `commit_messages_file` (optional, default: `""`):
    **For testing/mocking purposes.** Path to a file containing commit messages, one per line. If provided, the action will read messages from this file instead of using `git log`. # Mock rationale: Allows deterministic and offline testing by providing predefined commit message content.

## Outputs

*   `alignment_status`:
    The overall status of the cosmic alignment check. Possible values: `aligned` or `misaligned`.
*   `required_found`:
    A comma-separated list of `required_keywords` that were successfully found in the commit messages.
*   `forbidden_found`:
    A comma-separated list of `forbidden_keywords` that were found in the commit messages.

## Development & Testing

See `tests/test_action.yml` for examples of how to test this action locally using `act` or in a CI environment.
