# Daily Haiku Generator

A tiny, self‑contained utility that produces a three‑line haiku (5‑7‑5 syllable pattern) based on the current date or any supplied date.

## Features
- Deterministic output: the same date always yields the same haiku.
- No external dependencies – pure Python 3.11.
- Simple CLI (`python -m src.haiku`) prints today’s haiku.
- Library function `generate(date: datetime.date | None) -> str` for programmatic use.

## Usage
```bash
# Print today's haiku
python -m src.haiku
```
```python
from src.haiku import generate
import datetime

print(generate(datetime.date(2023, 1, 1)))
```

## Testing
Run the bundled tests with:
```bash
python -m unittest discover -s tests
```
