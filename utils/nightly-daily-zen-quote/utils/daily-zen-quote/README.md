# Daily Zen Quote

Utility that prints a deterministic "Zen" quote for the current day. No network calls; quotes are embedded. Useful for terminal greetings, scripts, or CI logs.

## Usage

```sh
python -m daily_zen_quote
```

or

```sh
python src/main.py
```

Will output a quote.

## How it works

Selects a quote from a hard‑coded list based on the day of year modulo the number of quotes.

## Testing

Run `pytest` in the utility folder.
