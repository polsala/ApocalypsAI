# Timezone Converter CLI

Utility to convert a datetime string from one IANA time zone to another using only the Python standard library.

## Features
- No external dependencies (uses `zoneinfo` from the stdlib).
- Simple command‑line interface.
- Returns an ISO‑8601 timestamp with the target zone offset.

## Usage
```bash
python utils/timezone-converter-cli/src/convert.py "2025-01-01 15:30" America/New_York Asia/Tokyo
```

The above prints something like:
```
2025-01-02T05:30:00+09:00
```

## Running Tests
```bash
python -m unittest utils/timezone-converter-cli/tests/test_convert.py
```
