# Emoji Calendar

Generate a month calendar where Saturdays and Sundays are highlighted with emojis for a quick visual schedule.

## Features

- 🎉 Saturdays are replaced with a party emoji.
- 🌞 Sundays are replaced with a sun emoji.
- Works offline, no external dependencies.

## Usage

```bash
python -m src.emoji_calendar <year> <month>
```

Example:

```bash
python -m src.emoji_calendar 2025 11
```

Will output a calendar for November 2025 with emojis on weekends.

## Files

- `src/emoji_calendar.py` – core implementation.
- `tests/test_emoji_calendar.py` – deterministic offline tests.
