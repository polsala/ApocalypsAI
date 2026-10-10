# Nightly PR Blessing Bot

This GitHub Action adds a touch of post-apocalyptic whimsy to your Pull Request workflows. Depending on the PR's status (success, failure, or anything else), it will post a unique, encouraging, or observative comment, bringing a bit of light-heartedness to your CI/CD pipeline.

## Features

*   **Whimsical Affirmations**: Posts a celebratory message for successful PRs.
*   **Encouraging Retries**: Offers a hopeful message for failed PRs.
*   **Observative Comments**: Provides a neutral, cosmic observation for unknown statuses.
*   **Reusable**: Easily integrate into any workflow that needs to comment on a PR's outcome.

## Usage

To use this action, include it in your workflow after your build, test, or other status-determining jobs. You'll need to pass the PR number, its status, and a `GITHUB_TOKEN` with `pull-requests: write` permissions.

### Example Workflow: Blessing a PR after CI

This example demonstrates how to integrate the `nightly-pr-blessing-bot` into a typical CI workflow. The bot will comment on the PR based on the outcome of the `build_and_test` job.

```yaml
name: CI and PR Blessing

on:
  pull_request:
    branches: [ main ] # Trigger on PRs targeting the main branch

jobs:
  build_and_test:
    runs-on: ubuntu-latest
    outputs:
      status: ${{ steps.determine_status.outputs.status }}
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Run tests
        id: run_tests
        run: |
          echo "Running critical tests..."
          # Simulate a test run. Uncomment 'exit 1' to simulate a failure.
          # exit 1

      - name: Determine status
        id: determine_status
        run: |
          if [ ${{ steps.run_tests.outcome }} == 'success' ]; then
            echo "status=success" >> "$GITHUB_OUTPUT"
          else
            echo "status=failure" >> "$GITHUB_OUTPUT"
          fi

  bless_pr:
    runs-on: ubuntu-latest
    needs: build_and_test # This job depends on the build_and_test job
    if: always() # Ensure this job runs even if build_and_test fails
    steps:
      - name: Call PR Blessing Bot
        # If the action is in the same repository, use a relative path.
        # Otherwise, use 'polsala/ApocalypsAI/github-actions/nightly-pr-blessing-bot@main'
        uses: ./github-actions/nightly-pr-blessing-bot
        with:
          pr-number: ${{ github.event.pull_request.number }}
          pr-status: ${{ needs.build_and_test.outputs.status }} # Pass the status from the previous job
          github-token: ${{ secrets.GITHUB_TOKEN }}
```

## Inputs

| Input          | Description                                         | Required | Default |
| :------------- | :-------------------------------------------------- | :------- | :------ |
| `pr-number`    | The number of the Pull Request to comment on.       | `true`   |         |
| `pr-status`    | The status of the Pull Request (e.g., `"success"`, `"failure"`). | `true`   |         |
| `github-token` | GitHub token with `pull-requests: write` permissions. | `true`   |         |

## Outputs

| Output          | Description                                   |
| :-------------- | :-------------------------------------------- |
| `comment-message` | The exact message that was posted to the PR. |

## Development

### Testing Message Generation

The core logic for generating the whimsical messages is contained in `src/generate_message.sh`. This script can be tested independently and offline. Refer to `tests/test_generate_message.yml` for an example of how these tests are structured.
