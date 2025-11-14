# Daily Zen Quote Dispenser

Utility that prints a random Zen‑inspired quote. Great for sprinkling a bit of calm into scripts, CI pipelines, or just for personal enjoyment.

## Features

- Returns a random quote from a curated list.
- Optional `--max-length` filter to limit quote size.
- Fully self‑contained Python 3.11 module.
- Deterministic offline tests using mocks.

## Installation

Copy the `utils/daily-zen-quote-dispenser` folder into your repository and run the script directly:

```bash
python -m daily_zen_quote_dispenser.src.quote
```

Or import the function in your own code:

```python
from daily_zen_quote_dispenser.src.quote import get_zen_quote

print(get_zen_quote())
```

## CLI Usage

```bash
python -m daily_zen_quote_dispenser.src.quote [--max-length N]
```

- `--max-length N` – only consider quotes with `len(quote) <= N`.

## Testing

Run the bundled tests with:

```bash
python -m unittest discover -s utils/daily-zen-quote-dispenser/tests
```
