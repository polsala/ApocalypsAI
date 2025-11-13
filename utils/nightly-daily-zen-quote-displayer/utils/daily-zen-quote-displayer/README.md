# Daily Zen Quote Displayer

A tiny, self‑contained utility that prints a Zen‑inspired quote for the current day. The selection is **deterministic** – the same date (and optional theme) always yields the same quote, making it perfect for scripts, CI messages, or a daily splash screen.

## Features
- No external dependencies or network calls.
- Optional theme filtering (case‑insensitive).
- Fully test‑covered with offline deterministic tests.

## Usage
```bash
# From the repository root
python -m utils.daily-zen-quote-displayer.src.quote
# With a theme
python -m utils.daily-zen-quote-displayer.src.quote --theme silence
```

## API
```python
from utils.daily-zen-quote-displayer.src.quote import get_quote

# Get today's quote
quote = get_quote()

# Get a themed quote for a specific date
import datetime
quote = get_quote(date=datetime.date(2023, 1, 1), theme="silence")
```

## Testing
Run the bundled tests with `pytest`:
```bash
pytest utils/daily-zen-quote-displayer/tests
```
