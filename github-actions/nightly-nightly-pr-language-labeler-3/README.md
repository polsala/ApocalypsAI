# PR Language Labeler Action

## Overview

A lightweight GitHub Action that examines the list of files changed in a pull request and automatically adds *language* labels (e.g., `language:python`, `language:javascript`). This helps teams quickly see what languages are affected without manually scanning the diff.

## Inputs

| Name | Description | Required |
|------|-------------|----------|
| `files` | Comma‑separated list of file paths changed in the PR. The action expects the workflow to provide this list (e.g., via `git diff --name-only`). | Yes |

## Outputs

| Name | Description |
|------|-------------|
| `labels` | Comma‑separated list of language labels that were detected.

## Example Workflow

```yaml
name: Auto‑label PR languages
on:
  pull_request:
    types: [opened, synchronize]

jobs:
  label:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v3

      - name: Get changed files
        id: changed
        run: |
          echo "files=$(git diff --name-only ${{ github.event.pull_request.base.sha }} ${{ github.sha }} | paste -sd ',' -)" >> $GITHUB_OUTPUT

      - name: Run language labeler
        uses: ./nightly-pr-language-labeler
        with:
          files: ${{ steps.changed.outputs.files }}
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}

      - name: Apply labels
        if: steps.labeler.outputs.labels != ''
        run: |
          LABELS=${{ steps.labeler.outputs.labels }}
          for L in $(echo $LABELS | tr ',' '\n'); do
            gh pr edit ${{ github.event.pull_request.number }} --add-label "$L"
          done
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

## How It Works

The action receives the `files` input, splits it into an array, maps each file extension to a predefined language label, deduplicates the results, and then writes the labels to the `$GITHUB_OUTPUT` file so they can be consumed by subsequent steps.

## Testing

Run the provided Jest‑style test with Node:

```bash
node tests/test_index.js
```

The test suite validates that the label detection logic works for a variety of common extensions.
