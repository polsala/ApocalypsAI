# Nightly Emoji Mood Tracker

A whimsical yet useful utility that reads a short piece of text (e.g., a daily journal entry) and outputs a single emoji that best represents the overall mood.

## Features
- **Zero external dependencies** – pure Python 3.11.
- **Deterministic keyword‑based sentiment mapping** – no network calls, fully offline.
- **CLI interface** for quick one‑liners.

## Installation
```bash
# From the repository root
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt  # (no extra deps needed)
```

## Usage
```bash
python -m utils.nightly-emoji-mood-tracker.src.emoji_mood --text "I had a wonderful day!"
# → 😄
```

You can also pipe input:
```bash
echo "Feeling terrible after the meeting" | python -m utils.nightly-emoji-mood-tracker.src.emoji_mood
# → 😞
```

## How it works
The script looks for a set of mood‑related keywords. The first matching keyword determines the emoji. If no keywords are found, a neutral face is returned.

## Testing
```bash
python -m unittest discover utils/nightly-emoji-mood-tracker/tests
```
