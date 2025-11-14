# Daily Zen Quote Fetcher

Utility that prints a daily "zen" quote. Deterministic based on date, no external network.

## Usage

```sh
python -m daily_zen_quote_fetcher
```

or

```sh
python utils/daily-zen-quote-fetcher/src/quote_fetcher.py
```

## How it works

- Contains a static list of quotes.
- Selects quote by `date.toordinal() % len(quotes)`.
- Provides `get_today_quote()` function and CLI.

## Tests

Run with `pytest`:

```sh
pytest utils/daily-zen-quote-fetcher/tests
```
