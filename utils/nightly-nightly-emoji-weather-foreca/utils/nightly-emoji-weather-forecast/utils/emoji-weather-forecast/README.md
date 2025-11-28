# Emoji Weather Forecast

A tiny, self‑contained Python utility that returns a weather emoji for a supplied date. The forecast is **deterministic** – the same date always yields the same emoji – and requires no network access.

## Features
- No external dependencies beyond the Python standard library.
- Deterministic output based on the date (perfect for reproducible tests).
- Simple CLI for quick ad‑hoc use.

## Usage
```python
from datetime import date
from src.forecast import get_forecast

print(get_forecast(date.today()))  # e.g. "☀️"
```

Or from the command line:
```bash
python -m src.forecast 2025-12-25
# Output: 🌧️
```

## Emoji Mapping
| Index | Emoji | Meaning |
|-------|-------|---------|
| 0 | ☀️ | Sunny |
| 1 | 🌤️ | Partly Cloudy |
| 2 | 🌧️ | Rain |
| 3 | ⛈️ | Thunderstorm |

The index is derived from `date.toordinal() % 4`.

## Testing
Run the bundled tests with:
```bash
pytest -q
```
All tests are deterministic and run offline.
