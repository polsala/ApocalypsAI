# Human Relative Time Utility

A tiny, dependency‑free Python library that turns absolute timestamps into friendly relative phrases.

## Features
- Handles past and future dates.
- Supports seconds, minutes, hours, days, weeks, months, and years.
- Returns "just now" for timestamps within a few seconds.

## Installation
```bash
# This utility is self‑contained; just copy the folder into your project.
```

## Usage
```python
from utils.human_relative_time.src.relative_time import format_relative
from datetime import datetime, timezone

now = datetime.now(timezone.utc)
future = now + timedelta(days=2)
print(format_relative(future, now))  # → "in 2 days"
```

## Testing
Run the bundled tests with:
```bash
python -m unittest discover -s utils/human_relative_time/tests
```
