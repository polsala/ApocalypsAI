# Nightly Emoji Clock

`nightly-emoji-clock` converts a given time (or the current system time) into a string of clock‑face emojis representing the hour and minute.  

## Features

- **Pure Python 3.11** – no external dependencies.
- **Deterministic** – tests mock `datetime` so they run offline.
- **Whimsical** – perfect for adding a splash of fun to logs, CI output, or chat messages.

## Usage

```bash
python -m utils.nightly-emoji-clock.src.emoji_clock
```

Will print something like:

```
🕒🕧
```

where the first emoji is the hour (rounded to the nearest hour) and the second is the minute (rounded to the nearest half‑hour).

You can also import the helper:

```python
from utils.nightly-emoji-clock.src.emoji_clock import get_emoji_time

print(get_emoji_time())  # uses current UTC time
print(get_emoji_time(datetime.datetime(2025, 1, 1, 14, 22)))
```

## Tests

Run the test suite with:

```bash
python -m pytest utils/nightly-emoji-clock/tests
```
