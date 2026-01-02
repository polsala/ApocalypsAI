# Nightly PR Labeler

A GitHub Action that inspects the files changed in a pull request and automatically adds labels such as `docs`, `code`, `tests`, `ci` to help triage.

## Usage

```yaml
name: PR Labeler
on:
  pull_request:
    types: [opened, synchronize]

jobs:
  label:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Label PR
        uses: ./ # assuming action in repo root
        with:
          github-token: ${{ secrets.GITHUB_TOKEN }}
```

## How it works

The action runs a small Bash script that:

1. Reads the pull request number from the event payload.
2. Calls `gh pr view $PR_NUMBER --json files` to get changed files.
3. Determines categories:
   - paths starting with `docs/` → `docs`
   - paths ending with `.md` → `docs`
   - paths under `src/` or ending with `.py`, `.js`, `.ts`, `.rs`, `.go` → `code`
   - paths under `tests/` → `tests`
   - paths under `.github/` → `ci`
4. Adds the labels via `gh pr edit $PR_NUMBER --add-label <label>`.

## Inputs

| Name | Description | Required |
|------|-------------|----------|
| github-token | Token with `repo` scope (usually `secrets.GITHUB_TOKEN`). | Yes |

## License

MIT
