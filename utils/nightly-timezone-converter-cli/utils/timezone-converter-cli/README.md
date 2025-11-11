# Timezone Converter CLI

A whimsical yet practical command‑line tool that converts a datetime from one timezone to another.

## Features
- Pure Python 3.11 – no external dependencies.
- Uses the standard‑library `zoneinfo` module for accurate IANA timezone handling.
- Simple CLI: `python -m timezone_converter <datetime> <from_tz> <to_tz>`
- Returns an ISO‑8601 string with the target offset.

## Installation
```bash
# From the repository root
cd utils/timezone-converter-cli
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt  # (empty, kept for consistency)
```

## Usage
```bash
# Convert 2023‑01‑01 12:00:00 UTC to America/New_York
python -m timezone_converter "2023-01-01T12:00:00" UTC America/New_York
# → 2023-01-01T07:00:00-05:00
```

## Running Tests
```bash
python -m unittest discover -s tests
```

## License
MIT © ApocalypsAI
