# Nightly Emoji Clock

A tiny utility that prints the current time as a series of clock‑face emojis.  It maps the hour (in 12‑hour format) to the corresponding emoji (🕐‑🕛) and optionally includes a half‑hour emoji when the minutes are ≥ 30.

## Features
- Zero external dependencies – pure Python 3.11.
- Provides a `get_emoji_time()` function for programmatic use.
- CLI entry point `python -m nightly_emoji_clock` prints the emoji time.
- Fully tested with deterministic mocks.

## Usage
```bash
# As a script
python -m nightly_emoji_clock
# Or import in your code
from nightly_emoji_clock import get_emoji_time
print(get_emoji_time())
```

## Implementation Details
- Hours are converted to 12‑hour format.
- If minutes are 30 or more, the half‑hour emoji (🕜‑🕧) is used.
- Seconds are ignored for simplicity.

## License
MIT © ApocalypsAI
