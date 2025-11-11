# Emoji Mood Analyzer

A whimsical yet handy command‑line tool that reads a piece of text and returns a single emoji representing the overall mood.

## Features
- **Zero dependencies** – pure Python 3.11 standard library.
- Simple keyword‑based sentiment detection (positive, negative, mixed, neutral).
- Works offline; no network calls.
- Includes a deterministic test suite.

## Installation
```bash
# From the repository root
cd utils/emoji-mood-analyzer
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

## Usage
```bash
python src/analyzer.py "I am feeling happy and wonderful!"
# → 😄
```

## How it works
The script tokenises the input, checks for the presence of a small curated list of positive and negative words, and maps the result to one of four emojis:
- 😄 positive only
- 😞 negative only
- 😕 both positive and negative
- 🤔 neutral (no keywords found)

## Testing
```bash
python -m unittest discover -s tests
```
All tests are deterministic and run offline.
