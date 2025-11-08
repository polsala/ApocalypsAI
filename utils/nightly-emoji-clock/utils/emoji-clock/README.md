# Emoji Clock Utility

## Summary
A tiny, dependency‑free Python utility that maps a `datetime` hour to the matching clock‑face emoji (🕛‑🕚). Perfect for sprinkling a bit of visual time‑keeping into logs, chat messages, or generated markdown.

## Installation
The utility is self‑contained – just copy the `src/emoji_clock.py` file into your project or import it directly from this repository.

## Usage
```python
from datetime import datetime
from src.emoji_clock import get_clock_emoji

now = datetime.now()
print(get_clock_emoji(now))  # e.g. 🕒 for 3 PM
```

## API
- `get_clock_emoji(dt: datetime) -> str`
  - **dt** – a `datetime` instance (timezone‑aware or naive).
  - **returns** – the Unicode clock‑face emoji representing the hour of `dt` on a 12‑hour clock.

## Testing
Run the bundled tests with `pytest`:
```bash
cd utils/emoji-clock
pytest -q
```

## License
MIT – see the repository root for details.
