# Emoji Mood Analyzer

A whimsical yet handy command‑line tool that reads a line of text and returns an emoji representing the overall mood. It uses a lightweight keyword‑based heuristic, no external APIs, and works offline.

## Installation

```bash
python -m venv .venv
source .venv/bin/activate
pip install .
```

(Or just run the script directly.)

## Usage

```bash
python -m utils.emoji-mood-analyzer.src.analyzer "I love sunny days!"
# Output: 😊
```

## How it works

The analyzer scans the input for positive, negative, and neutral keywords and selects an emoji accordingly.

## Tests

Run:

```bash
python -m unittest discover utils/emoji-mood-analyzer/tests
```
