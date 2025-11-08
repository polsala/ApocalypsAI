# Emoji Clock

Utility that converts an hour (0‑23) into the corresponding clock‑face emoji. Handy for adding time‑of‑day emojis to chat messages, logs, or markdown.

## Installation

Copy the `src/emoji_clock.py` file into your project or run it directly.

## Usage

```python
from emoji_clock import get_clock_emoji

print(get_clock_emoji(14))  # 🕑
```

CLI:

```bash
python -m src.emoji_clock 14
# Output: 🕑
```

## Tests

Run with pytest:

```bash
pytest -q utils/emoji-clock/tests
```
