# Nightly Apocalypse Quote Commenter

A GitHub Action that posts a random apocalyptic‑themed quote as a comment on a pull request. Useful for adding a bit of flair to PR reviews.

## Usage

```yaml
name: Apocalyptic Quote
on:
  pull_request:
    types: [opened, reopened]

jobs:
  quote:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Post random quote
        uses: ./utils/github-actions/nightly-apocalypse-quote-commenter
        with:
          github-token: ${{ secrets.GITHUB_TOKEN }}
```

## Inputs

| Name | Description | Required |
|------|-------------|----------|
| github-token | Token with repo scope to post comment | true |

## How it works

The action selects a random quote from a built‑in list and uses the GitHub REST API to create a comment on the PR that triggered the workflow.
