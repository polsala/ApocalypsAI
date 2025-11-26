# Emoji Clock Utility

## Overview

`emoji_clock` provides a single function `get_emoji_clock()` that returns a string
representing the current time with a clock‑face emoji and zero‑padded minutes.

```bash
$ python -m emoji_clock
🕒 07m
```

## API

```python
from src.clock import get_emoji_clock

# Use the current time
print(get_emoji_clock())

# Or supply a specific datetime
from datetime import datetime
print(get_emoji_clock(datetime(2023, 1, 1, 13, 27)))  # 🕐 27m
```

## Tests

Run the test suite with:

```bash
python -m unittest discover -s tests
```

The tests are deterministic and offline, using mocks where appropriate.
