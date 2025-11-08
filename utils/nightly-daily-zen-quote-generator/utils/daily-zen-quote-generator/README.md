# Daily Zen Quote Generator

A whimsical yet useful utility that prints a random Zen‑style quote to inspire your day.

## Features
- Built‑in collection of 20+ Zen quotes.
- Optional `--theme` flag to limit quotes to a specific theme (e.g., *mindfulness*, *growth*, *simplicity*).
- Zero external dependencies – works offline.

## Installation
```bash
# From the repository root
cd utils/daily-zen-quote-generator
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt  # (empty, only stdlib)
```

## Usage
```bash
python -m src.main            # prints a random quote
python -m src.main --theme mindfulness   # prints a quote tagged with 'mindfulness'
```

## Testing
```bash
python -m unittest discover -s tests
```
