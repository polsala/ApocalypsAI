# Nightly PR Labeler

A tiny GitHub Action that scans the title of a pull request and automatically adds labels based on configurable keyword‑to‑label mappings.

## Features

- Zero‑configuration default mapping (bug → `bug`, feat → `feature`, docs → `documentation`).
- Custom mapping via the `mapping` input (JSON string).
- Works with the standard `GITHUB_TOKEN` provided to actions.
- Fully unit‑tested core logic.

## Inputs

| Name    | Description                                            | Required | Default |
|---------|--------------------------------------------------------|----------|---------|
| `token` | GitHub token with `repo` scope (usually `secrets.GITHUB_TOKEN`). | Yes      | – |
| `mapping` | JSON string mapping **keyword** → **label**. Example: `{\"bug\":\"bug\",\"feat\":\"feature\",\"docs\":\"documentation\"}` | No | `{\"bug\":\"bug\",\"feat\":\"feature\",\"docs\":\"documentation\"}` |

## Example Workflow

```yaml
name: Auto‑label PRs
on:
  pull_request:
    types: [opened, edited]

jobs:
  label:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Apply labels
        uses: ./
        with:
          token: ${{ secrets.GITHUB_TOKEN }}
          mapping: '{"bug":"bug","feat":"feature","docs":"documentation"}'
```

## How It Works

The action reads the PR title from the event payload, lower‑cases it, and checks whether any of the configured keywords appear as substrings. All matching labels are added in a single API call.

## Testing

Run the bundled tests locally with Node:

```bash
npm install
node tests/test_index.js
```

All tests should pass, confirming the keyword‑matching logic.
