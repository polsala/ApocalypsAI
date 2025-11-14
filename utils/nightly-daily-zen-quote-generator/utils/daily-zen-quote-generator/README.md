# Daily Zen Quote Generator

Utility that provides a deterministic Zen quote for a given date. No network calls; uses a static list of quotes and a simple hash to select one. Ideal for terminal MOTDs, CI logs, or personal reminders.

## Usage

```bash
python -m src.quote_generator <YYYY-MM-DD>
```

or import:

```python
from src.quote_generator import get_quote_of_day
from datetime import date
print(get_quote_of_day(date.today()))
```

## How it works

- Maintains a list of ~20 Zen quotes.
- Computes SHA‑256 of the ISO date string.
- Uses the hash to pick an index modulo the list length.

## Testing

Run `pytest` in the utility folder:

```bash
cd utils/daily-zen-quote-generator
pytest
```
