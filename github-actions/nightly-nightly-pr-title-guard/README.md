# PR Title Guard

A lightweight GitHub Action that ensures pull request titles meet a configurable minimum length. Prevents vague or empty titles, encouraging clearer communication.

## Usage

```yaml
name: PR Title Guard
on:
  pull_request:
    types: [opened, edited, reopened]

jobs:
  title-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Check PR title length
        uses: ./  # assuming the action lives at the repository root
        with:
          min_length: 15
```

## Inputs

- `min_length` (default: `10`): Minimum number of characters required for the PR title.

## How it works

The action reads the event payload from `GITHUB_EVENT_PATH`, extracts the PR title, and fails the job if the title is shorter than `min_length`.
