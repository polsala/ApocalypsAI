# Emoji Mood Meter

`emoji-mood-meter` is a lightweight, zero‑dependency Python utility that reads a short piece of text and returns a single emoji representing the overall mood.

## Features
- **Instant**: No network calls, pure Python.
- **Deterministic**: Fixed keyword‑to‑emoji mapping ensures repeatable results.
- **CLI friendly**: Run directly from the command line.

## Installation
```bash
# From the repository root
cd utils/nightly-emoji-mood-meter
python -m venv .venv
source .venv/bin/activate
pip install .
```

## Usage
```bash
python -m src.mood_meter "I love sunny days!"
# → 😊
```

## How it works
The script scans the input for a handful of keyword groups (happy, sad, angry, love, surprise). The first matching group determines the emoji. If no keywords are found, a neutral face (😐) is returned.

## Testing
Run the bundled tests with:
```bash
pytest -q
```
