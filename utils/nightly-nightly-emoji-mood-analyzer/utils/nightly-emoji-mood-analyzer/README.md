# Nightly Emoji Mood Analyzer

A whimsical yet practical command‑line utility that reads a short piece of text and returns an emoji representing its overall mood.

## Features

- **Zero dependencies** – pure Python 3.11 standard library.
- **Deterministic** – uses a simple keyword‑based heuristic, no network calls.
- **CLI friendly** – pipe text or pass a string argument.
- **Reusable** – expose `analyze_mood(text: str) -> str` for import in other projects.

## Installation

Copy the `utils/nightly-emoji-mood-analyzer` folder into your repository and run:

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt  # (none needed)
```

## Usage

```bash
# From the command line
python -m utils.nightly-emoji-mood-analyzer.src.analyzer "I love sunny days!"
# → 😄
```

Or as a library:

```python
from utils.nightly-emoji-mood-analyzer.src.analyzer import analyze_mood
print(analyze_mood("Feeling a bit gloomy..."))  # 😔
```

## Testing

```bash
python -m unittest discover utils/nightly-emoji-mood-analyzer/tests
```

---

*Created by the ApocalypsAI Nightly Integrator.*
