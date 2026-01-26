# Nightly PR Labeler

A whimsical GitHub Action that automatically adds labels to a pull request based on the types of files changed.

## Features

- Detects Markdown files → adds `📚 docs‑drift`
- Detects Python source files → adds `🐍 python‑whirl`
- Detects test files (`*_test.py` or `.test` extensions) → adds `🧪 test‑tornado`
- Runs as a **composite** action, no external services required.

## Usage

```yaml
name: Auto‑label PRs
on:
  pull_request_target:
    types: [opened, synchronize]

jobs:
  label:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4
      - name: Run PR labeler
        uses: ./github-actions/nightly-pr-labeler
        with:
          github-token: ${{ secrets.GITHUB_TOKEN }}
```

## Inputs

| Name | Description | Required |
|------|-------------|----------|
| `github-token` | Token with `repo` scope to add labels via the GitHub API. | Yes |

## How it works

The action reads the pull‑request event payload (available at `$GITHUB_EVENT_PATH`), extracts the list of changed files, determines which whimsical labels apply, and prints them. In a real deployment you could extend the script to call the GitHub REST API to actually apply the labels.

## Testing

Run the provided test script locally:

```bash
bash tests/test_labeler.sh
```

The test uses a mocked event payload and verifies the expected label output.
