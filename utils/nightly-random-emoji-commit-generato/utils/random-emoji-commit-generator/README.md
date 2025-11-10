# Random Emoji Commit Generator

Utility that creates a fun commit message by prepending a random emoji to a user‑provided description. Useful for adding a splash of personality to Git histories.

## Usage

```bash
python -m random_emoji_commit_generator "Fix typo in README"
# Output: 🛠️ Fix typo in README
```

## How it works

- Picks a random emoji from a curated list.
- Joins it with the supplied message.

## Testing

Run `pytest` in the utility folder.
