# Nightly Relative Time Converter

A tiny, dependency‑free utility that turns a `datetime` into a friendly, human‑readable relative string such as:

- `just now`
- `45 seconds ago`
- `in 3 minutes`
- `2 days ago`
- `in 1 year`

## Why?

When building CLIs, bots, or logs you often want to show *when* something happened without overwhelming the user with exact timestamps. This helper does the math for you and works offline.

## Installation

The utility is self‑contained. Just copy the `src/relative_time.py` file into your project or import it directly from this repo.

```bash
# Example usage (Python 3.11+)
python - <<'PY'
from datetime import datetime, timedelta
from utils.nightly-relative-time-converter.src.relative_time import format_relative_time

now = datetime.utcnow()
print(format_relative_time(now - timedelta(seconds=30)))   # 30 seconds ago
print(format_relative_time(now + timedelta(days=2)))      # in 2 days
PY
```

## API

```python
format_relative_time(target: datetime, reference: Optional[datetime] = None) -> str
```

- **target** – The datetime you want to describe.
- **reference** – The point of comparison (defaults to `datetime.utcnow()`).

The function returns a short English phrase.

## Testing

Run the bundled tests with `pytest`:

```bash
pytest utils/nightly-relative-time-converter/tests
```
