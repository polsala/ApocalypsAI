# Nightly Quote of the Day

A whimsical yet useful utility that prints a motivational quote based on the current date.

## Features

- **Deterministic**: The same date always yields the same quote.
- **Offline**: No network calls; quotes are bundled with the utility.
- **CLI**: `python -m nightly_quote_of_the_day` prints the quote for today.
- **Testable**: Unit tests mock the date to guarantee deterministic behavior.

## Usage

```bash
# Print today's quote
python -m nightly_quote_of_the_day

# Print a quote for a specific date (YYYY‑MM‑DD)
python -m nightly_quote_of_the_day --date 2023-10-31
```

## Implementation Details

- Quotes are stored in a simple Python list.
- The selection algorithm hashes the ISO‑formatted date string, takes the modulo with the number of quotes, and returns the corresponding entry.
- The CLI lives in `src/quote.py` and is exposed via the `-m` module flag.

## Testing

The test suite lives under `tests/` and uses `unittest.mock` to replace `datetime.date.today` with a fixed date, ensuring deterministic output without any external dependencies.
