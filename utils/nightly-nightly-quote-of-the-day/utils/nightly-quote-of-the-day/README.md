# Nightly Quote of the Day

Utility that prints a deterministic **Quote of the Day** based on the current date. It requires **only** the Python standard library, making it safe to run in any environment without network access.

## Usage

```bash
python -m nightly_quote_of_the_day
```

The command prints a single line containing the quote for today.

## How it works

* A small, curated list of inspirational quotes lives inside the package.
* The current date (or a supplied `datetime.date`) is converted to an integer via `date.toordinal()`.
* That integer seeds Python's `random.Random`, guaranteeing the same quote for the same date across all machines.

## Testing

Run the test suite with:

```bash
python -m unittest discover -s utils/nightly-quote-of-the-day/tests
```

The tests mock the date to ensure deterministic output.
