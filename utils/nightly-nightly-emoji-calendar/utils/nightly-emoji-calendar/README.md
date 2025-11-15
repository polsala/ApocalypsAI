# Nightly Emoji Calendar

**What it does**

`nightly-emoji-calendar` is a lightweight, zero‑dependency Python 3.11 utility that:

1. Returns a fun emoji representing any given date (based on the day of the week).
2. Generates a simple month‑view calendar where each day is replaced by its emoji.
3. Provides a tiny CLI for quick look‑ups.

The tool is completely self‑contained – no external services, no network calls, and deterministic unit tests that run offline.

## Installation & Usage

```bash
# Clone the repository (or copy the folder) and install the utility in a venv
python -m venv .venv && source .venv/bin/activate
pip install -e utils/nightly-emoji-calendar
```

```bash
# CLI examples
python -m utils.nightly-emoji-calendar.src.emoji_calendar 2025-12-25   # 🎄 (Saturday)
python -m utils.nightly-emoji-calendar.src.emoji_calendar --month 2025 12
```

## API

```python
from utils.nightly_emoji_calendar.src.emoji_calendar import get_emoji_for_date, month_calendar

emoji = get_emoji_for_date(date(2025, 12, 25))
weeks = month_calendar(2025, 12)  # List[List[Tuple[int, str]]]
```

## Testing

Run the bundled tests with:

```bash
pytest utils/nightly-emoji-calendar/tests
```

All tests are deterministic and use mocks where needed.
