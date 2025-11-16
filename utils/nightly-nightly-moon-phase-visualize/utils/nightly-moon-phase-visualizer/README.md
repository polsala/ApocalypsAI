# Nightly Moon Phase Visualizer

A whimsical yet practical utility that tells you the current moon phase (or the phase for any given date) and prints a cute ASCII‑art representation.

## Features

- **Programmatic API** – `get_moon_phase(date: datetime.date) -> str` returns one of eight standard phase names.
- **CLI** – Run the script to see today’s phase with ASCII art.
- **Zero external dependencies** – Pure Python 3.11 standard library.
- **Deterministic** – Uses a well‑known lunar‑cycle algorithm; no network calls.

## Usage

```bash
# From the utility folder
python -m src.moon          # prints today’s phase + ASCII art
python -m src.moon 2023-02-05  # prints the phase for the supplied date
```

Or import it in your own code:

```python
from src.moon import get_moon_phase
import datetime

phase = get_moon_phase(datetime.date.today())
print(phase)  # e.g. "Waxing Gibbous"
```

## Testing

```bash
pytest -q
```

All tests are deterministic and run offline.
