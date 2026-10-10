# Nightly Temporal Title Tamer

## Overview

The `nightly-temporal-title-tamer` is a whimsical GitHub Action designed to maintain chronological stability within your repository's Pull Request titles. It scans PR titles for keywords that suggest 'temporal anomalies' (e.g., time travel, paradoxes, future fixes, past regressions) and, if detected, posts a playful comment on the PR, gently reminding the author to keep their timelines in order.

This utility helps foster a consistent and stable narrative around changes, preventing accidental temporal distortions in your project's history.

## How it Works

1.  **Trigger**: The action runs on `pull_request` events (e.g., `opened`, `synchronize`, `reopened`).
2.  **Scan**: It extracts the PR title and compares it against a configurable list of 'anomaly keywords'.
3.  **Detect**: If any keyword is found in the title (case-insensitive), a 'temporal anomaly' is detected.
4.  **Comment**: A pre-defined, whimsical comment is posted on the Pull Request, including the detected title.
5.  **Output**: Sets an `anomaly-detected` output variable for further workflow logic.

## Usage

To use this action, add a step to your GitHub Actions workflow (e.g., in `.github/workflows/temporal-check.yml`):

```yaml
name: Temporal Title Check

on:
  pull_request:
    types: [opened, synchronize, reopened]

jobs:
  check_pr_title:
    runs-on: ubuntu-latest
    steps:
      - name: Temporal Title Tamer
        uses: polsala/ApocalypsAI/.github/actions/nightly-temporal-title-tamer@main # Adjust path if needed
        with:
          github-token: ${{ secrets.GITHUB_TOKEN }}
          # Optional: Customize anomaly keywords (comma-separated)
          # anomaly-keywords: 'time,future,past,paradox,chronos,epoch,temporal,anachronism,revert,forward,backward,timeline,rift,glitch,quantum'
          # Optional: Customize the comment template
          # comment-template: |
          #   Oh dear, it seems your PR title "{title}" has caused a ripple in the spacetime continuum!
          #   Please ensure your changes are chronologically aligned to prevent catastrophic paradoxes.
```

### Inputs

*   `github-token`: **(Required)** Your GitHub token, usually `${{ secrets.GITHUB_TOKEN }}`, to allow the action to post comments.
*   `anomaly-keywords`: (Optional) A comma-separated string of keywords to detect. Defaults to `time,future,past,paradox,chronos,epoch,temporal,anachronism,revert,forward,backward,timeline,rift,glitch`.
*   `comment-template`: (Optional) A multiline string template for the comment to post. Use `{title}` as a placeholder for the PR title. Defaults to a whimsical message.

### Outputs

*   `anomaly-detected`: A boolean (`true` or `false`) indicating whether a temporal anomaly was detected in the PR title.

## Development & Testing

This action is built with Node.js. To run tests locally:

1.  Navigate to the `nightly-temporal-title-tamer` directory.
2.  Install dependencies: `npm install`
3.  Run tests: `npm test`

Tests use `jest` and mock the `@actions/core` and `@actions/github` modules to ensure deterministic and offline execution.
