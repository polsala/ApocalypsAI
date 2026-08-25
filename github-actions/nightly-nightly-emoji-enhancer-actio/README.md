# Nightly Emoji Enhancer Action

A tiny GitHub Action that prefixes a given string with a whimsical emoji.
Useful for adding flair to commit messages, PR titles, or any text.

## Inputs

- `text` (required): The text to enhance.
- `seed` (optional): Integer seed to make emoji selection deterministic. If omitted, current timestamp is used.

## Outputs

- `enhanced_text`: The original text prefixed with the selected emoji.

## Usage

```yaml
uses: your-org/nightly-emoji-enhancer-action@v1
with:
  text: "Deploy to production"
  seed: 42
```

The action will set `enhanced_text` which you can use in subsequent steps.

## How it works

The action runs a small Node.js script that selects an emoji from a fixed list
based on the provided seed (modulo the list length). This makes the result
repeatable for the same seed, which is handy for testing.

## License

MIT
