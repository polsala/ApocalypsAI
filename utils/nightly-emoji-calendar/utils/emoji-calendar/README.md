# Emoji Calendar Utility

## Overview

`emoji-calendar` is a lightweight, self‑contained Python 3.11 utility that prints a month calendar where each day is decorated with an emoji:

- **🟦** – regular weekday
- **🟧** – weekend (Saturday & Sunday)
- **🎉** – holiday (user‑provided list of `datetime.date` objects)

The output is plain‑text, making it easy to embed in terminals, markdown files, or any other text‑based medium.

## Installation & Usage

The utility is completely self‑contained – just copy the `src/` folder into your project or run it directly from the repository.

```bash
python -m utils.emoji-calendar.src.calendar --year 2023 --month 4 --holidays 2023-04-07,2023-04-22
```

## API

```python
from utils.emoji-calendar.src.calendar import generate_calendar

calendar_str = generate_calendar(year=2023, month=4, holidays=[date(2023, 4, 7)])
print(calendar_str)
```

## Testing

Run the bundled tests with:

```bash
python -m unittest discover utils/emoji-calendar/tests
```

The tests are deterministic and use no external network resources.
