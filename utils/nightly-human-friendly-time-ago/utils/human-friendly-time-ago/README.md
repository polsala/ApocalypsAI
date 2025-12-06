# Human‑Friendly Time‑Ago Utility

A tiny, self‑contained Python library that turns a `datetime` (or ISO‑8601 string) into a friendly, relative description such as:

- `just now`
- `5 min ago ⏳`
- `2 h ago ⏰`
- `yesterday 🌅`
- `3 days ago`
- `on Jan 2, 2023`

## Features

- **Zero dependencies** – only the Python standard library.
- Accepts `datetime.datetime` objects **or** ISO‑8601 strings.
- Optional `now` argument for deterministic testing / custom reference time.
- Emoji‑enhanced output for a whimsical touch.

## Installation

Copy the folder `utils/human-friendly-time-ago/` into your project and import:

```python
from utils.human-friendly-time-ago.src.timeago import time_ago
```

## Usage

```python
from datetime import datetime, timedelta
from utils.human-friendly-time-ago.src.timeago import time_ago

past = datetime.utcnow() - timedelta(minutes=42)
print(time_ago(past))  # → "42 min ago ⏳"
```

## API

```python
def time_ago(ts: Union[datetime, str], *, now: Optional[datetime] = None, emoji: bool = True) -> str:
    """Return a human‑friendly relative time string.

    Parameters
    ----------
    ts:
        The timestamp to describe – either a ``datetime`` object (aware or naive, assumed UTC) or an ISO‑8601 string.
    now:
        Reference point for the calculation. If ``None`` the current UTC time is used. Supplying a value makes the function deterministic for testing.
    emoji:
        When ``True`` (default) an appropriate emoji is appended.
    """
```

## Testing

Run the bundled tests with `pytest`:

```bash
python -m pip install pytest  # if not already installed
pytest utils/human-friendly-time-ago/tests
```

All tests are offline and deterministic – they rely on the optional ``now`` argument rather than mocking the system clock.
