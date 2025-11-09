# Daily Zen Quote Generator

A tiny, self‑contained utility that prints a "Zen" quote for the current day. The quote is chosen deterministically from a built‑in list using the SHA‑256 hash of the ISO date string, so the same date always yields the same quote.

## Features
- No external network calls – works completely offline.
- Zero third‑party dependencies beyond the Python standard library.
- Simple CLI (`python -m src.main`) prints the quote.
- Comes with deterministic unit tests that mock the current date.

## Usage
```bash
# From the utility folder
python -m src.main
```

You can also import the helper function in your own code:
```python
from src.main import get_quote_of_the_day
print(get_quote_of_the_day())
```

## Testing
```bash
python -m unittest discover -s tests
```

The test suite uses `unittest.mock` to freeze the current date and verifies that the quote selection is deterministic.
