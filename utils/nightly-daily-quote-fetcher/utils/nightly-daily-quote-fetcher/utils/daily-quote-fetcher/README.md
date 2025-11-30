# Daily Quote Fetcher

A tiny utility that prints a random inspirational quote from a built‑in collection. Perfect for adding a splash of motivation to terminal sessions, scripts, or chat‑bots.

## Usage

```bash
python -m daily_quote_fetcher
# or
python utils/nightly-daily-quote-fetcher/utils/daily-quote-fetcher/src/quote_fetcher.py
```

Will output a random quote each run.

## Design

- Pure Python 3.11, no external dependencies.
- Quotes are stored in‑code for offline operation.
- Deterministic unit tests mock `random.choice`.
