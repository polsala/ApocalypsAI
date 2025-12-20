# Nightly Apocalypse Badge

A tiny GitHub Action that watches pull‑request events and, when a PR carries the `apocalypse` label, posts a fun badge comment.

## Features

- Detects the `apocalypse` label on PRs.
- Posts a comment with a custom shield badge (powered by shields.io).
- Works as a JavaScript action (Node.js 12+).

## Usage

Create a workflow file (e.g. `.github/workflows/apocalypse-badge.yml`) with the following content:

```yaml
name: Apocalypse Badge
on:
  pull_request:
    types: [opened, labeled, unlabeled, synchronize]

jobs:
  badge:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Add Apocalypse Badge
        uses: ./github-actions/nightly-apocalypse-badge
        with:
          github-token: ${{ secrets.GITHUB_TOKEN }}
```

> **Note**: The action expects a `github-token` input with permission to comment on PRs (the default `GITHUB_TOKEN` works).

## Inputs

| Name | Description | Required | Default |
|------|-------------|----------|---------|
| `github-token` | Token used to authenticate with the GitHub API. | Yes | – |

## How it works

The action reads the event payload, checks if the PR has the `apocalypse` label, and if so, uses the Octokit REST client to create a comment containing the badge:

```
![Apocalypse](https://img.shields.io/badge/Apocalypse-⚔️-red)
```

If the label is removed, the action does nothing (it does not delete previous comments).

## Development

```bash
# Install dependencies
npm install

# Run tests
npm test
```

## License

MIT © ApocalypsAI
