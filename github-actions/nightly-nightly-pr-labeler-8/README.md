# Nightly PR Labeler

## Overview

A whimsical yet useful GitHub Action that automatically adds labels to pull requests based on keywords found in the PR title. It helps keep your repository tidy without manual effort.

## How it works

The action examines the `PR_TITLE` environment variable (populated from the pull request title) and applies the following rules:

- titles containing **bug** → label `bug`
- titles containing **feature** or **feat** → label `enhancement`
- titles containing **doc** or **docs** → label `documentation`

If multiple keywords match, all corresponding labels are added.

## Setup

1. Add the composite action to your repository under `.github/actions/pr-labeler/` using the files provided in this utility.
2. Create a workflow that calls the action on `pull_request_target` events.

```yaml
name: Auto PR Labeler
on:
  pull_request_target:
    types: [opened, edited, reopened]

jobs:
  label:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v3
      - name: Run PR Labeler
        uses: ./.github/actions/pr-labeler
        env:
          PR_TITLE: ${{ github.event.pull_request.title }}
```

## Testing

Run the provided test script locally:

```bash
bash tests/test_labeler.sh
```

The script simulates different PR titles and verifies the expected labels are printed.

## License

MIT
