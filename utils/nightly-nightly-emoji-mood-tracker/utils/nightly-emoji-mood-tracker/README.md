# Nightly Emoji Mood Tracker

A whimsical yet practical utility that extracts the *mood* of a piece of text and returns a single emoji.

## Features
- Pure‑Python, no external dependencies.
- Deterministic keyword‑based sentiment analysis.
- Small CLI (`python -m emoji_mood "Your text here"`).
- Fully unit‑tested with offline mocks.

## Installation
```bash
# From the repository root
cd utils/nightly-emoji-mood-tracker
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

## Usage
```bash
python -m src.emoji_mood "I love the sunshine!"
# => 😄
```

## How it works
The script looks for a set of *happy* and *sad* keywords. If any happy word is found, it returns 😄; if any sad word is found, it returns 😢; otherwise it returns 😐.

## Testing
```bash
pytest -q
```
