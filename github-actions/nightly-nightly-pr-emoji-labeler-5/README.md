# Nightly PR Emoji Labeler

A whimsical GitHub Action that examines the pull request title and emits an emoji representing its sentiment: 👍 for positive, 👎 for negative, 🤝 for neutral. Use the output `emoji` in subsequent steps to add fun labels or messages.

## Inputs

- `title` (required): The pull request title. Usually provided via `${{ github.event.pull_request.title }}`.

## Outputs

- `emoji`: The selected emoji.

## Example workflow

```yaml
name: PR Emoji Labeler
on:
  pull_request:
    types: [opened, edited]

jobs:
  label:
    runs-on: ubuntu-latest
    steps:
      - id: emoji
        uses: ./github-actions/nightly-pr-emoji-labeler
        with:
          title: ${{ github.event.pull_request.title }}
      - name: Add label
        uses: actions-ecosystem/action-add-labels@v1
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          labels: ${{ steps.emoji.outputs.emoji }}
```

## How it works

The action uses a simple keyword heuristic to decide sentiment.

- Positive keywords: `add`, `fix`, `improve`, `update`, `enhance`
- Negative keywords: `remove`, `deprecate`, `break`, `fail`, `bug`
- If none match, it defaults to neutral.

## License

MIT
