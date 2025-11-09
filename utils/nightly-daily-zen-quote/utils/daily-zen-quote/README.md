# Daily Zen Quote

A tiny, self‑contained utility that returns a random Zen‑style quote from an internal list.

## Features

- **Pure Python 3.11** – no external dependencies.
- Deterministic output via an optional `--seed` flag (useful for testing or reproducible daily messages).
- Optional `--max-length` filter to restrict the quote length.
- Simple CLI (`python -m src.zen`) that prints the quote to stdout.
- Importable functions for programmatic use.

## Usage

```bash
# Print a random quote
python -m src.zen

# Print a quote no longer than 60 characters
python -m src.zen --max-length 60

# Deterministic output (same quote every run)
python -m src.zen --seed 123
```

## API

```python
from src.zen import get_random_quote, filter_by_max_length

quote, author = get_random_quote()               # random quote
quote, author = get_random_quote(seed=42)        # deterministic
quote, author = filter_by_max_length(70)         # respects length constraint
```

## Testing

Run the bundled tests with:

```bash
python -m unittest discover -s tests
```
