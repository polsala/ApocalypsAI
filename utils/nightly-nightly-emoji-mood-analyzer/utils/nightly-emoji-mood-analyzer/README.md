# Nightly Emoji Mood Analyzer

A tiny, self‑contained utility that scans a string for emojis and reports the overall mood.

## Features
- Detects **happy**, **sad**, and **angry** emojis.
- Returns one of four mood labels: `happy`, `sad`, `angry`, or `neutral`.
- Simple, zero‑dependency Python implementation.

## Installation
```bash
# Clone the repository (or copy the folder) and install the utility in a venv
python -m venv .venv
source .venv/bin/activate
pip install -e utils/nightly-emoji-mood-analyzer
```

## Usage
```python
from src.emoji_analyzer import analyze_mood

text = "I love this! 😊😊"
print(analyze_mood(text))  # -> happy
```

## Testing
```bash
pytest utils/nightly-emoji-mood-analyzer/tests
```

## License
MIT © ApocalypsAI
