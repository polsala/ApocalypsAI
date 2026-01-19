# Emoji Boost GitHub Action

Adds a random emoji to your workflow output, perfect for brightening CI logs or adding fun to commit messages.

## Usage

```yaml
steps:
  - uses: ./nightly-action-commit-emoji-boost
    id: emoji
  - run: echo "Today's emoji: ${{ steps.emoji.outputs.emoji }}"
```

The action sets an output `emoji` containing a single random emoji.

## How it works

The action selects a random emoji from a curated list using JavaScript's `Math.random` and exposes it via the `emoji` output.

## License

MIT
