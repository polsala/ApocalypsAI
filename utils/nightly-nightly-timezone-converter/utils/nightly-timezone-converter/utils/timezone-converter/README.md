# Nightly Timezone Converter

A whimsical yet practical utility that converts a given timestamp from one IANA time zone to another.

## Features
- Pure Python 3.11, no external dependencies.
- Works offline – uses the standard library `zoneinfo` database.
- Simple CLI interface.
- Deterministic unit tests.

## Installation
Copy the `src` directory into your project or run the script directly:
```bash
python -m timezone_converter --time "2023-01-01 12:00:00" --from "America/New_York" --to "Asia/Tokyo"
```

## Usage
```bash
python -m timezone_converter \
    --time "<TIMESTAMP>" \
    --from "<FROM_TZ>" \
    --to "<TO_TZ>" \
    [--format "<FORMAT>"]
```
- `<TIMESTAMP>` – the input time string.
- `<FROM_TZ>` – source IANA time zone (e.g., `America/New_York`).
- `<TO_TZ>` – target IANA time zone (e.g., `Asia/Tokyo`).
- `<FORMAT>` – optional `datetime.strftime` format (default: `%Y-%m-%d %H:%M:%S`).

## Example
```bash
$ python -m timezone_converter \
    --time "2023-01-01 12:00:00" \
    --from "America/New_York" \
    --to "Asia/Tokyo"
2023-01-02 02:00:00
```

## Testing
Run the tests with:
```bash
python -m unittest discover -s tests
```
