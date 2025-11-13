# Whimsical Quote of the Day

A tiny, self‑contained Python utility that prints a *deterministic* quote for the current day.

## Features

- No external network calls – all quotes are bundled.
- Deterministic selection based on the ISO calendar date, so the same date always yields the same quote.
- Simple CLI: `python -m quote` prints the quote for today.
- Optional tag filtering (e.g., `--tag humor`).

## Layout

```
utils/whimsical-quote-of-the-day/
├── README.md               # ← you are here
├── src/
│   ├── quote.py            # main implementation & CLI
│   └── quotes.json         # bundled quote database
└── tests/
    └── test_quote.py       # deterministic offline tests
```

## Usage

```bash
# Print today’s quote
python -m utils.whimsical-quote-of-the-day.src.quote

# Filter by tag (e.g., "humor")
python -m utils.whimsical-quote-of-the-day.src.quote --tag humor
```

## Testing

Run the test suite with `pytest`:

```bash
cd utils/whimsical-quote-of-the-day
pytest -q
```

The tests mock the current date to guarantee repeatable results.
