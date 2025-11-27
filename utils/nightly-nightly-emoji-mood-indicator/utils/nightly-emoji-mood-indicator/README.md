# Nightly Emoji Mood Indicator

## Overview

`nightly-emoji-mood-indicator` is a self‑contained Python utility that prints a single emoji representing the current time of day:

| Time range | Emoji | Meaning |
|------------|-------|---------|
| 05:00‑12:00 | 🌅 | Morning |
| 12:00‑17:00 | 🌞 | Afternoon |
| 17:00‑21:00 | 🌇 | Evening |
| 21:00‑05:00 | 🌙 | Night |

The tool is deliberately lightweight and has **no external dependencies** beyond the Python standard library. It can be invoked directly from the command line or imported as a module.

## Usage

```bash
python -m nightly-emoji-mood-indicator
```

Will output something like:

```
🌞
```

### As a library

```python
from nightly_emoji_mood_indicator import get_mood_emoji

emoji = get_mood_emoji()
print(emoji)  # 🌅, 🌞, 🌇 or 🌙 depending on the current time
```

## Testing

Run the test suite with:

```bash
python -m unittest discover -s utils/nightly-emoji-mood-indicator/tests
```

The tests are deterministic and use **mocked datetime** objects, so they never require real time or network access.

## License

MIT © ApocalypsAI
