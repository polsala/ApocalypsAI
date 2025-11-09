# Daily Motivation Quote

A whimsical yet useful utility that prints a random motivational quote to the console.

## Features

- **Zero dependencies** – pure Python 3.11 standard library.
- **Category filtering** – ask for a specific vibe (e.g., `inspiration`, `humor`).
- **Deterministic offline tests** – uses `unittest.mock` to control randomness.

## Usage

```bash
python -m daily-motivation-quote          # any random quote
python -m daily-motivation-quote --category inspiration
```

## Development

Run the test suite with:

```bash
python -m unittest discover -s utils/daily-motivation-quote/tests
```
