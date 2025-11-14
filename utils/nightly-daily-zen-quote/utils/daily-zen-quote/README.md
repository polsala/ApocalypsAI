# Daily Zen Quote

Utility that prints a deterministic "Zen of the Day" quote based on the current date. No network calls; works offline. Ideal for adding a daily inspirational line to your terminal or scripts.

## Usage

```sh
python -m daily_zen_quote
```

or

```sh
python utils/daily-zen-quote/src/main.py
```

## How it works

A small hard‑coded list of quotes is indexed by the day of year modulo the number of quotes, ensuring the same date always yields the same quote.

## Testing

Run the tests with:

```sh
python -m unittest discover -s utils/daily-zen-quote/tests
```
