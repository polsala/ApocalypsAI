# Nightly PR Emoji Labeler

A tiny GitHub Action that inspects a pull‑request title and automatically adds an emoji‑styled label based on simple keyword detection.  It’s whimsical, lightweight, and perfect for community repos that love a bit of flair.

## Features

- Detects common PR intents (`bug`, `feature`, `docs`, `test`, `refactor`).
- Assigns a matching emoji label (e.g. `🐞 bug`, `✨ feature`).
- Falls back to a generic `🤖 unknown` label.
- No external dependencies – pure JavaScript.

## Inputs

| Name | Description | Required | Default |
|------|-------------|----------|---------|
| `title` | The pull‑request title to evaluate. GitHub automatically provides this as `github.event.pull_request.title`. | **true** | N/A |

## Outputs

| Name | Description |
|------|-------------|
| `label` | The emoji label that should be applied to the PR. |

## Usage

Add the action to your workflow (e.g. `.github/workflows/pr-labeler.yml`):

```yaml
name: PR Emoji Labeler
on:
  pull_request:
    types: [opened, edited]

jobs:
  label:
    runs-on: ubuntu-latest
    steps:
      - name: Determine emoji label
        id: emoji
        uses: ./nightly-pr-emoji-labeler
        with:
          title: "${{ github.event.pull_request.title }}"

      - name: Apply label
        uses: actions-ecosystem/action-add-labels@v1
        with:
          labels: "${{ steps.emoji.outputs.label }}"
```

The workflow runs whenever a PR is opened or its title is edited, computes the appropriate label, and then adds it using the popular `action-add-labels` action.

## How it works

The action’s JavaScript (`src/index.js`) looks for keywords in the title (case‑insensitive). The first matching keyword determines the label. If none match, the generic `🤖 unknown` label is returned.

## Testing

Run the bundled tests locally with Node:

```bash
node tests/test_main.js
```

All tests should pass, confirming deterministic behaviour.
