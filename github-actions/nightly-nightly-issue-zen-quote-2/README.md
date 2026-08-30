# Issue Zen Quote Action

A whimsical GitHub Action that posts a random Zen‑style quote as a comment whenever a new issue is opened. Helps keep the community calm and inspired.

## Usage

```yaml
name: Issue Zen Quote
on:
  issues:
    types: [opened]

jobs:
  zen:
    runs-on: ubuntu-latest
    steps:
      - uses: ./.github/actions/issue-zen-quote
        with:
          github-token: ${{ secrets.GITHUB_TOKEN }}
```

## Inputs

- `github-token` (required): Token with repo scope to post comments.

## How it works

The action selects a random quote from an internal list and posts it as a comment on the newly opened issue.
