# Daily Zen Quote Generator

A tiny utility that prints a daily Zen‑style quote. The quote is selected deterministically based on the current date, so every day yields the same quote across machines without network access.

## Usage

```sh
python -m daily_zen_quote_generator
```

or

```sh
python src/quote_generator.py
```

## How it works

- Quotes are stored in `src/quotes.json`.
- The index is computed as `day_of_year % len(quotes)`.
- No external dependencies; works offline.

## Tests

Run with `pytest`:

```sh
pytest -q
```
