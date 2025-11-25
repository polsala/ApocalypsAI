# Nightly Quote of the Day

A tiny utility that prints a whimsical quote for the current day. The quote is selected deterministically from a built‑in list, so the same date always yields the same quote. Perfect for adding a splash of inspiration to your terminal or CI logs.

## Usage

```bash
python -m src.quote_of_the_day
```

or

```bash
python utils/nightly-quote-of-the-day/src/quote_of_the_day.py
```

## How it works

The utility hashes the ISO calendar day (YYYY‑MM‑DD) to an index into a static list of quotes. No network access, no external files.
