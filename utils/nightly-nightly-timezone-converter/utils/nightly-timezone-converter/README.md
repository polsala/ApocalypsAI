# ChronoChameleon – Nightly Timezone Converter

A whimsical yet practical utility that converts a given datetime from a source IANA timezone to a target IANA timezone.

## Features
- Pure Python 3.11 – no external dependencies.
- Uses the standard library `zoneinfo` module (no network calls).
- Simple CLI: `python -m src.converter "2023-10-31T15:00:00" America/New_York Europe/London`
- Returns an ISO‑8601 string with the appropriate offset.

## Installation
The utility is self‑contained. Just copy the `utils/nightly-timezone-converter` folder into your project and run the script with Python 3.11+.

## Usage
```bash
python -m src.converter <datetime> <source_tz> <target_tz>
```
- `<datetime>` – ISO‑8601 format, e.g., `2023-10-31T15:00:00`
- `<source_tz>` – IANA timezone name, e.g., `America/New_York`
- `<target_tz>` – IANA timezone name, e.g., `Europe/London`

The script prints the converted datetime to stdout.

## Testing
Run the bundled tests with:
```bash
python -m unittest discover -s tests
```
All tests are deterministic and offline.
