# Timezone Converter Utility

A lightweight, pure‑Python command‑line tool that converts a date‑time string from one IANA time‑zone to another.

## Features

- No external dependencies – uses the standard library `zoneinfo` (Python ≥3.9).
- Accepts a date‑time in `YYYY-MM-DD HH:MM` format.
- Handles ambiguous or non‑existent times gracefully (uses `fold` flag).
- Provides helpful error messages.

## Installation & Usage

```bash
# Clone the repository (or copy the folder) and run the script directly
python -m utils.timezone-converter.src.convert \
    --from "America/New_York" \
    --to "Asia/Tokyo" \
    --time "2025-12-31 23:30"
```

The command prints the converted time in the target zone:

```
2025-01-01 13:30 (Asia/Tokyo)
```

## Testing

Run the bundled tests with `pytest`:

```bash
cd utils/timezone-converter
pytest -q
```

All tests are deterministic and offline.
