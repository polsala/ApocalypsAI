# Nightly Emoji Clock

A tiny, self‑contained utility that prints the current local time using emojis.

## Features
- **Clock‑face emoji** for the hour (🕐‑🕛).
- **Digit emojis** for minutes (0️⃣‑9️⃣).
- Pure Python 3.11, no external dependencies.

## Usage
```bash
python -m utils.nightly-emoji-clock.src.emoji_clock
```
Or import the helper in your own code:
```python
from utils.nightly-emoji-clock.src.emoji_clock import get_emoji_time
print(get_emoji_time())
```

## Example Output
```
🕒 1️⃣5️⃣
```
*(3:15 PM)*

## Testing
Run the bundled tests with `pytest`:
```bash
cd utils/nightly-emoji-clock
pytest -q
```
