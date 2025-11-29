# Nightly Quote of the Day

A tiny utility that prints a random post‑apocalyptic quote. Useful for adding a bit of flavor to terminal sessions or CI logs.

## Usage

```sh
python -m nightly_quote_of_the_day
```

or

```sh
python utils/nightly-quote-of-the-day/src/quote.py
```

## How it works

The script contains a curated list of quotes. It selects one at random using `random.choice` and prints it to stdout.

## Testing

Run the tests with:

```sh
python -m unittest discover utils/nightly-quote-of-the-day/tests
```
