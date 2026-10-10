# Nightly Emoji Commit Enhancer

A whimsical GitHub Action that appends a time‑of‑day appropriate emoji to pull‑request titles (or any string you feed it).  It makes the repository a little brighter without changing any code.

## Features

- Detects the current UTC hour (or a supplied override for testing) and selects an emoji that matches the time of day.
- Fully deterministic when `date_override` is provided – perfect for CI testing.
- Implemented as a **composite** action with a tiny Bash entrypoint, so it runs on any runner without extra dependencies.

## Inputs

| Name | Description | Required | Default |
|------|-------------|----------|---------|
| `date_override` | ISO‑8601 timestamp to override the current date (useful for tests). | false | *none* |

## Outputs

| Name | Description |
|------|-------------|
| `emoji` | The selected emoji string (e.g., `☀️`). |

## Example Workflow

```yaml
name: PR Emoji Enhancer
on:
  pull_request:
    types: [opened, edited]

jobs:
  add-emoji:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Apply Emoji
        id: emoji
        uses: ./nightly-emoji-commit-enhancer
      - name: Update PR title
        if: steps.emoji.outputs.emoji != ''
        run: |
          gh pr edit ${{ github.event.pull_request.number }} --title "${{ steps.emoji.outputs.emoji }} ${{ github.event.pull_request.title }}"
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

## Testing

Run the bundled test script locally:

```bash
cd nightly-emoji-commit-enhancer
bash tests/test_entrypoint.sh
```

The test forces a morning timestamp and expects the sun emoji (`☀️`).
