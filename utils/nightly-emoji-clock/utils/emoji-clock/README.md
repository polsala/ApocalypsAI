# Emoji Clock Utility

## Overview

`emoji-clock` is a tiny Python utility that prints the current time using clock‑face emojis. Each hour maps to its corresponding emoji (🕛 – 🕚). The tool is useful for:

- Adding fun timestamps to commit messages, chat logs, or documentation.
- Quickly visualising the hour without reading numbers.

## Usage

```bash
python -m src.emoji_clock
```

The script prints a single line, e.g.:

```
🕒
```

## API

```python
from src.emoji_clock import get_emoji_time

# Returns the emoji for the current hour
emoji = get_emoji_time()
```

You can also pass a custom `datetime` object for testing or other purposes.

## Testing

Run the test suite with:

```bash
python -m unittest discover -s utils/emoji-clock/tests
```

The tests mock the current time to guarantee deterministic results.
