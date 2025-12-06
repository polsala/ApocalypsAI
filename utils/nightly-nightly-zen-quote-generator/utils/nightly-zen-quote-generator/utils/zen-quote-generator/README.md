# Zen Quote Generator

A tiny, self‑contained utility that prints a random Zen‑style quote.

## Features
- Returns a random quote from a curated list.
- Optional `--theme` flag to filter quotes by theme (e.g., *mindfulness*, *motivation*).
- Zero external dependencies – pure Python 3.11.

## Usage
```bash
python -m src.zen_quote            # prints a random quote
python -m src.zen_quote --theme mindfulness   # prints a mindfulness quote
```

## Adding New Quotes
Edit the `QUOTES` list in `src/zen_quote.py`. Each entry is a dict with:
```python
{"quote": "Your quote here.", "theme": "optional-theme"}
```

## Testing
```bash
python -m unittest discover -s tests
```
