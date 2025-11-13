# Daily Zen Quote Generator

A whimsical yet practical utility that prints a Zen‑inspired quote based on the current day. The selection is **deterministic** – the same calendar day always yields the same quote, making it perfect for:

- Adding a calming line to your terminal prompt or shell startup script.
- Including a daily quote in automated emails or reports.
- Any situation where a predictable, lightweight “quote of the day” is handy.

## How it works

The script contains a short static list of Zen quotes. It computes the day‑of‑year (1‑365) for the target date and selects a quote using:

```python
index = (day_of_year - 1) % len(quotes)
```

Thus the mapping repeats every *len(quotes)* days.

## Usage

```bash
# Run the utility (prints today’s quote)
python -m daily_zen_quote_generator
```

Or invoke the module directly:

```bash
python utils/daily-zen-quote-generator/src/main.py
```

You can also request a quote for a specific date programmatically:

```python
from src.main import get_quote
import datetime
print(get_quote(datetime.date(2023, 1, 1)))
```

## Testing

The utility ships with deterministic, offline tests. Run them with:

```bash
cd utils/daily-zen-quote-generator
pytest
```

---

*No external network calls are made; all data is bundled with the utility.*
