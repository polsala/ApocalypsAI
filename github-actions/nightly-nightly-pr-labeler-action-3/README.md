# Nightly PR Labeler Action

## Overview

`nightly-pr-labeler-action` is a **composite GitHub Action** that automatically adds helpful labels to a pull request based on the types of files changed. It looks for:

- `docs`      → any ``*.md`` files
- `frontend`  → JavaScript/TypeScript files (``*.js``, ``*.ts``, ``*.jsx``, ``*.tsx``)
- `backend`   → Python, Go, Rust source files (``*.py``, ``*.go``, ``*.rs``)

The action can be used in any workflow that runs on `pull_request` events.

## Usage

```yaml
name: Auto‑label PRs
on:
  pull_request:
    types: [opened, synchronize]

jobs:
  label:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Run PR labeler
        uses: ./nightly-pr-labeler-action
        id: labeler
        env:
          # In CI the action will compute changed files via git diff.
          # For local testing you can override with a comma‑separated list.
          # CHANGED_FILES: "README.md,src/app.js,server/main.py"

      - name: Apply labels
        if: steps.labeler.outputs.labels != ''
        uses: actions-ecosystem/action-add-labels@v1
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          labels: ${{ steps.labeler.outputs.labels }}
```

## How it works

The action is a **composite action** that runs a small Bash script (`src/labeler.sh`). The script:

1. Determines the list of changed files. In a real workflow it uses `git diff` between the PR head and base commits. For unit testing you can provide the list via the `CHANGED_FILES` environment variable (comma‑separated).
2. Scans each file and collects the appropriate labels.
3. Emits the labels as an output named `labels` (comma‑separated) that downstream steps can consume.

## Testing

A simple Bash test is provided under `tests/test_labeler.sh`. It runs the script with a mocked `CHANGED_FILES` variable and checks that the expected labels are produced.

```bash
bash tests/test_labeler.sh
```

## License

MIT © ApocalypsAI
