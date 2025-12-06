# Daily Whimsical Haiku

A tiny utility that prints a three‑line haiku that changes every day, but is **deterministic** – the same calendar date always yields the same poem.  It can be used for:

- Adding a daily splash of poetry to scripts or CI logs.
- Providing a fun “quote of the day” in chat bots.
- Any situation where a lightweight, offline, reproducible text generator is handy.

## Installation

The utility is self‑contained and requires only the Python 3.11 standard library.

```bash
# Clone the repository (or copy the folder) and run the script directly
python -m utils.daily-whimsical-haiku.src.haiku
```

## Usage

```bash
$ python -m utils.daily-whimsical-haiku.src.haiku
Silent moon whispers
across the sleepy town
time folds into light.
```

You can also import the function in your own code:

```python
from utils.daily-whimsical-haiku.src.haiku import generate_haiku
print(generate_haiku())
```

## How it works

The date (YYYY‑MM‑DD) is turned into an integer (e.g., `20230401`).  Simple modular arithmetic selects one line from each of three predefined word banks, guaranteeing the same output for the same date without any external randomness or network calls.

## Testing

Run the bundled tests with:

```bash
python -m unittest discover -s utils/daily-whimsical-haiku/tests
```

---

*Created by the ApocalypsAI Nightly Integrator.*
