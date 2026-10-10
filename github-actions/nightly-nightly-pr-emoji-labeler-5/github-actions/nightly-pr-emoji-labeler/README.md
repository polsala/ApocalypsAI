# Nightly PR Emoji Labeler

## Overview

`nightly-pr-emoji-labeler` is a lightweight GitHub Action that scans the title of a pull request for user‑defined keywords and adds a matching emoji as a label. It adds a fun, visual cue to PRs while keeping the implementation simple and offline‑testable.

## Inputs

| Name | Description | Required | Default |
|------|-------------|----------|---------|
| `token` | GitHub token (usually `{{ secrets.GITHUB_TOKEN }}`) | Yes | – |
| `keyword_emoji_map` | JSON string mapping keywords (regex) to emojis. | No | `{ "fix":"🔧", "feat":"✨", "docs":"📚", "refactor":"♻️" }` |

## How it works

1. The action reads the PR title from the event payload.
2. It iterates over the provided keyword‑emoji map.
3. The first keyword that matches the title determines the emoji.
4. The emoji is exposed as an output (`emoji`) which can be used by subsequent steps (e.g., to add a label via the GitHub API).

## Example workflow

```yaml
name: PR Emoji Labeller
on:
  pull_request:
    types: [opened, edited]

jobs:
  label:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - id: emoji
        uses: ./github-actions/nightly-pr-emoji-labeler
        with:
          token: ${{ secrets.GITHUB_TOKEN }}
          keyword_emoji_map: '{"fix":"🔧","feat":"✨","docs":"📚"}'
      - name: Add label
        if: steps.emoji.outputs.emoji != '❓'
        run: |
          curl -s -X POST \
            -H "Authorization: token ${{ secrets.GITHUB_TOKEN }}" \
            -H "Accept: application/vnd.github+json" \
            https://api.github.com/repos/${{ github.repository }}/issues/${{ github.event.pull_request.number }}/labels \
            -d '{"labels":["${{ steps.emoji.outputs.emoji }}"]}'
```

## Testing

Run the provided test script locally:

```bash
bash tests/test_main.sh
```

The test simulates a PR event and verifies that the correct emoji (`✨`) is produced for a title containing the keyword `feat`.
