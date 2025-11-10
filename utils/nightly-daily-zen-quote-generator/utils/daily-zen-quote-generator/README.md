# Daily Zen Quote Generator

A tiny, self‑contained utility that prints a *quote of the day*.

- **Whimsical**: each day you get a different piece of Zen wisdom.
- **Useful**: can be used in terminal prompts, daily‑email scripts, or chat‑bot replies.
- **Deterministic & Offline**: quotes are baked into the package; the selection is based on the current date, so no network calls are required.

## Usage
```bash
python -m daily_zen_quote_generator
```
Will output a single line with today’s quote.

## API
```python
from daily_zen_quote_generator import get_quote

# Get today's quote (or supply a custom date)
quote = get_quote()                     # uses datetime.date.today()
quote = get_quote(date=datetime.date(2023, 1, 1))
```

## Testing
Run the bundled tests with:
```bash
python -m unittest discover -s utils/daily-zen-quote-generator/tests
```
All tests are deterministic and require no external resources.
