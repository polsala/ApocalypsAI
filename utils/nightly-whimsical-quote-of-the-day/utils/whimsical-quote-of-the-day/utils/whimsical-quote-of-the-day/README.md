# Whimsical Quote of the Day

A tiny offline utility that prints a deterministic "Quote of the Day" based on the current date. No network required; perfect for a daily dose of inspiration in CI or local terminals.

## Usage

```sh
python -m whimsical_quote_of_the_day
```

or

```sh
python utils/whimsical-quote-of-the-day/utils/whimsical-quote-of-the-day/src/quote_of_the_day.py
```

## How it works

The utility selects a quote from a built‑in list using the ordinal of today's date (`date.toordinal() % len(quotes)`). Because the calculation is purely deterministic, the same date always yields the same quote.

## Testing

Run the tests with:

```sh
python -m unittest discover utils/whimsical-quote-of-the-day/utils/whimsical-quote-of-the-day/tests
```
