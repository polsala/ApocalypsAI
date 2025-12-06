# Timezone Converter CLI

A lightweight, self‑contained command‑line tool that converts an ISO‑8601 timestamp from one IANA time zone to another.

## Features
- No third‑party dependencies – uses only the Python standard library (`zoneinfo`, `datetime`, `argparse`).
- Works on any platform with Python 3.11+.
- Deterministic unit tests that run offline.

## Installation
```bash
# Clone the repository (or copy the folder) and run the script directly:
python utils/timezone-converter-cli/src/convert.py --help
```

## Usage
```bash
# Convert a timestamp from New York to London
python utils/timezone-converter-cli/src/convert.py \
    --timestamp "2025-01-01T12:00:00" \
    --from-tz "America/New_York" \
    --to-tz "Europe/London"
```

The script prints the converted timestamp in ISO‑8601 format with the target zone offset.

## Testing
```bash
python -m unittest utils/timezone-converter-cli/tests/test_convert.py
```

All tests are deterministic and do not require network access.
