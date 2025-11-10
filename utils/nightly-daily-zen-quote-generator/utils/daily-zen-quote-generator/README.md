# Daily Zen Quote Generator

A whimsical utility that prints a random Zen‑inspired quote to the console. Great for a quick moment of reflection during your day.

## Usage

```sh
python -m daily_zen_quote_generator
```

or

```sh
python utils/daily-zen-quote-generator/src/main.py
```

## How it works

The script selects a quote from a built‑in list using Python's `random.choice`. No external dependencies, works offline.

## Testing

Run the tests with:

```sh
python -m unittest discover -s utils/daily-zen-quote-generator/tests
```
