# Nightly Emoji Mood Tracker

A whimsical yet practical utility that translates plain‑text mood descriptions into emojis.

## Features

- **Deterministic mapping** from common mood words to emojis.
- **CLI** that reads moods from stdin, a file, or command‑line arguments.
- **Python 3.11** only, no external dependencies.

## Installation

```bash
# From the repository root
python -m venv .venv && source .venv/bin/activate
pip install -e utils/nightly-emoji-mood-tracker
```

## Usage

```bash
# Single mood via argument
python -m nightly_emoji_mood_tracker "feeling great"

# Multiple moods from a file (one per line)
python -m nightly_emoji_mood_tracker --file moods.txt
```

## Mapping Table

| Mood keyword | Emoji |
|--------------|-------|
| happy, great, awesome | 😄 |
| sad, down, gloomy | 😢 |
| angry, mad, furious | 😠 |
| love, loved, heart | ❤️ |
| confused, unsure, meh | 🤔 |
| default (unknown) | ❓ |

## Testing

```bash
pytest utils/nightly-emoji-mood-tracker/tests
```
