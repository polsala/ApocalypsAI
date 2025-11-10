# Emoji Relative Time

`emoji-relative-time` is a lightweight, zero‑dependency Python 3.11 utility that turns a past timestamp into a friendly, emoji‑enhanced relative‑time string.

## Features

- Human‑readable output like `🕑 5 minutes ago` or `📅 2 days ago`.
- Emoji selection for seconds, minutes, hours, days, weeks, months, and years.
- Pure standard‑library implementation – works offline.
- Comes with a tiny test suite that runs deterministically.

## Installation

Copy the `src/relative_time.py` file into your project or install the utility via the generated folder.

## Usage

```python
from datetime import datetime, timedelta
from src.relative_time import format_relative_time

past = datetime.now() - timedelta(minutes=5)
print(format_relative_time(past))  # → "🕑 5 minutes ago"
```

You can also provide a custom `now` reference:

```python
now = datetime(2025, 1, 1, 12, 0, 0)
past = datetime(2025, 1, 1, 11, 45, 0)
print(format_relative_time(past, now))  # → "🕑 15 minutes ago"
```

## Testing

Run the tests with:

```bash
python -m unittest discover -s tests
```

All tests are deterministic and do not require network access.
