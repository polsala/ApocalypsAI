# Nightly Zen Quote of the Day

Provides a deterministic Zen quote for any given date. Useful for daily inspiration in scripts, CI logs, or terminal banners.

## Features

- `get_quote(date: datetime.date) -> str` returns a quote based on the day of year.
- CLI: `python -m src.quote` prints today's quote.
- No external dependencies.

## Usage

```bash
python -m src.quote
# or in code
from src.quote import get_quote
print(get_quote(date.today()))
```

## Testing

Run `pytest -q` in the utility folder.
