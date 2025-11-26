# Nightly Emoji Clock

**Utility name:** `nightly-emoji-clock`

## What it does
`nightly-emoji-clock` turns a 24‑hour time string (e.g. `14:30`) into the closest clock‑face emoji. It supports full‑hour and half‑hour granularity:

| Time | Emoji |
|------|-------|
| 00:00 / 12:00 | 🕛 |
| 01:00 | 🕐 |
| 01:30 | 🕜 |
| … | … |
| 23:30 | 🕦 |

The conversion follows the standard 12‑hour clock face emojis provided by Unicode.

## Usage
```bash
python -m nightly_emoji_clock.src.clock 14:45
# → 🕞 (3:30 PM)
```

If the minutes are not exactly `00` or `30`, they are rounded to the nearest half hour.

## Installation
The utility is self‑contained and requires only Python 3.11+. No external dependencies.

## Testing
Run the bundled tests with:
```bash
python -m unittest discover -s utils/nightly-emoji-clock/tests
```
