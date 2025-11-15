# Daily Zen Quote Generator

Utility that prints a deterministic "quote of the day" based on the current date. No network calls; uses a built‑in list of zen sayings. Helpful for adding a bit of calm to scripts or CI logs.

## Usage

```bash
python -m utils.daily-zen-quote-generator.src.main
# or
python utils/daily-zen-quote-generator/src/main.py
```

Will output a quote.

## API

```python
get_quote(date: datetime.date | None = None) -> str
```

If `date` is `None`, the function uses today’s date.

## Tests

Run with:

```bash
python -m unittest discover utils/daily-zen-quote-generator/tests
```
