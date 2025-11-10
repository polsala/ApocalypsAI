# Emoji Mood Analyzer

A whimsical yet practical command‑line tool that reads a short piece of text and returns an emoji representing its emotional tone. It uses a lightweight, keyword‑based heuristic – no external APIs, no network calls, fully offline.

## Features
- Zero dependencies (standard library only).
- Deterministic output – the same input always yields the same emoji.
- Simple CLI for quick use in scripts or terminals.
- Comprehensive unit tests bundled with the utility.

## Installation
```bash
# Clone the repository (or copy the folder) and navigate into it
cd utils/emoji-mood-analyzer
# Ensure you have Python 3.11+
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt  # (empty for now)
```

## Usage
```bash
python -m src.analyzer "I am feeling very happy today!"
# → 😊
```

You can also pipe text:
```bash
echo "I love this project" | python -m src.analyzer
# → ❤️
```

## How it works
The analyzer scans the input for a set of predefined keywords (e.g., *happy*, *sad*, *angry*, *love*). The first matching keyword determines the emoji. If no keywords are found, a thinking face 🤔 is returned.

## Testing
Run the bundled tests with:
```bash
python -m unittest discover -s tests
```
All tests are deterministic and use no external resources.
