# Mood Emoji Generator

A tiny utility that maps textual mood descriptions to a fitting emoji. Useful for adding emotional flair to logs, chat messages, or commit messages.

## Usage

```bash
python -m mood_emoji_generator "excited"
# => 🤩
```

## How it works

A simple dictionary maps common moods to emojis. The lookup is case‑insensitive and falls back to 🤔 for unknown moods.

## Testing

Run `pytest` in the utility folder.
