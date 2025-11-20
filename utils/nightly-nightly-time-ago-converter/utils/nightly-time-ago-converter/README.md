# Nightly Time‑Ago Converter

A tiny, self‑contained Python utility that turns a `datetime` (or UNIX timestamp) into a friendly relative‑time string such as:

- `just now`
- `5 seconds ago`
- `2 minutes ago`
- `3 hours ago`
- `yesterday`
- `2 days ago`
- `last week`
- `3 weeks ago`
- `last month`
- `2 months ago`
- `last year`
- `3 years ago`

## Features

- Pure‑Python, no external dependencies.
- Works with timezone‑aware or naive `datetime` objects.
- Deterministic unit tests using `unittest.mock`.

## Usage

```python
from datetime import datetime, timezone
from src.ago import time_ago

# naive datetime (assumed local time)
print(time_ago(datetime(2025, 11, 20, 12, 0, 0)))

# aware datetime (UTC)
print(time_ago(datetime(2025, 11, 20, 12, 0, 0, tzinfo=timezone.utc)))
```

## Running the tests

```bash
python -m unittest discover -s utils/nightly-time-ago-converter/tests
```
