# Human Time Parser

Utility to convert simple human‑readable time expressions into ISO‑8601 timestamps.

## Features

- Understands expressions like:
  - `now`
  - `in 5 seconds`
  - `10 minutes ago`
- Returns a `datetime.datetime` in UTC.
- CLI usage: `python -m human_time_parser "in 3 days"`

## Installation

Copy the `src/` folder into your project or run directly from this repository.

## API

```python
from src.parser import parse_human_time

dt = parse_human_time("in 2 days")
print(dt.isoformat())
```

## Testing

Run the bundled tests with:

```bash
python -m unittest discover -s utils/human-time-parser/tests
```
