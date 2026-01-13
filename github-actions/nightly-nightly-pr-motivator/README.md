# Nightly PR Motivator

A GitHub Action that posts a random motivational quote as a comment on a pull request. Useful for keeping contributors upbeat during code reviews.

## Usage

```yaml
name: PR Motivator
on:
  pull_request:
    types: [opened, reopened]

jobs:
  motivate:
    runs-on: ubuntu-latest
    steps:
      - uses: ./.github/actions/nightly-pr-motivator
        with:
          github-token: ${{ secrets.GITHUB_TOKEN }}
```

## Inputs

- `github-token` (required): Token with repo scope to post comment.

## How it works

The action selects a quote from `quotes.txt` using a deterministic pseudoârandom algorithm based on the PR number, ensuring the same PR always gets the same quote.

