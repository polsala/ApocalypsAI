# ASCII Calendar Generator

A tiny, dependency‑free utility that prints a classic text‑based calendar for any month and year.

## Features
- Offline – uses only the Python standard library.
- Optional highlighting of the current day (wrapped in `*` characters).
- Simple CLI: `python -m src.calendar_generator <year> <month> [--highlight]`.

## Installation
Just copy the `utils/ascii-calendar-generator` folder into your repository. No additional packages are required.

## Usage
```bash
# Print March 2023
python -m src.calendar_generator 2023 3

# Highlight today if the month matches the current date
python -m src.calendar_generator 2023 3 --highlight
```

## API
```python
from src.calendar_generator import generate_calendar

cal_str = generate_calendar(month=3, year=2023, highlight_today=False)
print(cal_str)
```

## Testing
Run the test suite with:
```bash
python -m unittest discover -s tests
```
