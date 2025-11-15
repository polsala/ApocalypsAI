# Daily Zen Quote Generator

A tiny, self‑contained utility that returns a *deterministic* quote of the day based on the current date. No network access, no external data files – the quotes are baked into the source code.

## Features
- Zero dependencies (standard library only).
- Deterministic output – the same date always yields the same quote.
- Simple CLI (`python -m daily_zen_quote_generator`) and importable function.
- Fully tested with offline, deterministic unit tests.

## Installation
Copy the `utils/daily-zen-quote-generator` folder into your project and add the `src` directory to your `PYTHONPATH` or install it as a package if you wish.

```bash
# Example usage directly from the repository root
python -m utils.daily-zen-quote-generator.src.main
```

## Usage
```python
from utils.daily-zen-quote-generator.src.main import get_quote_of_the_day

print(get_quote_of_the_day())  # Uses today's date
```

You can also supply a custom `datetime.date` object (useful for testing or generating quotes for past/future dates):

```python
import datetime
custom_date = datetime.date(2023, 1, 1)
print(get_quote_of_the_day(custom_date))
```

## Testing
Run the bundled tests with `pytest` or the standard library `unittest` runner:

```bash
python -m unittest discover -s utils/daily-zen-quote-generator/tests
```
