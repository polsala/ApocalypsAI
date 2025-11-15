# Daily Zen Quote Generator

A whimsical utility that prints a deterministic "quote of the day" from a curated list. The quote changes each day based on the calendar, but is reproducible offline—perfect for terminal splash screens, CI logs, or personal motivation.

## Features

- Zero external dependencies.
- Deterministic output: the same date always yields the same quote.
- Simple CLI: `python -m daily_zen_quote_generator` (or run the script directly).
- Easily extensible: add your own quotes to `src/quote.py`.

## Usage

```sh
$ python -m daily_zen_quote_generator
🧘 “The only limit to our realization of tomorrow is our doubts today.” – Franklin D. Roosevelt
```

## How it works

The utility stores a static list of quotes. The quote for a given day is selected by computing `date.toordinal() % len(quotes)`. This ensures a repeatable mapping without any network calls.

## Testing

Run the bundled tests with:

```sh
python -m unittest discover -s utils/daily-zen-quote-generator/tests
```
