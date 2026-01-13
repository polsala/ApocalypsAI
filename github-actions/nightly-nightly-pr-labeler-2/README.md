# Nightly PR Labeler

A tiny GitHub Action that automatically adds helpful labels to a pull request based on the files that were changed.

## Features

- Detects documentation changes (files in `docs/` or Markdown files) â adds `documentation` label
- Detects test changes (files in `tests/` or typical test file suffixes) â adds `tests` label
- Detects CI/CD changes (files in `.github/` or any YAML file) â adds `ci` label
- Detects source code changes (common code extensions) â adds `code` label
- Works with any repository that provides a `repo-token` with `pull_requests` scope.

## Usage

Create a workflow file (e.g., `.github/workflows/pr-labeler.yml`) and add the following step to your PR workflow:

```yaml
name: PR Labeler

on:
  pull_request:
    types: [opened, synchronize, reopened]

jobs:
  label:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Autoâlabel PR
        uses: ./nightly-pr-labeler
        with:
          repo-token: ${{ secrets.GITHUB_TOKEN }}
```

The action will run on every PR event, inspect the changed files and apply the appropriate labels.

## Inputs

| Name | Description | Required | Default |
|------|-------------|----------|---------|
| `repo-token` | GitHub token with permission to read PR files and add labels. Usually `{{ secrets.GITHUB_TOKEN }}`. | Yes | â |

## Development

The action is implemented in JavaScript and uses the official `@actions/*` packages. To run the tests locally:

```bash
npm install
npm test
```

## License

MIT
