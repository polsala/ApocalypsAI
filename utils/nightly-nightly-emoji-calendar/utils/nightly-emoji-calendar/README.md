# Nightly Emoji Calendar

A tiny utility that prints a month calendar using emojis:

- **Weekdays** → `📅`
- **Weekends** → `🌞`

## Usage

```bash
# Run for the current month
python -m nightly_emoji_calendar.src.calendar

# Or specify a year and month (1‑based)
python -m nightly_emoji_calendar.src.calendar 2024 10
```

The script prints a calendar where each day is replaced by the appropriate emoji, keeping the familiar Monday‑to‑Sunday layout.

## API

```python
from nightly_emoji_calendar.src.calendar import generate_calendar

calendar_str = generate_calendar(2024, 10)
print(calendar_str)
```

`generate_calendar(year, month)` returns a string representation of the month calendar with emojis.

## Why?

Quickly glance at the month’s weekend distribution without leaving the terminal, and enjoy a splash of emoji fun.
