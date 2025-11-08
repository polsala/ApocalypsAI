# Daily Zen Quote Generator

A lightweight, zero‑dependency Python utility that produces a deterministic Zen‑style quote for a given date.

## Features
- **Deterministic**: The same date always yields the same quote.
- **Offline**: No network calls; quotes are baked into the source.
- **CLI & Library**: Use it from the command line or import the `get_quote` function.

## Installation
Simply copy the `utils/daily-zen-quote-generator` folder into your project and run the script with Python 3.11+.

```bash
python -m utils.daily-zen-quote-generator.src.main [YYYY-MM-DD]
```
If no date is supplied, today's date is used.

## Example
```bash
$ python -m utils.daily-zen-quote-generator.src.main 2023-01-01
"The journey of a thousand miles begins with a single step."
```

## API
```python
from utils.daily-zen-quote-generator.src.main import get_quote
import datetime

quote = get_quote(datetime.date(2023, 1, 1))
```

## Testing
Run the bundled tests with:
```bash
python -m unittest discover utils/daily-zen-quote-generator/tests
```
All tests are deterministic and require no external resources.
