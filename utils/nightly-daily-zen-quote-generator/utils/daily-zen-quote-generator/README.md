# Daily Zen Quote Generator

A whimsical CLI that prints a Zen‑style quote of the day. The quote is selected deterministically from a built‑in list based on the current date, so it works offline and is fully reproducible.

## Usage

```sh
python -m daily_zen_quote_generator
```

or

```sh
python src/main.py
```

It prints a single line quote to stdout.

## How it works

The utility loads `quotes.json`, computes `date.today().toordinal() % len(quotes)` and selects the corresponding entry.
