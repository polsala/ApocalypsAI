# Nightly Emoji Mood Analyzer

A lightweight, self‑contained Python utility that parses a collection of text messages and reports how often each emoji appears. Perfect for chat logs, comment threads, or any place where emojis convey sentiment.

## Features
- Detects Unicode emojis (including multi‑code‑point sequences).
- Returns a sorted frequency dictionary.
- Simple CLI for quick ad‑hoc analysis.
- Zero external dependencies beyond the Python standard library.

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
python -m src.emoji_analyzer path/to/messages.txt
```
The input file should contain one message per line. The script prints a JSON‑formatted frequency map, e.g.:
```json
{"😀": 12, "😢": 3, "🚀": 5}
```

## Testing
```bash
pytest -q
```
All tests run offline and are deterministic.
