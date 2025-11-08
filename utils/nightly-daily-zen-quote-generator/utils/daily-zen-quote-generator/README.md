# Daily Zen Quote Generator

## Overview
`daily-zen-quote-generator` is a self‑contained utility that prints a single, deterministic “Zen” quote for the current day. The quote is chosen from a built‑in list using the day’s ordinal number, so the output is repeatable and requires **no network access**.

## Features
- Zero external dependencies (standard library only).
- Deterministic output – the same date always yields the same quote.
- Simple CLI (`python -m src.quote_generator`).
- Fully tested with offline mocks.

## Installation
Copy the folder `utils/daily-zen-quote-generator/` into your repository and run the script directly. No additional installation steps are required.

## Usage
```bash
$ python -m src.quote_generator
The obstacle is the path.
```

You can also import the helper function in your own code:
```python
from src.quote_generator import get_today_quote
print(get_today_quote())
```

## Testing
Run the tests with the standard library `unittest` runner:
```bash
$ python -m unittest discover -s tests
```
All tests are deterministic and use mocks, so they work offline.
