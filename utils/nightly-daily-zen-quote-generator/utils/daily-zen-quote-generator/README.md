# Daily Zen Quote Generator

A tiny utility that prints a deterministic Zen‑inspired quote for the current day. No network access, no dependencies beyond the Python standard library.

## Usage

```sh
python -m daily_zen_quote_generator
```

or

```sh
python utils/daily-zen-quote-generator/src/quote_generator.py
```

## How it works

The utility contains a static list of quotes. The quote for a given day is selected by computing the day‑of‑year modulo the number of quotes, ensuring the same quote is returned for the same date across any environment.

## Testing

Run the tests with:

```sh
python -m unittest discover -s utils/daily-zen-quote-generator/tests
```
