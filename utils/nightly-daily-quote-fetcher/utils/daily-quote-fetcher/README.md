# Daily Quote Fetcher

Utility that prints a random quote from a bundled collection. No network required.

## Usage

```bash
python -m src.quote_fetcher
```

or

```bash
python src/quote_fetcher.py
```

## How it works

- Quotes stored in `src/quotes.json`.
- `get_random_quote()` selects a random entry.
- CLI prints the formatted quote.

## Testing

Run:

```bash
pytest -q
```
