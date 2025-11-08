# Emoji Date Formatter

A tiny, self‑contained Python utility that turns a standard ISO date string (`YYYY‑MM‑DD`) into a fun emoji string.

## Features

- **Digit → Emoji**: each numeral is replaced by its corresponding emoji (e.g., `0` → `0️⃣`).
- **Month → Seasonal Emoji**: the month number is mapped to a seasonal emoji (e.g., `01` → `🌱` for January).
- **Zero‑dependency**: pure Python 3.11, no external packages.
- **CLI & library usage**.

## Installation

Copy the folder `utils/emoji-date-formatter` into your project and run the tests to verify everything works:

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt  # (none needed)
python -m pytest utils/emoji-date-formatter/tests
```

## Usage

### As a library

```python
from utils.emoji_date_formatter.src.formatter import format_date

print(format_date("2025-12-31"))
# 🎄 2️⃣2️⃣❄️
```

### As a CLI

```bash
python -m utils.emoji_date_formatter.src.formatter 2025-12-31
# 🎄 2️⃣2️⃣❄️
```

## How it works

1. Split the input string into year, month, and day.
2. Replace each digit with its emoji counterpart.
3. Replace the month number with a predefined seasonal emoji.
4. Join the parts with a space.

## Testing

Run the bundled pytest suite:

```bash
pytest utils/emoji-date-formatter/tests
```

All tests are deterministic and offline.
