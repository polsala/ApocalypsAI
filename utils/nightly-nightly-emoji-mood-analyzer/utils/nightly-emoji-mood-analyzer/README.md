# Nightly Emoji Mood Analyzer

A whimsical yet practical utility that reads a piece of text and returns a simple sentiment label (`positive`, `negative`, `neutral`) together with a matching emoji.

## Features
- **Zero external dependencies** – pure Python 3.11.
- Works offline; no network calls.
- Provides a tiny CLI (`python -m analyzer "Your text"`).
- Includes a deterministic test‑suite.

## Installation
```bash
# From the repository root
cd utils/nightly-emoji-mood-analyzer
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

## Usage
```bash
python -m analyzer "I love open source!"
# Output: positive 😊
```

## How it works
The analyzer uses a handcrafted word‑list to score the input text. Each positive word adds +1, each negative word subtracts 1. The final score determines the sentiment:
- score > 0 → `positive` 😊
- score < 0 → `negative` 😞
- otherwise → `neutral` 😐

## Testing
```bash
pytest -q
```
All tests run offline and are fully deterministic.
