# Nightly Emoji Clock

`nightly-emoji-clock` is a tiny, self‑contained Python utility that turns a `datetime` into a readable emoji string.

## Features
- Maps the hour to the appropriate clock‑face emoji (🕛‑🕚).
- Appends the minute as a zero‑padded number.
- Pure Python, no external dependencies.
- Includes deterministic unit tests that mock the current time.

## Installation & Usage
```bash
# Clone the repository (or copy the folder) and run:
python -m utils.nightly-emoji-clock.src.emoji_clock
```

```python
from utils.nightly-emoji-clock.src.emoji_clock import get_emoji_time

print(get_emoji_time())  # e.g. "🕒 07"
```

## Testing
```bash
python -m unittest discover -s utils/nightly-emoji-clock/tests
```

## License
MIT © ApocalypsAI
