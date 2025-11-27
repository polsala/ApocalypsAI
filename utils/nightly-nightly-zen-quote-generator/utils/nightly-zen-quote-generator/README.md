# Nightly Zen Quote Generator

A whimsical yet useful utility that prints a deterministic "Zen" quote for the current day (or any given date). Perfect for sprinkling a bit of calm into your terminal or CI logs.

## Features

- **Deterministic**: The same date always yields the same quote.
- **Zero external dependencies** – pure Python 3.11 standard library.
- **CLI**: `python -m zen` prints today’s quote.
- **Library**: Import `get_zen_quote` for programmatic use.

## Usage

```bash
# As a script (prints today’s quote)
python -m zen

# As a module (specify a date)
python - <<PY
from zen import get_zen_quote
import datetime
print(get_zen_quote(datetime.date(2023, 1, 1)))
PY
```

## Implementation Details

The utility stores a static list of ~20 Zen‑style sayings. It seeds a `random.Random` instance with the numeric representation of the date (`YYYYMMDD`) and selects a quote via `choice`. This guarantees reproducibility without persisting any state.

## Testing

Run the tests with:

```bash
python -m unittest discover -s tests
```
