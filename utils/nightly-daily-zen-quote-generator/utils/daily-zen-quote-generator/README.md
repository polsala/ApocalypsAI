# Daily Zen Quote Generator

Provides a deterministic "Zen" quote for each day. The quote is selected from a small built‑in collection based on the day of year, so the same date always yields the same quote without any network calls.

## Usage

```bash
python -m daily_zen_quote_generator
# or
python utils/daily-zen-quote-generator/src/main.py
```

Outputs a single line quote.

## How it works

- Quotes are stored in `src/quotes.json`.
- `get_quote(date)` computes `index = (day_of_year - 1) % len(quotes)`.
- If `date` is omitted, uses `datetime.date.today()`.

## Testing

Run:

```bash
python -m unittest discover utils/daily-zen-quote-generator/tests
```
