# Nightly Chrono-Guard

A GitHub Action designed to detect temporal inconsistencies and whimsical paradoxes within Pull Request titles and their associated commit messages. This utility helps maintain chronological sanity in your repository, flagging potential time-travel mishaps or simple date-related errors that could confuse future historians (or just your teammates).

## 🌌 Features

*   **Keyword Detection**: Scans PR titles and commit messages for a curated list of "temporal anomaly" keywords (e.g., "time travel", "flux capacitor", "retroactive patch").
*   **Future Year Anomaly**: Flags years mentioned in the text that are more than 2 years in the future relative to the current year.
*   **Past Year Anomaly**: Flags years mentioned in the text that are more than 5 years in the past relative to the current year.
*   **Informative Outputs**: Provides `is-anomalous` boolean output and `anomaly-details` string output with specific findings.
*   **Whimsical Warnings**: Issues a GitHub Action warning if anomalies are detected, encouraging review.

## 🚀 Usage

To integrate the Nightly Chrono-Guard into your workflow, add a step to your `.github/workflows/your-workflow.yml` file. This action is typically run on `pull_request` events.

```yaml
name: PR Chronology Check

on:
  pull_request:
    types: [opened, reopened, synchronize]

jobs:
  chrono_check:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
        # Fetch all commit messages for the PR
        with:
          fetch-depth: 0

      - name: Get PR details
        id: pr_details
        run: |
          PR_TITLE="${{ github.event.pull_request.title }}"
          echo "pr_title=$PR_TITLE" >> "$GITHUB_OUTPUT"

          # Get all commit messages for the PR
          COMMIT_MESSAGES=$(git log --format=%B --no-merges ${{ github.event.pull_request.base.sha }}..${{ github.event.pull_request.head.sha }})
          # Escape newlines for multi-line output
          ESCAPED_COMMIT_MESSAGES="${COMMIT_MESSAGES//$'
'/'%0A'}"
          echo "commit_messages=$ESCAPED_COMMIT_MESSAGES" >> "$GITHUB_OUTPUT"

      - name: Run Nightly Chrono-Guard
        id: chrono-guard
        uses: polsala/ApocalypsAI/github-actions/nightly-chrono-guard@main # Adjust path if needed
        with:
          pr-title: ${{ steps.pr_details.outputs.pr_title }}
          commit-messages: ${{ steps.pr_details.outputs.commit_messages }}
          # current-year: '2024' # Optional: specify a fixed year for testing or specific contexts
```

### Inputs

*   `pr-title` (required): The title of the Pull Request.
*   `commit-messages` (required): A newline-separated string of commit messages for the PR.
*   `current-year` (optional): The current year to use for temporal checks. If not provided, the action will use the system's current year. Useful for deterministic testing.

### Outputs

*   `is-anomalous`: `true` if temporal anomalies were detected, `false` otherwise.
*   `anomaly-details`: A newline-separated string detailing all detected temporal anomalies.

## 🧪 Development & Testing

To run tests locally:

1.  Navigate to the `github-actions/nightly-chrono-guard` directory.
2.  Install dependencies: `npm install`
3.  Run tests: `npm test`

The tests use `jest` and mock the `@actions/core` library to ensure deterministic and offline execution.

## 📜 License

This utility is released under the MIT License.
