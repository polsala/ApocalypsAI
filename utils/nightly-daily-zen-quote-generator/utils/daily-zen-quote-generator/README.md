# Daily Zen Quote Generator

A whimsical utility that prints a random zen‑style quote each time it runs. Perfect for adding a moment of reflection to scripts, CI logs, or your terminal.

## Usage

```sh
python -m daily_zen_quote_generator
# or
python utils/daily-zen-quote-generator/src/main.py
```

Will output a single quote.

## How it works

- Quotes are stored in `src/quotes.json`.
- The script loads the JSON, picks a random entry, and prints it.
- No external network calls; fully offline.

## Testing

Run the tests with:

```sh
python -m unittest discover utils/daily-zen-quote-generator/tests
```
