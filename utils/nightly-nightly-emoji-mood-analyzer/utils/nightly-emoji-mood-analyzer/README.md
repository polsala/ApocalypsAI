# Emoji Mood Analyzer

Utility that scans a text file for Unicode emojis and reports the dominant mood category (`happy`, `sad`, `love`, `angry`, `neutral`). Useful for summarizing chat logs, comment threads, or any emoji‑rich text.

## Usage

```bash
python -m emoji_mood_analyzer path/to/file.txt
```

Outputs one of: `happy`, `sad`, `love`, `angry`, `neutral`.

## How it works

- Parses the file, extracts emojis using a regex.
- Maps each emoji to a mood category (see `EMOJI_MOOD_MAP`).
- Counts occurrences and returns the category with the highest count.
- If no emojis are found, returns `neutral`.

## Tests

Run with `pytest`:

```bash
pytest -q utils/nightly-emoji-mood-analyzer/tests
```
