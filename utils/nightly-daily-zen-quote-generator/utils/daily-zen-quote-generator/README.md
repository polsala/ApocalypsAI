# Daily Zen Quote Generator

A whimsical utility that prints a deterministic "quote of the day" from a curated list. The quote changes each day based on the calendar date, but is reproducible offline—no network calls.

## Features

- No external dependencies.
- Deterministic output; same date always yields the same quote.
- Simple CLI: `python src/main.py`.
- Easy to embed in scripts or terminal prompts.

## Usage

```bash
$ python src/main.py
"Be yourself; everyone else is already taken." — Oscar Wilde
```

## How it works

The utility computes the day‑of‑year for the current date, takes the modulo with the number of built‑in quotes, and selects the corresponding entry.

## Testing

Run the test suite with:

```bash
python -m unittest discover -s tests
```
