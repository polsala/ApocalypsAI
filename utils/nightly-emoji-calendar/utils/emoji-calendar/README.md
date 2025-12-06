# Emoji Calendar

A whimsical CLI utility that prints a month calendar where each day is prefixed by an emoji representing its weekday.

## Features
- No external dependencies (uses only the Python standard library).
- `render_month(year, month)` returns a formatted string.
- Run as a script to display the current month.

## Usage

```sh
python -m utils.emoji-calendar.src.emoji_calendar
```

Or import in Python:

```python
from utils.emoji-calendar.src.emoji_calendar import render_month
print(render_month(2023, 10))
```

## Example Output (October 2023)

```
October 2023
Mo Tu We Th Fr Sa Su
                     🌞 1
🌜 2 🌛 3 🌞 4 🌜 5 🌛 6 🌞 7 🌜 8
🌛 9 🌞10 🌜11 🌛12 🌞13 🌜14 🌛15
🌞16 🌜17 🌛18 🌞19 🌜20 🌛21
🌞22 🌜23 🌛24 🌞25 🌜26 🌛27
🌞28 🌜29 🌛30 🌞31       
```

## Testing

Run the bundled tests with:

```sh
python -m unittest discover utils/emoji-calendar/tests
```
