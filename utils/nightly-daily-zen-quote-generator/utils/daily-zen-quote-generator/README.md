# Daily Zen Quote Generator

A whimsical yet practical command‑line tool that prints a random Zen‑style quote each time you run it. You can optionally filter quotes by a *theme* (e.g., `mindfulness`, `growth`, `humor`).

## Features
- **Zero external dependencies** – all quotes are stored locally.
- **Deterministic tests** – uses `unittest.mock` to stub randomness.
- **Lightweight** – a single Python file (`quote_generator.py`).

## Installation
```bash
# From the repository root
cd utils/daily-zen-quote-generator
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt  # (empty, but kept for consistency)
```

## Usage
```bash
python -m src.quote_generator            # prints a random quote
python -m src.quote_generator --theme growth  # prints a random "growth" quote
```

## Testing
```bash
pytest tests
```

## License
MIT © ApocalypsAI
