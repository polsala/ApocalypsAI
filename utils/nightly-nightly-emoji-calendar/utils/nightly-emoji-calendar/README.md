# Nightly Emoji Calendar

A tiny Python utility that turns any date into a whimsical emoji representation.

## Features
- Emoji for each weekday (e.g., Monday → 📅)
- Recognizes a few common holidays and returns a special emoji.
- Simple CLI: `python -m emoji_calendar 2025-01-01`

## Installation
Copy the `src/` folder into your project or run directly with Python 3.11.

## Usage
```python
from datetime import date
from src.emoji_calendar import get_emoji_for_date

print(get_emoji_for_date(date.today()))
# → "📅" (or a holiday emoji)
```

## Tests
Run `pytest` inside the utility folder:
```bash
cd utils/nightly-emoji-calendar
pytest -q
```
