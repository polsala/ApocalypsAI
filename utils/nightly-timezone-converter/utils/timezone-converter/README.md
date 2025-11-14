# Timezone Converter

A tiny, dependency‑free Python utility that converts a datetime string from one IANA time zone to another. Useful for scripts, logs, or quick CLI conversions without needing external APIs.

## Installation

The utility is self‑contained; just copy the `src/` directory into your project or run it directly from the repository.

## Usage

```bash
python -m timezone_converter.convert "2025-01-01 15:30:00" America/New_York Asia/Tokyo
# => 2025-01-02 05:30:00+09:00
```

## API

```python
from timezone_converter.convert import convert_time

iso = convert_time(
    "2025-01-01 15:30:00",
    "America/New_York",
    "Asia/Tokyo"
)
print(iso)  # 2025-01-02 05:30:00+09:00
```

## Tests

Run the test suite with `pytest`:

```bash
pytest -q utils/timezone-converter/tests
```

The tests are deterministic and run offline.
