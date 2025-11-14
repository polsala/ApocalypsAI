# Emoji Calendar Converter

Convert dates (YYYY-MM-DD) into a string of emojis and back again. Useful for adding playful timestamps to logs, commit messages, or chat.

## Usage

```bash
python -m emoji_calendar 2023-10-31
# Output: 2️⃣0️⃣2️⃣3️⃣➖1️⃣0️⃣➖3️⃣1️⃣
```

## Functions

- `date_to_emoji(date_str: str) -> str`
  - Takes a date in ``YYYY-MM-DD`` format and returns an emoji representation.
- `emoji_to_date(emoji_str: str) -> str`
  - Reverses the conversion, yielding the original date string.

## Installation

The utility is self‑contained; just run the script with Python 3.11+. No external dependencies are required.
