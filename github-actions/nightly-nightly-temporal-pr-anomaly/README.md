# Nightly Temporal PR Anomaly Check

This GitHub Action scans Pull Request titles and commit messages for keywords related to temporal anomalies, time travel, and paradoxes. If such keywords are detected, it will post a whimsical warning comment on the Pull Request, reminding contributors to be mindful of the spacetime continuum.

## 🚀 Usage

To use this action, add a step to your GitHub Actions workflow (e.g., on `pull_request` events):

```yaml
name: PR Temporal Anomaly Scan

on:
  pull_request:
    types: [opened, synchronize, reopened, edited]

jobs:
  temporal_check:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v3

      - name: Run Temporal Anomaly Check
        uses: polsala/ApocalypsAI/github-actions/nightly-temporal-pr-anomaly-check@main # Replace 'main' with your branch/tag
        with:
          github-token: ${{ secrets.GITHUB_TOKEN }}
```

### Inputs

*   `github-token`: **Required**. Your GitHub Token, usually `${{ secrets.GITHUB_TOKEN }}`, which grants the action permission to read PR details and post comments.

## 🕵️ How it Works

The action retrieves the Pull Request title and all associated commit messages. It then scans this text for a predefined list of keywords (e.g., "time travel", "paradox", "temporal shift"). If any keyword is found, a randomly selected, light-hearted warning message is posted as a comment on the PR.

## 🧪 Development & Testing

To run tests locally:

1.  Install dependencies: `npm install`
2.  Run tests: `npm test`

The tests use Jest and mock the `@actions/github` and `@actions/core` libraries to ensure deterministic and offline execution.
