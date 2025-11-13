# Nightly Quote of the Day

A whimsical yet useful utility that prints a random inspirational quote to the console.

## Features

- Built‑in collection of quotes with optional categories (e.g., *motivation*, *humor*).
- Zero external dependencies – works offline.
- Simple CLI:
  ```bash
  python -m nightly_quote_of_the_day [--category CATEGORY]
  ```
- Deterministic unit tests that mock randomness.

## Usage

```bash
# Print any random quote
python -m nightly_quote_of_the_day

# Print a random quote from the "motivation" category
python -m nightly_quote_of_the_day --category motivation
```

## Development

Run the test suite with:
```bash
python -m unittest discover -s utils/nightly-quote-of-the-day/tests
```
