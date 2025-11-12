# Daily Zen Quote

Utility that prints a deterministic Zen quote of the day based on the current date. No external dependencies, works offline.

## Usage

```sh
python -m daily_zen_quote
```

or

```sh
python utils/daily-zen-quote/src/main.py
```

Will output a quote.

## How it works

Selects a quote from a built‑in list using the day‑of‑year modulo the number of quotes.
