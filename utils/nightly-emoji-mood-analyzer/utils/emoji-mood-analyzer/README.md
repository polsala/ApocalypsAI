# Emoji Mood Analyzer

A whimsical yet practical utility that determines the overall mood of a piece of text.

## Features
- Detects common happy and sad emojis.
- Falls back to simple keyword heuristics.
- Pure Python 3.11, no external dependencies.

## Installation
```bash
# From the repository root
cd utils/emoji-mood-analyzer
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

## Usage
```python
from src.analyzer import analyze_mood

text = "I love this! 😄"
print(analyze_mood(text))  # -> happy
```

## Testing
```bash
pytest -q
```
