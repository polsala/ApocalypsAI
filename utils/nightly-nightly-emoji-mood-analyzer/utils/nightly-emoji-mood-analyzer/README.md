# Nightly Emoji Mood Analyzer

**Purpose**: Quickly gauge the sentiment of a short piece of text and get a single emoji that captures the mood.

## Features
- Pure‑Python, no external services.
- Simple keyword‑based sentiment detection (happy, sad, angry, neutral).
- CLI entry‑point for ad‑hoc use.
- Library function `analyze_mood(text: str) -> str` for integration.

## Installation
```bash
# From the repository root
cd utils/nightly-emoji-mood-analyzer
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt  # (empty, only stdlib)
```

## Usage
```bash
python -m src.analyzer "I love this wonderful day!"
# → 😄
```

Or as a library:
```python
from src.analyzer import analyze_mood
print(analyze_mood("I'm feeling terrible..."))  # 😢
```

## Testing
```bash
pytest -q
```

## Design
The analyzer uses a small, deterministic keyword list. It is deliberately simple to keep the utility lightweight and fully offline.
