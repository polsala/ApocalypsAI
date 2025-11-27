# Nightly Emoji Mood Indicator

## Overview
`emoji-mood-indicator` is a lightweight, zero‑dependency Python utility that converts a textual mood (e.g., "happy", "sad", "angry") into a corresponding emoji. It can be used in scripts, CI pipelines, or manually from the command line to add a dash of personality to logs, commit messages, or chat bots.

## Features
- **Deterministic** – No network calls; all mappings are baked in.
- **Case‑insensitive** – Accepts any capitalisation of the mood string.
- **Graceful fallback** – Returns a generic "❓" for unknown moods.
- **CLI friendly** – `python -m mood <mood>` prints the emoji directly.

## Installation
```bash
# From the repository root
cd utils/nightly-emoji-mood-indicator
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt  # (empty, kept for future extensibility)
```

## Usage
```bash
python -m src.mood happy
# → 😊

python -m src.mood "feeling stressed"
# → ❓ (unknown mood)
```

## API
```python
from src.mood import get_mood_emoji

emoji = get_mood_emoji("excited")  # returns "🤩"
```

## Testing
```bash
pytest -q
```

## License
MIT © ApocalypsAI
