# Daily Quote Generator

A whimsical yet useful utility that prints a random inspirational quote to the console. You can optionally filter quotes by category (e.g., *wisdom*, *humor*, *motivation*).

## Features
- Built‑in collection of quotes, no external API calls.
- Simple command‑line interface.
- Deterministic unit tests using mocks.

## Usage
```bash
python -m daily_quote_generator [--category CATEGORY]
```

- If `--category` is omitted, a quote is chosen from all categories.
- Invalid categories result in a helpful error message.

## Development
Run the test suite with:
```bash
python -m unittest discover -s utils/nightly-daily-quote-generator/utils/daily-quote-generator/tests
```
