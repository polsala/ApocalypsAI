# Nightly Zen Quote

A whimsical utility that delivers a random Zen‑inspired quote, optionally filtered by category. Perfect for a quick dose of wisdom during your nightly coding sessions.

## Features

- Random quote selection from curated collections.
- Optional category filter (`life`, `work`, `nature`).
- Simple CLI: `python -m utils.zen_quote.src.quote [--category CATEGORY]`.

## Installation

The utility is self‑contained; just run the module with Python 3.11.

## Usage

```sh
python -m utils.zen_quote.src.quote
# or with a category
python -m utils.zen_quote.src.quote --category life
```

## Testing

Run the tests with:

```sh
python -m unittest discover -s utils/nightly-zen-quote/utils/zen-quote/tests
```
