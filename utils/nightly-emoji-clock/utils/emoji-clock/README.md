# Emoji Clock Utility

**emoji‑clock** is a tiny, self‑contained Python utility that turns an ISO‑8601 timestamp into a friendly string containing:

1. The appropriate clock emoji for the hour (🕐‑🕛).
2. A formatted 12‑hour time.
3. A relative phrase such as "in 3 hours" or "2 days ago".

It works offline, has no external dependencies beyond the Python 3.11 standard library, and ships with deterministic unit tests that mock the current time.

## Installation

```bash
# From the repository root
python -m venv .venv
source .venv/bin/activate
pip install -e utils/emoji-clock
```

## Usage

```python
from emoji_clock import format_time

print(format_time("2025-01-01T15:30:00+00:00"))
# → 🕒 3:30 PM (in 3 hours)   # assuming now is 2025‑01‑01 12:30 UTC
```

You can also run it as a script:

```bash
python -m emoji_clock "2025-01-01T15:30:00+00:00"
```

## Testing

```bash
pytest utils/emoji-clock/tests
```

The test suite uses `unittest.mock` to freeze the current time, guaranteeing deterministic results.
