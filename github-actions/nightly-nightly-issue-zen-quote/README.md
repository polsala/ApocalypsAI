# Nightly Issue Zen Quote

A whimsical GitHub Action that automatically comments a random Zen quote on every newly opened issue. Helps bring calm to the chaos of the issue tracker.

## Usage

Create a workflow in your repository that triggers on `issues` events and uses this action:

```yaml
name: Zen Issue Greeting
on:
  issues:
    types: [opened]

jobs:
  add-zen-quote:
    runs-on: ubuntu-latest
    steps:
      - uses: polsala/ApocalypsAI/github-actions/nightly-issue-zen-quote@v1
        with:
          token: ${{ secrets.GITHUB_TOKEN }}
```

## How it works

The action reads the issue payload, picks a random quote from a built‑in list, and posts it as a comment via the GitHub REST API.

## License

MIT
