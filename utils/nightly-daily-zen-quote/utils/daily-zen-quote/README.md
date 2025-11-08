# Daily Zen Quote

A tiny, whimsical utility that prints a deterministic "zen" quote for the current day.

## Features

- No external dependencies.
- Deterministic selection based on the calendar date, so the same date always yields the same quote.
- Simple CLI: `python -m src.quote` prints the quote for today.
- Easy to embed in scripts, terminals, or as a daily reminder.

## Usage

```sh
python -m src.quote
```

## How it works

The utility maintains a short list of curated quotes. The index is calculated as:

```
index = (year + month + day) % len(quotes)
```

Thus each day maps to a predictable quote without any network calls.

## Testing

Run the bundled tests with:

```sh
python -m unittest discover -s tests
```
