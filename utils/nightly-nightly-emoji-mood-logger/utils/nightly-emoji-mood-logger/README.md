# Nightly Emoji Mood Logger

## Overview
`nightly-emoji-mood-logger` is a lightweight, zero‑dependency Python utility that reads a line of text and returns an emoji representing the inferred mood. It uses a small set of keyword heuristics and works entirely offline.

## Features
- **Deterministic** – No external APIs, pure Python logic.
- **CLI friendly** – Pipe text or pass a string argument.
- **Embeddable** – Import `get_mood_emoji` in other scripts.

## Installation
```bash
# From the repository root
cd utils/nightly-emoji-mood-logger
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

## Usage
```bash
# As a module
python -m nightly_emoji_mood_logger "I am so happy today!"
# Output: 😊

# Or import in code
from nightly_emoji_mood_logger import get_mood_emoji
print(get_mood_emoji("Feeling a bit sad..."))  # 😢
```

## Testing
```bash
pytest -q
```

## License
MIT © ApocalypsAI
