# Daily Zen Quote Generator

A lightweight, self‑contained utility that prints a random Zen‑inspired quote.

## Features
- Returns a random quote from a curated list.
- Optional `--theme` flag to filter quotes by a simple tag (e.g., `motivation`, `mindfulness`).
- Zero external dependencies – pure Python 3.11.

## Installation & Usage
```bash
# Clone the repository (or just copy the folder)
cd utils/daily-zen-quote-generator
python -m src.quote            # prints a random quote
python -m src.quote --theme mindfulness  # prints a mindfulness‑tagged quote
```

## Development
Run the test suite with `pytest`:
```bash
cd utils/daily-zen-quote-generator
pytest -q
```

## License
MIT – see the root LICENSE file.
