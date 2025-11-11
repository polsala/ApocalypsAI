# Nightly Emoji Calendar

A tiny Python utility that converts a calendar date into a fun emoji representing the day of the week, along with a short, whimsical description.

## Features

- **Pure Python 3.11** – no external dependencies.
- Deterministic mapping (Monday → 🟦, Tuesday → 🟪, …, Sunday → ⬜️).
- Human‑readable one‑liner CLI for quick look‑ups.

## Installation

Copy the `src/` folder into your project or install via a direct path:

```bash
pip install ./utils/nightly-emoji-calendar/src
```

## Usage

```python
from calendar import date
from src.calendar import get_emoji_for_date, get_description_for_date

my_date = date(2023, 10, 31)  # a Tuesday
print(get_emoji_for_date(my_date))        # 🟪
print(get_description_for_date(my_date)) # "Mid‑week magic!"
```

Or from the command line:

```bash
python -m src.calendar 2023-10-31
# Output: 🟪 – Mid‑week magic!
```

## Testing

Run the bundled tests with:

```bash
python -m unittest discover -s utils/nightly-emoji-calendar/tests
```

---

*Created by the ApocalypsAI Nightly Integrator.*
