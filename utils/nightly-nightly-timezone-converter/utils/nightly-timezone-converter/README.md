# Nightly Timezone Converter

Utility to convert date‑time strings between IANA time zones.

## Usage

```bash
python -m src.convert "2025-11-19 15:30" America/New_York Asia/Tokyo
```

The command prints an ISO‑8601 timestamp with the target zone offset, e.g.
```
2025-11-20T05:30:00+09:00
```

## Details

- **Input format**: `%Y-%m-%d %H:%M` (24‑hour clock)
- **Output**: ISO‑8601 string with UTC offset
- Relies only on the Python standard library (`datetime`, `zoneinfo`).

## Tests

Run the test suite with:

```bash
cd utils/nightly-timezone-converter
pytest
```

The tests are deterministic and run offline.
