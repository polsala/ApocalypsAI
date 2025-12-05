# Emoji Clock Utility

A tiny, whimsical tool that turns a time of day into a Unicode clock‑face emoji.

## Features

- **Library function** `time_to_emoji(hour, minute)` – returns the closest clock emoji.
- **CLI** – `python -m src.emoji_clock 13:45` prints the emoji.
- **Zero‑dependency** Python 3.11 implementation.
- **Fully offline deterministic tests**.

## Installation & Usage

```bash
# Clone the repository and navigate to the utility folder
cd utils/nightly-emoji-clock/utils/emoji-clock

# Run the CLI (requires Python 3.11+)
python -m src.emoji_clock 09:30
# → 🕤
```

## Library Example

```python
from src.emoji_clock import time_to_emoji

print(time_to_emoji(23, 45))  # 🕦
```

## Testing

```bash
# From the utility root folder
pytest -q
```

All tests run offline and use only the standard library.
