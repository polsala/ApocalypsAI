# Nightly Emoji Mood Clock

## Overview

`emoji-mood-clock` is a tiny, self‑contained Python utility that translates the hour of the day (0‑23) into a mood‑representing emoji. It’s perfect for:

- Adding a playful timestamp to logs or commit messages.
- Displaying a quick visual cue in terminal dashboards.
- Learning how to map numeric ranges to symbolic output.

The package ships with:

- **`src/emoji_clock.py`** – the core library exposing `get_emoji_for_hour(hour: int) -> str` and a small CLI.
- **`tests/test_emoji_clock.py`** – deterministic unit tests that verify the mapping for every hour.

## Installation & Usage

The utility is completely self‑contained; no external dependencies are required beyond the Python 3.11 standard library.

```bash
# Clone the repository (or copy the folder) and run the CLI
python -m utils.nightly-emoji-mood-clock.src.emoji_clock
```

You can also import the function in your own code:

```python
from utils.nightly-emoji-mood-clock.src.emoji_clock import get_emoji_for_hour

print(get_emoji_for_hour(14))  # ➜ 🌞
```

## Emoji Mapping

| Hour | Emoji |
|------|-------|
| 0‑5  | 🌙 (night) |
| 6‑8  | 🌅 (sunrise) |
| 9‑11 | 🌤️ (morning) |
| 12‑13| ☀️ (midday) |
| 14‑17| 🌞 (afternoon) |
| 18‑19| 🌇 (sunset) |
| 20‑23| 🌌 (late night) |

## Testing

Run the bundled tests with:

```bash
python -m unittest discover -s utils/nightly-emoji-mood-clock/tests
```

All tests are deterministic and run offline.
