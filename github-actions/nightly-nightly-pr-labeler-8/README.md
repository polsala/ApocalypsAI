# Nightly PR Labeler

A tiny, whimsical GitHub Action that automatically adds helpful labels to a pull request based on keywords found in its title.

## Features

- Detects common keywords: `bug`, `feature`, `doc`/`docs`.
- Falls back to `needs‑triage` when no keyword matches.
- Works as a **composite** action – no extra runtime dependencies.
- Fully testable offline with a simple Bash test script.

## Usage

Add the action to your workflow (e.g. `.github/workflows/pr-labeler.yml`):

```yaml
name: PR Labeler
on:
  pull_request:
    types: [opened, edited]

jobs:
  label:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Auto‑label PR
        uses: ./github-actions/nightly-pr-labeler
        with:
          github-token: ${{ secrets.GITHUB_TOKEN }}
```

The action reads the PR title, decides on a label, and adds it via the GitHub REST API.

## Inputs

| Name | Description | Default |
|------|-------------|---------|
| `github-token` | Token with `issues:write` permission (usually `${{ secrets.GITHUB_TOKEN }}`). | `${{ github.token }}` |

## How it works

The action is a **composite** action that runs a small Bash script (`src/labeler.sh`). The script:
1. Extracts the PR title from `github.event.pull_request.title`.
2. Matches keywords (case‑insensitive).
3. Calls the GitHub API to apply the chosen label.

## Testing

Run the offline test script locally:

```bash
bash tests/test_labeler.sh
```

The test simulates several PR titles and verifies that the script outputs the expected label.
