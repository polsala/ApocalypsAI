# Nightly Apocalypse Badge

A whimsical GitHub Action that leaves a post‑apocalypse themed badge comment on a pull request based on how many files the PR changes.

## Inputs

| Name | Description | Required |
|------|-------------|----------|
| `changed_files` | Comma‑separated list of files changed in the PR (e.g. `src/main.py,README.md`). | true |
| `github_token` | GitHub token with `repo` scope (automatically provided as `secrets.GITHUB_TOKEN`). | true |

## How it works

The action counts the number of files listed in `changed_files` and selects a badge:

* **🛡️ Small** – 5 files or fewer  
* **⚔️ Medium** – 6‑20 files  
* **☢️ Massive** – more than 20 files  

It then posts a comment on the PR with the badge.

## Usage

```yaml
name: Apocalypse Badge

on:
  pull_request:
    types: [opened, synchronize]

jobs:
  badge:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Get changed files
        id: files
        run: |
          echo "changed=$(git diff --name-only ${{ github.event.pull_request.base.sha }} ${{ github.sha }} | paste -sd ',' -)" >> $GITHUB_OUTPUT
      - name: Add badge
        uses: ./ # uses the action from this repository
        with:
          changed_files: ${{ steps.files.outputs.changed }}
          github_token: ${{ secrets.GITHUB_TOKEN }}
```

## License

MIT
