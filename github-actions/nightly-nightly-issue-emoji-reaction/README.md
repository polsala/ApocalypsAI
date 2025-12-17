# Issue Emoji Reaction Action

Adds a random uplifting emoji reaction to newly opened issues.

## Usage

```yaml
name: Issue Emoji Reaction
on:
  issues:
    types: [opened]

jobs:
  react:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: React with Emoji
        uses: ./  # assuming action in repo root or path
        with:
          token: ${{ secrets.GITHUB_TOKEN }}
          emojis: "👍,🎉,🚀,🌟,💡"
```

## Inputs

- `token` (required): GitHub token.
- `emojis` (optional): Comma‑separated list of emojis. Default list provided.

## How it works

The action picks a random emoji from the list and adds it as a reaction to the issue that triggered the workflow.

## License

MIT
