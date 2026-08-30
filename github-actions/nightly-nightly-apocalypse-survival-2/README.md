# Apocalyptic Survival Tip Action

A GitHub Action that posts a random whimsical survival tip as a comment on a pull request. Useful for adding fun to PR reviews.

## Usage

```yaml
name: Add Survival Tip
on:
  pull_request:
    types: [opened, reopened]

jobs:
  tip:
    runs-on: ubuntu-latest
    steps:
      - uses: ./.github/actions/nightly-apocalypse-survival-tip
        with:
          github-token: ${{ secrets.GITHUB_TOKEN }}
```

## Inputs

- `github-token` (required): Token with repo scope.

## How it works

The action selects a tip from a built‑in list and posts it as a comment on the PR using the GitHub REST API.
