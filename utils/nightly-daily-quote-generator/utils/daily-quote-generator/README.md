# Daily Quote Generator

A self‑contained Python utility that prints a *Quote of the Day*.

- **Deterministic** – the same calendar date always yields the same quote.
- **Zero external dependencies** – just the Python standard library.
- **Offline‑friendly** – no network requests, perfect for CI or air‑gapped environments.

## Usage
```bash
python -m daily_quote_generator
```
Or import the helper:
```python
from daily_quote_generator import get_quote
print(get_quote())
```

## How it works
The utility stores a short list of whimsical quotes. It hashes the ISO‑format date (e.g., `2025-11-09`) and uses the result to index the list, guaranteeing repeatability across runs and machines.

## Testing
Run the bundled tests with:
```bash
python -m unittest discover -s utils/daily-quote-generator/tests
```
