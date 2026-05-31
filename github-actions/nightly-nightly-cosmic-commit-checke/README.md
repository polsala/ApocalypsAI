# Nightly Cosmic Commit Checker

This GitHub Action ensures that your commit messages are 'cosmically aligned' by checking for the presence of a specific 'cosmic blessing' keyword or phrase. It's a whimsical yet useful way to enforce custom commit message conventions, promote team culture, or simply add a fun gate to your pull requests.

## Features

*   **Customizable Blessing**: Define any keyword or phrase that must appear in commit messages.
*   **Flexible Enforcement**: Choose whether to simply report misalignment or fail the workflow step.
*   **Output for Downstream Actions**: Provides an `is_cosmically_aligned` output for conditional steps.

## Usage

To use this action, add it to your workflow file (e.g., `.github/workflows/pr_check.yml`).

```yaml
name: Cosmic Alignment Check
on:
  pull_request:
    types: [opened, synchronize, reopened, edited]
  push:
    branches: [ main, master ]

jobs:
  check_commit_message:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Get commit message (for PRs)
        id: get_pr_commit_message
        if: github.event_name == 'pull_request'
        run: |
          PR_COMMIT_MESSAGE="$(git log -1 --pretty=%B ${{ github.event.pull_request.head.sha }})"
          echo "commit_message=$PR_COMMIT_MESSAGE" >> "$GITHUB_OUTPUT"
        # Mock rationale: In a real workflow, this fetches the actual commit message.
        # For testing, we pass a static string directly.

      - name: Get commit message (for pushes)
        id: get_push_commit_message
        if: github.event_name == 'push'
        run: |
          PUSH_COMMIT_MESSAGE="$(git log -1 --pretty=%B ${{ github.sha }})"
          echo "commit_message=$PUSH_COMMIT_MESSAGE" >> "$GITHUB_OUTPUT"
        # Mock rationale: In a real workflow, this fetches the actual commit message.
        # For testing, we pass a static string directly.

      - name: Check Cosmic Alignment
        id: cosmic_check
        uses: polsala/ApocalypsAI/utils/nightly-cosmic-commit-checker@main # Replace 'main' with your branch/tag
        with:
          commit_message: ${{ steps.get_pr_commit_message.outputs.commit_message || steps.get_push_commit_message.outputs.commit_message }}
          required_blessing: 'Blessed by the Void'
          fail_on_misalignment: 'true'

      - name: Report Alignment Status
        if: always()
        run: |
          if [ "${{ steps.cosmic_check.outputs.is_cosmically_aligned }}" == "true" ]; then
            echo "✨ The latest commit is cosmically aligned! Proceed with confidence. ✨"
          else
            echo "⚠️ The latest commit is NOT cosmically aligned. Please add 'Blessed by the Void' to your commit message. ⚠️"
          fi
```

## Inputs

*   `commit_message` (required): The full commit message string to check.
*   `required_blessing` (required): The specific keyword or phrase that must be present in the commit message.
*   `fail_on_misalignment` (optional, default: `false`): Set to `true` to make the action fail if the `required_blessing` is not found. If `false`, the action will complete successfully but `is_cosmically_aligned` will be `false`.

## Outputs

*   `is_cosmically_aligned`: `true` if the `required_blessing` was found in the `commit_message`, `false` otherwise.
