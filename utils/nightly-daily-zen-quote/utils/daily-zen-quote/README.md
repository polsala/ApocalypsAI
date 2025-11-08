# Daily Zen Quote

`daily-zen-quote` is a lightweight, zero‑dependency Python utility that prints a short, uplifting Zen‑style quote for the current day (or any date you provide). The quote selection is deterministic – it is derived from the calendar date, so the same day always yields the same quote without any network calls.

## Features

- **Offline & deterministic** – no external APIs, no randomness.
- **Tiny footprint** – pure standard‑library Python 3.11.
- **CLI & importable** – run as a script or import the function in your own code.

## Installation

Copy the `utils/daily-zen-quote` folder into your repository and add it to your Python path, or install it as a package if you wish.

```bash
# Example: run directly from the repo root
python -m utils.daily-zen-quote.src.zen_quote
```

## Usage

```python
from utils.daily-zen-quote.src.zen_quote import get_zen_quote

# Get today's quote
print(get_zen_quote())

# Get a quote for a specific date
import datetime
print(get_zen_quote(datetime.date(2023, 1, 1)))
```

## Testing

Run the bundled tests with `pytest` (or `python -m unittest`).

```bash
cd utils/daily-zen-quote
python -m unittest discover -s tests
```

---

*Created by the ApocalypsAI Nightly Integrator.*
