# PR Keyword Labeler

A GitHub Action that scans pull‑request titles and bodies for user‑defined keywords and automatically adds whimsical labels.

## Usage

```yaml
name: PR Keyword Labeler
on:
  pull_request:
    types: [opened, edited, reopened]

jobs:
  label:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Label PR
        uses: ./ # path to this action
        with:
          token: ${{ secrets.GITHUB_TOKEN }}
          mapping: |
            bug:🐞 Bug
            feature:✨ Feature
            zombie:🧟‍♂️ Zombie
```

The action will add any matching labels to the PR.

## Inputs

- `token` – GitHub token with repo permissions (required).
- `mapping` – Multiline mapping of `keyword:label`. Each line defines a keyword (case‑insensitive) and the label to apply when the keyword appears in the PR title or body (required).

## How it works

1. The action reads the `GITHUB_EVENT_PATH` environment variable to load the PR event payload.
2. It parses the `title` and `body` fields.
3. For each `keyword` defined in `mapping`, it checks if the keyword appears (case‑insensitive) in the title or body.
4. All matching labels are collected.
5. If any labels match, the action outputs them via the `added_labels` output and prints a friendly message. In a real run it would call the GitHub REST API to apply the labels, but for safety in CI it only prints what it *would* do.

## Example output

```
::set-output name=added_labels::🧟‍♂️ Zombie,✨ Feature
Would add labels ["🧟‍♂️ Zombie","✨ Feature"] to PR #42
```

## Testing

Run the provided Jest‑style test with `node tests/test_main.js`. The test creates a mock PR event, sets the required inputs, executes the action, and asserts that the expected labels are reported.
