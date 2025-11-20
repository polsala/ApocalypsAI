# Nightly Emoji Calendar

A tiny Python utility that prints the current month's calendar to the console, decorating weekends with 🌞 (Saturday) and 🌜 (Sunday) emojis and optionally marking a list of holiday dates with 🎉.

## Features
- Zero external dependencies (uses only the Python standard library).
- Deterministic output for a given month/year.
- Simple CLI: `python -m src.emoji_calendar [--holidays YYYY-MM-DD, ...]`.
- Includes a comprehensive test suite that mocks the current date.

## Usage
```bash
python -m src.emoji_calendar
# or with custom holidays
python -m src.emoji_calendar --holidays 2025-12-25,2025-12-31
```

The output looks like:
```
      📅 October 2025
Mo Tu We Th Fr Sa Su
          1 🌞 2 🌜
 3  4  5  6  7 🌞 🌜
 8  9 10 11 12 🌞 🌜
13 14 15 16 17 🌞 🌜
18 19 20 21 22 🌞 🌜
23 24 25 26 27 🌞 🌜
28 29 30 31 🌞 🌜
```

## Testing
Run the tests with:
```bash
python -m unittest discover -s tests
```
All tests are offline and use mocks to freeze the current date.
