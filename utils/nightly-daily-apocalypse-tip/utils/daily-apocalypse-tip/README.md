# Daily Apocalypse Tip

A tiny, self‑contained Python utility that prints a *daily* apocalypse‑survival tip. The tip is chosen deterministically from a static list based on the current date, so the same date always yields the same tip.

## Features

- Zero external dependencies (only the Python standard library).
- Simple CLI: `python -m src.tip_generator` prints today’s tip.
- Library API: `get_tip_for_date(date: datetime.date) -> str`.
- Fully tested with deterministic, offline unit tests.

## Installation

Just copy the `utils/daily-apocalypse-tip` folder into your repository. No `pip install` required.

## Usage

```bash
# Run the CLI (prints today’s tip)
python -m src.tip_generator
```

Or import the function in your own code:

```python
from src.tip_generator import get_tip_for_date
import datetime

print(get_tip_for_date(datetime.date.today()))
```

## Running the Tests

```bash
# From the utility root directory
python -m pytest tests
```

The tests are deterministic and use no network calls.
