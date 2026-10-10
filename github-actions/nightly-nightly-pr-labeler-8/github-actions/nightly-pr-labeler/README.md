# Nightly PR Labeler

## Overview

A tiny GitHub Action that automatically adds a label to a pull request based on the words found in its title.  It helps keep your PR board tidy without any manual effort.

## How it works

1. The workflow triggers on `pull_request` events (opened, reopened, edited).
2. A Bash script reads the event payload, extracts the PR title, and decides on a label:
   * titles containing **feat** → `feature`
   * titles containing **fix** → `bug`
   * titles containing **docs** → `documentation`
   * anything else → `misc`
3. The script uses the `gh` CLI to apply the label.

## Setup

Add the workflow file located at `.github/workflows/pr-labeler.yml` to your repository (or copy the whole `github-actions/nightly-pr-labeler` directory). No additional secrets are required – the default `GITHUB_TOKEN` is sufficient.

## Testing

Run the provided Bash test locally:

```bash
cd github-actions/nightly-pr-labeler
tests/test_label_pr.sh
```

The test mocks the `gh` CLI and verifies that the correct label is chosen for a sample PR title.

## License

MIT © ApocalypsAI
