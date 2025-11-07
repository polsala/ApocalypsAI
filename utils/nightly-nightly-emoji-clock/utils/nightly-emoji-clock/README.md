# Nightly Emoji Clock

`nightly-emoji-clock` is a tiny, self‑contained utility that tells the current time using Unicode clock face emojis. It can be used as a library function or run directly from the command line.

## Features

- **Library API**: `emoji_clock.get_emoji_time(dt: datetime) -> str`
- **CLI**: `python -m utils.nightly-emoji-clock.src.emoji_clock` prints the current time in emojis.
- **Deterministic tests**: offline unit tests mock `datetime.datetime.now`.

## Installation & Usage

The utility is pure Python 3.11 and has no external dependencies.

```bash
# Run the CLI (from the repository root)
python -m utils.nightly-emoji-clock.src.emoji_clock
```

```python
from utils.nightly-emoji-clock.src.emoji_clock import get_emoji_time
import datetime

now = datetime.datetime.now()
print(get_emoji_time(now))
```

## Emoji Mapping

| Hour | Emoji |
|------|-------|
| 0‑1  | 🕛 |
| 1‑2  | 🕐 |
| 2‑3  | 🕑 |
| 3‑4  | 🕒 |
| 4‑5  | 🕓 |
| 5‑6  | 🕔 |
| 6‑7  | 🕕 |
| 7‑8  | 🕖 |
| 8‑9  | 🕗 |
| 9‑10 | 🕘 |
|10‑11 | 🕙 |
|11‑12 | 🕚 |
|12‑13 | 🕛 |
|13‑14 | 🕐 |
|14‑15 | 🕑 |
|15‑16 | 🕒 |
|16‑17 | 🕓 |
|17‑18 | 🕔 |
|18‑19 | 🕕 |
|19‑20 | 🕖 |
|20‑21 | 🕗 |
|21‑22 | 🕘 |
|22‑23 | 🕙 |
|23‑24 | 🕚 |

Minutes are represented by the nearest half‑hour emoji (e.g., `:30` adds a half‑hour indicator). The implementation keeps it simple: it rounds minutes to the nearest 30.
