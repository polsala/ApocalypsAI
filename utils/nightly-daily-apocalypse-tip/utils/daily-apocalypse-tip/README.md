# Daily Apocalypse Tip

A tiny, self‑contained Python utility that prints a *deterministic* survival tip for the current day (or any date you provide). The tip is chosen from a curated list using the date's ordinal value, so the same date always yields the same tip – perfect for scripting, terminal widgets, or just a daily chuckle.

## Features

- Zero external dependencies (standard library only).
- Callable as a module function `get_tip(date: datetime.date) -> str`.
- Executable script `python -m daily_apocalypse_tip` prints today’s tip.
- Optional `--date YYYY-MM-DD` argument to query a specific day.
- Fully tested with deterministic offline unit tests.

## Usage

```bash
# Print today's tip
python -m daily_apocalypse_tip

# Print tip for a specific date
python -m daily_apocalypse_tip --date 2023-01-01
```

Or import in your own code:

```python
from daily_apocalypse_tip import get_tip
import datetime

print(get_tip(datetime.date.today()))
```

## Adding New Tips

Edit `src/tip_generator.py` and extend the `TIPS` list. The selection algorithm automatically incorporates new entries.
