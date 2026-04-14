# Issue Zen Quote Commenter

A GitHub Action that comments a random zen quote on every newly opened issue, bringing a moment of calm to your repository.

## Usage

```yaml
name: Zen Issue Commenter
on:
  issues:
    types: [opened]

jobs:
  comment:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Post Zen Quote
        uses: ./
        with:
          github-token: ${{ secrets.GITHUB_TOKEN }}
```

## Inputs

- `github-token` (required): Token with repo scope.

## How it works

The action selects a random quote from a built‑in list and posts it as a comment on the issue that triggered the workflow.
