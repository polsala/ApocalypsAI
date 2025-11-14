# Nightly Emoji Clock

A tiny utility that prints the current time prefixed with a clock‑face emoji representing the hour (or half‑hour). Perfect for adding a whimsical timestamp to logs, commit messages, or chat bots.

## Usage

```bash
python -m utils.nightly-emoji-clock.src.emoji_clock
# Example output: 🕑 14:05
```

Or import the function:

```python
from utils.nightly-emoji-clock.src.emoji_clock import get_emoji_time

print(get_emoji_time())                     # uses current time
print(get_emoji_time(datetime(2023, 1, 1, 14, 45)))  # → 🕝 14:45
```

## How it works

Maps each hour and half‑hour to the corresponding Unicode clock emoji.

## Tests

Run with `pytest`:

```bash
pytest utils/nightly-emoji-clock/tests
```
