# Nightly ASCII Art Calendar

A whimsical utility that generates ASCII-art calendars for any month/year, with optional event markers.

## Features

- Generate a calendar for any month and year
- Mark specific dates with custom symbols
- Clean, readable ASCII output
- Command-line interface

## Usage

```bash
python src/calendar.py --year 2024 --month 12
python src/calendar.py --year 2024 --month 12 --events 2024-12-25=🎄 2024-12-31=🎆
```

## Installation

No installation required. Just run the script directly.

## Examples

### Basic Calendar

```bash
python src/calendar.py --year 2024 --month 12
```

### Calendar with Events

```bash
python src/calendar.py --year 2024 --month 12 --events 2024-12-25=🎄 2024-12-31=🎆
```

This will mark December 25th with a Christmas tree emoji and December 31st with fireworks.

## License

MIT
