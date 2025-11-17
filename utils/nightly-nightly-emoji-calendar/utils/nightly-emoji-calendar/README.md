# Nightly Emoji Calendar

Utility that prints a month calendar where weekends are replaced with emojis (Saturday 🌞, Sunday 🌜). Helpful for quick visual planning without looking up a full calendar.

## Usage

```bash
python -m nightly_emoji_calendar.src.calendar 2023 3
```

Will output:

```
Mo Tu We Th Fr Sa Su
      1  2  3 🌞 🌜
 6  7  8  9 10 🌞 🌜
13 14 15 16 17 🌞 🌜
20 21 22 23 24 🌞 🌜
27 28 29 30 31
```

## API

`render_month(year: int, month: int) -> str` returns the formatted string.
