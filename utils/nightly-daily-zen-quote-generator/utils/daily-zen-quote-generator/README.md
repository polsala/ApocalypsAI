# Daily Zen Quote Generator

Utility that prints a deterministic Zen quote for the day.

## Usage

```sh
python -m daily_zen_quote_generator
```

or

```sh
python src/main.py
```

Will output a quote.

## How it works

Selects a quote based on today's date ordinal modulo the number of built‑in quotes, guaranteeing the same quote for a given day across all machines.

## Testing

Run the test suite with:

```sh
python -m unittest discover -s tests
```
