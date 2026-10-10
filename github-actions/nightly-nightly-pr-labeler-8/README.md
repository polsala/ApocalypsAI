# Nightly PR Labeler

## Overview

A reusable GitHub Actions workflow that automatically adds labels to a pull request based on the files changed. Define a mapping of glob patterns to labels, and the workflow will apply the appropriate labels when the PR is opened or synchronized.

## Usage

Add the following to your repository's workflow directory (e.g., `.github/workflows/auto-label.yml`):

```yaml
name: Auto‑Label PR
on:
  pull_request_target:
    types: [opened, synchronize]

jobs:
  label:
    uses: ./github-actions/nightly-pr-labeler/workflow.yml
    with:
      label_map: '{"src/**/*.py":"python","docs/**/*.md":"documentation","tests/**/*.py":"tests"}'
    secrets:
      GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

## Inputs

- `label_map` (required): JSON string where keys are glob patterns (compatible with `minimatch`) and values are the label to apply when any changed file matches the pattern.

## How it works

1. The workflow checks out the PR's code.
2. It determines the list of changed files using `git diff --name-only ${{ github.event.pull_request.base.sha }} ${{ github.sha }}`.
3. For each pattern in `label_map`, if any changed file matches, the corresponding label is added via the GitHub REST API.

## Permissions

The workflow requires the `contents: read` and `pull_requests: write` permissions (provided by the default `GITHUB_TOKEN`).

## License

MIT
