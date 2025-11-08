# Daily Motivation Generator

A whimsical yet useful utility that returns a random motivational quote each time it is invoked. Perfect for adding a splash of inspiration to scripts, terminals, or CI pipelines.

## Features

- **Zero dependencies** – pure Python standard library.
- Simple API: `get_motivation()` returns a formatted quote.
- Ready‑to‑run CLI: `python -m src.motivation` prints a quote to stdout.
- Deterministic offline tests using mocks.

## Usage

```bash
python -m src.motivation
```

Or within Python:

```python
from src.motivation import get_motivation

print(get_motivation())
```

## Testing

Run the bundled tests with:

```bash
python -m unittest discover -s utils/daily-motivation-generator/tests
```

## Extensibility

Add more quotes to the `_QUOTES` list in `src/motivation.py` or implement categorization in future versions.
