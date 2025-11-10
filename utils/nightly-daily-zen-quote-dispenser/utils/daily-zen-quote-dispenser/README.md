# Daily Zen Quote Dispenser

Utility that prints a random Zen‑inspired quote. Useful for adding a touch of calm to scripts, commit messages, or terminal sessions.

## Usage

```bash
python -m utils.daily_zen_quote_dispenser.src.quote
```

Or import:

```python
from utils.daily_zen_quote_dispenser.src.quote import get_zen_quote
print(get_zen_quote())
```

## Features

- Built‑in list of 10+ Zen quotes.
- Optional `max_length` filter.
- No external dependencies.

## Testing

Run:

```bash
python -m unittest discover utils/daily-zen-quote-dispenser/tests
```
