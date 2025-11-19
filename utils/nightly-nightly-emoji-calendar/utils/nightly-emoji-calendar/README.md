# Nightly Emoji Calendar

Utility that prints a month calendar where weekends are highlighted with emojis (🌞 for Saturday, 🌜 for Sunday). Handy for quick visual planning directly in the terminal.

## Usage

```bash
python -m utils.nightly-emoji-calendar.src.calendar 2023 1
```

Outputs:

```
   January 2023
Mo Tu We Th Fr Sa Su
            🌞 🌜
 3  4  5  6  7 🌞 🌜
10 11 12 13 14 🌞 🌜
17 18 19 20 21 🌞 🌜
24 25 26 27 28 🌞 🌜
31
```

## API

```python
from utils.nightly_emoji_calendar.src.calendar import render_month
print(render_month(2023, 1))
```

## Tests

Run with `pytest`:

```bash
pytest utils/nightly-emoji-calendar/tests
```
