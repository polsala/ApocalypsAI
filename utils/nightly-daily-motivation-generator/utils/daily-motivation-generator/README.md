# Daily Motivation Generator

A whimsical yet useful utility that provides a deterministic motivational quote for any given date.

## Features
- **Deterministic**: The same date always yields the same quote (no external network calls).
- **Zero dependencies**: Pure Python 3.11 standard library.
- **CLI & library usage**:
  ```bash
  python -m daily_motivation_generator          # prints today's quote
  python -m daily_motivation_generator 2025-01-01  # prints quote for a specific date
  ```

## Installation
Simply copy the `utils/daily-motivation-generator` folder into your project and import:
```python
from daily_motivation_generator import get_motivation
``` 

## API
```python
get_motivation(date: datetime.date | None = None) -> str
```
Returns a motivational quote for the supplied date (or today if `None`).

## Testing
Run the bundled tests with:
```bash
python -m unittest discover -s utils/daily-motivation-generator/tests
```
