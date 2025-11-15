# Mood ASCII Art

`mood-ascii-art` converts a simple mood string into a pre‑defined ASCII‑art illustration.

## Features
- Zero external dependencies – pure Python 3.11.
- Deterministic mapping, safe for offline use.
- Small CLI (`python -m mood_art <mood>`) for quick terminal fun.

## Installation
```bash
# From the repository root
cd utils/mood-ascii-art
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt  # (empty, kept for consistency)
```

## Usage
```bash
python -m src.mood_art happy
```
Will print a happy face ASCII art.

## Supported moods
- `happy`
- `sad`
- `angry`
- `surprised`
- `neutral`

Any unknown mood falls back to a generic "meh" face.

## Testing
```bash
pytest -q
```
All tests run offline and are fully deterministic.
