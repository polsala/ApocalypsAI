# Moon Phase Calculator

A lightweight, self‑contained utility that tells you the lunar phase for any given date.

## Features
- Pure Python 3.11, no external dependencies.
- Simple command‑line interface.
- Whimsical emoji output (🌑, 🌒, 🌓, 🌔, 🌕, 🌖, 🌗, 🌘).
- Deterministic offline tests using mocked dates.

## Installation
Just copy the `utils/moon-phase-calculator` folder into your project and run:
```bash
python -m utils.moon-phase-calculator.src.moon_phase [--date YYYY-MM-DD]
```
If `--date` is omitted, the current local date is used.

## Usage examples
```bash
$ python -m utils.moon-phase-calculator.src.moon_phase
Today (2025-11-15) is a Waxing Crescent 🌒

$ python -m utils.moon-phase-calculator.src.moon_phase --date 2025-11-01
2025-11-01 is a Full Moon 🌕
```

## How it works
The algorithm is based on the known lunation period of **29.53058867** days. It calculates the number of days since a reference new moon (2000‑01‑06) and maps the fractional lunation to one of eight standard phases.

## Testing
Run the tests with:
```bash
python -m unittest discover utils/moon-phase-calculator/tests
```
All tests are deterministic and use mocks for the current date.
