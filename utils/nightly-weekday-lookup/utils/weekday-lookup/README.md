# Weekday Lookup Utility

**Purpose**: Quickly determine the day of the week (Monday‑Sunday) for any Gregorian calendar date without external services.

## Features
- Pure Python implementation (no dependencies).
- Exposes a `get_weekday(year, month, day) -> str` function for library use.
- Provides a small CLI: `python -m weekday_lookup <year> <month> <day>`.
- Fully tested with deterministic unit tests.

## Usage
```bash
# As a library
>>> from weekday_lookup import get_weekday
>>> get_weekday(2025, 11, 9)
'Sunday'

# As a script
$ python -m weekday_lookup 2025 11 9
Sunday
```

## Implementation Details
The algorithm is based on **Zeller's Congruence**, adjusted for the Gregorian calendar. It works for all dates from year 1583 onward (the start of the Gregorian reform).

## Testing
Run the tests with:
```bash
python -m unittest discover -s utils/weekday-lookup/tests
```
All tests are offline and deterministic.
