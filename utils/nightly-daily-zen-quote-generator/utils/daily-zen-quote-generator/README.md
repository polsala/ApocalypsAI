# Daily Zen Quote Generator

A whimsical yet useful utility that prints a *quote of the day* directly in the terminal.

## Features

- **Offline** – all quotes are stored locally in `quotes.json`.
- **Deterministic** – the quote for a given date is always the same, making testing trivial.
- **Zero external dependencies** – pure Python 3.11 standard library.

## Usage

```bash
python -m daily_zen_quote_generator
```

Will output something like:

```
“Do not dwell in the past, do not dream of the future, concentrate the mind on the present moment.” – Buddha
```

## How it works

1. Loads `quotes.json` (a simple array of objects with `text` and `author`).
2. Computes the number of days since a fixed epoch (1970‑01‑01).
3. Uses modulo arithmetic to pick a quote from the list.
4. Prints the selected quote.

## Testing

Run the test suite with:

```bash
python -m unittest discover -s utils/daily-zen-quote-generator/tests
```

The tests mock the current date to ensure deterministic behaviour.
