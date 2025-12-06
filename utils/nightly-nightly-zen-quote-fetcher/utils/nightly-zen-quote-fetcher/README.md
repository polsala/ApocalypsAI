# Nightly Zen Quote Fetcher

A whimsical utility that prints a random Zen‑inspired quote to the console. Perfect for a quick dose of wisdom during your nightly coding sessions.

## Features

- No external dependencies.
- Deterministic behavior for testing via optional `random_state`.
- Simple CLI: `python -m src.zen_quote` prints a quote.

## Usage

```sh
python -m src.zen_quote
```

## Testing

Run the test suite with:

```sh
python -m unittest discover -s tests
```
