# Nightly PR Apocalypse Labeler

## Overview

`nightly-pr-apocalypse-labeler` is a **GitHub Action** that scans the title of a pull request for dramatic, end‑of‑world keywords (e.g., "apocalypse", "doom", "survival", "end of the world").
If any of these keywords are found, the action automatically adds the label **`apocalypse`** to the PR.

This whimsical utility helps teams keep track of PRs that deal with catastrophic scenarios—perfect for a post‑apocalyptic project or just for fun!

## Features

- Configurable list of trigger keywords (default includes common apocalypse‑themed words).
- Works with the built‑in `GITHUB_TOKEN` or a custom PAT.
- Fails gracefully with clear error messages.

## Usage

Add the following step to your workflow (e.g., `.github/workflows/pr-labeler.yml`):

```yaml
name: PR Apocalypse Labeler
on:
  pull_request:
    types: [opened, edited]

jobs:
  label:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Label apocalypse PRs
        uses: ./nightly-pr-apocalypse-labeler
        with:
          github-token: ${{ secrets.GITHUB_TOKEN }}
```

### Inputs

| Name | Description | Required | Default |
|------|-------------|----------|---------|
| `github-token` | Token with `issues:write` permission (usually `GITHUB_TOKEN`). | Yes | N/A |
| `keywords` | Comma‑separated list of trigger keywords (case‑insensitive). | No | `apocalypse,doom,survival,end of the world,catastrophe` |

### Outputs

The action does not produce outputs, but it will log its actions to the workflow console.

## Development

The action is implemented in JavaScript (Node.js) and uses the official `@actions/core` and `@actions/github` packages.

Run tests locally with:

```bash
npm install
npm test
```

## License

MIT © ApocalypsAI
