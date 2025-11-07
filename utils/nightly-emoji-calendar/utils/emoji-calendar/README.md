# Emoji Calendar

A tiny, self‑contained Python utility that prints a month calendar where:

* **Weekends** are replaced with 🌞 (Saturday) and 🌜 (Sunday).
* **Holidays** (New Year’s Day, Thanksgiving, Christmas) are replaced with 🎉, 🦃, 🎄 respectively.

## Installation & Usage

The utility has no external dependencies beyond the Python 3.11 standard library.

```bash
# Run the calendar for October 2024
python -m utils.emoji-calendar.src.main 2024 10
```

## API

* `generate_month(year: int, month: int) -> str`
  Returns a formatted string containing the emoji‑enhanced calendar.

## Testing

Run the bundled tests with:

```bash
python -m unittest discover -s utils/emoji-calendar/tests
```
