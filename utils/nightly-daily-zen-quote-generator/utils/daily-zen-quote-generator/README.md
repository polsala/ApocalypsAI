# Daily Zen Quote Generator

Utility that returns a *Zen* style quote for the current day. It works completely offline, using a small bundled list of quotes.

## Features
- Deterministic: the same date always yields the same quote.
- No external dependencies or network calls.
- Simple CLI and importable API.

## Installation
The utility is self‑contained. Just copy the `utils/daily-zen-quote-generator` folder into your project or run it directly.

## Usage
### CLI
```bash
python -m src.quote
```
Prints today’s quote to stdout.

### As a library
```python
from src.quote import get_daily_quote

print(get_daily_quote())  # uses today’s date
# or provide a specific date
import datetime
print(get_daily_quote(datetime.date(2023, 1, 1)))
```

## Testing
Run the tests with:
```bash
python -m unittest discover -s tests
```
All tests are deterministic and use mocks; no network required.
