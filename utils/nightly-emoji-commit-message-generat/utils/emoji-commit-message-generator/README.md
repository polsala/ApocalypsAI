# Emoji Commit Message Generator

Utility that creates a commit message by appending a deterministic emoji based on the provided description. Helpful for adding a splash of personality to git history while staying reproducible.

## Usage

```bash
python -m emoji_commit "Refactor user authentication flow"
# => "Refactor user authentication flow 🚀"
```

You can influence the emoji selection by setting the `EMOJI_SEED` environment variable.

## How it works

- Takes the description string.
- Computes a stable SHA‑256 hash of the description concatenated with an optional seed.
- Maps the hash to an emoji from a curated list.

## Testing

Run `pytest` inside the utility folder.
