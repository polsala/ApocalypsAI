# Nightly ISO‑8601 Duration Parser

A tiny, self‑contained utility that converts ISO‑8601 duration strings into a total number of seconds.

## Features
- Supports years, months, weeks, days, hours, minutes, and seconds.
- Returns an integer number of seconds (rounded down for fractional units).
- No third‑party dependencies – pure Python 3.11.

## Usage
```bash
python -m nightly_iso8601_duration_parser "PT1H30M"
# → 5400
```

Or import the function:
```python
from nightly_iso8601_duration_parser import parse_duration
seconds = parse_duration("P2DT3H")  # 2 days + 3 hours = 183600 seconds
```

## Testing
Run the bundled tests with:
```bash
python -m unittest discover -s utils/nightly-iso8601-duration-parser/tests
```
