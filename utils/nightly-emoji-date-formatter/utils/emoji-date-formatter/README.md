# Emoji Date Formatter

`emoji-date-formatter` converts a `datetime.date` (or an ISO‑8601 date string) into a fun, human‑readable emoji representation.

## Features
- **Library API** – call `format_date(date)` to get an emoji string.
- **CLI** – `python -m emoji_date_formatter 2023-12-25` prints the result.
- No external dependencies beyond the Python standard library.

## Installation
Simply copy the `utils/emoji-date-formatter` folder into your project or install it as a submodule.

## Usage
```python
from datetime import date
from src.formatter import format_date

print(format_date(date(2023, 12, 25)))  # 🎄📅
```

Or via the command line:
```bash
python -m src.formatter 2023-12-25
# Output: 🎄📅
```

## How it works
- The month is mapped to a themed emoji (e.g., January → ❄️, February → ❤️, …, December → 🎄).
- The day is represented by the day‑of‑month number surrounded by the calendar emoji 📅.
- The year is omitted for brevity; you can prepend it yourself if needed.

## Testing
Run the bundled tests with:
```bash
python -m unittest discover -s utils/emoji-date-formatter/tests
```
