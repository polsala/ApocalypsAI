# Nightly Issue Zen Quote Commenter

## Overview

`nightly-issue-zen-quote-commenter` is a lightweight GitHub Action that automatically posts a zen‑style quote as a comment whenever a new issue is opened. It adds a bit of calm (or chaos) to the issue tracker without any manual effort.

## Features
- Triggers on `issues: opened` events.
- Picks a quote from a curated list of zen sayings.
- Posts the quote as a comment using the repository's `GITHUB_TOKEN`.
- Pure Bash implementation – no extra runtime dependencies.

## Usage

Add the following step to your workflow (or create a dedicated workflow file):

```yaml
name: Zen Quote on New Issues
on:
  issues:
    types: [opened]

jobs:
  zen-comment:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repository
        uses: actions/checkout@v3

      - name: Post Zen Quote
        uses: ./github-actions/nightly-issue-zen-quote-commenter
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

The action is referenced via a relative path (`./github-actions/nightly-issue-zen-quote-commenter`) because it lives inside the same repository.

## Inputs & Outputs

This action does not require any inputs or produce outputs. All configuration is handled via environment variables automatically provided by GitHub Actions (`GITHUB_EVENT_PATH`, `GITHUB_REPOSITORY`, `GITHUB_TOKEN`).

## Testing

A deterministic Bash test is provided under `tests/run_test.sh`. It mocks `curl`, fixes the random seed, and verifies that the expected quote is sent to the GitHub API.

## License

MIT © ApocalypsAI
