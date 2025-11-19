# Nightly Quote of the Day

A tiny, self‑contained utility that prints a random inspirational quote each time it is run.

## Features

- **Zero external dependencies** – the quote list lives inside the package.
- **Tag filtering** – request a quote from a specific category (e.g., `wisdom`, `humor`).
- **Deterministic tests** – the random selection is mocked in the test suite.

## Usage

```bash
python -m nightly_quote_of_the_day
```

Optional tag filter:

```bash
python -m nightly_quote_of_the_day --tag wisdom
```

## Structure

```
utils/nightly-quote-of-the-day/
├── README.md
├── src/
│   └── quote.py      # core implementation
└── tests/
    └── test_quote.py # deterministic unit tests
```
