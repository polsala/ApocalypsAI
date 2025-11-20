# Emoji Mood Tracker

Utility that reads a plain‑text journal where each line starts with a date (`YYYY‑MM‑DD`) followed by a mood description. It maps common mood keywords to emojis and prints a concise summary per day.

## Usage

```bash
python -m src.mood_tracker path/to/journal.txt
```

**Example output**

```
2024-10-01 😊
2024-10-02 😞
2024-10-03 🤔
```

## How it works

- Parses each line, extracts the date and the free‑form text.
- Looks for mood‑related keywords (happy, sad, angry, etc.) and selects an emoji.
- If no keyword matches, defaults to 🤔.

## Tests

Run the test suite with `pytest`:

```bash
pytest -q utils/nightly-emoji-mood-tracker/tests
```
