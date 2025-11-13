# Emoji Mood Analyzer

A whimsical yet useful CLI utility that examines a piece of text, counts the emojis present, and reports the overall mood (happy, sad, angry, love, surprise, or neutral). Ideal for quick sentiment checks in chat logs, social media posts, or any emoji‑rich content.

## Features

- **Zero dependencies** – pure Python 3.11 standard library.
- Detects a curated set of emojis and maps them to five mood categories.
- Returns **neutral** when no known emojis are found.
- Simple CLI: `python -m utils.nightly-emoji-mood-analyzer.src.emoji_mood --text "Your text"`.

## Installation

Copy the `utils/nightly-emoji-mood-analyzer` directory into your project or add it to your `PYTHONPATH`.

## Usage

```bash
python -m utils.nightly-emoji-mood-analyzer.src.emoji_mood --text "I love this! ❤️❤️"
# Output: love
```

## Testing

Run the bundled tests with:

```bash
python -m unittest discover -s utils/nightly-emoji-mood-analyzer/tests
```
