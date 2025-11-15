# Nightly Emoji Clock

A tiny utility that renders the current time (hour and minute) as emoji digits.

## Installation

The utility is self‑contained; just copy the `src/` folder into your project or run it directly from the repository.

## Usage

```bash
python -m utils.nightly-emoji-clock.src.emoji_clock
```

Typical output:

```
0️⃣9️⃣:0️⃣5️⃣
```

## API

```python
from emoji_clock import get_emoji_time

# Get the current time as emojis
emoji_time = get_emoji_time()

# Or provide a specific datetime
from datetime import datetime
emoji_time = get_emoji_time(datetime(2022, 12, 31, 23, 59))
```

`get_emoji_time(dt: datetime | None = None) -> str`

* Returns a string formatted as `HH:MM` where each digit is replaced by its corresponding emoji.
* If `dt` is omitted, the local current time is used.

## Tests

Run the test suite with:

```bash
python -m unittest discover -s utils/nightly-emoji-clock/tests
```

The tests are deterministic and use mocks, so they work offline.
