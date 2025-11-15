# Nightly Emoji Forecast

`emoji-forecast` is a tiny, self‑contained Python utility that generates a deterministic "weather" forecast expressed entirely in emojis. The forecast is based on the supplied date (or today if omitted) and is reproducible – the same date always yields the same emoji sequence.

## Features
- Zero external dependencies (only the Python standard library).
- Provides a library function `get_emoji_forecast(date: datetime.date) -> str`.
- Offers a convenient CLI: `python -m emoji_forecast [--date YYYY-MM-DD]`.
- Fully unit‑tested with offline, deterministic expectations.

## Usage
```bash
# As a module
python - <<PY
from src.forecast import get_emoji_forecast
import datetime
print(get_emoji_forecast(datetime.date.today()))
PY

# As a CLI
python -m src.forecast            # forecast for today
python -m src.forecast --date 2023-01-01
```

## How it works
The utility hashes the ISO‑formatted date string, reduces the hash to an index, and selects an emoji from a fixed list of ten weather symbols. Because the algorithm is pure and deterministic, the same input always yields the same output – perfect for reproducible tests.
