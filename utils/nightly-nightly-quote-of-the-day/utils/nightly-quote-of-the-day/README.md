# Nightly Quote of the Day

Utility that returns a deterministic "quote of the day" based on the day of the year. No network calls; self‑contained list of quotes. Useful for adding a daily inspirational line to scripts, CI logs, or README banners.

## Usage

```bash
python -m src.quote_of_the_day
```

Will print today's quote.

Or import `get_quote` from `src.quote_of_the_day`:

```python
from src.quote_of_the_day import get_quote
print(get_quote())
```
