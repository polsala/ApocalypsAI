# Nightly Emoji Forecast

**Utility name:** `nightly-emoji-forecast`

## What it does

`nightly-emoji-forecast` produces a short, deterministic *emoji* weather forecast for any given date. The forecast consists of three emojis selected from a curated list (sun, clouds, rain, thunder, snow, etc.). Because the selection is based on a SHA‑256 hash of the date, the same date always yields the same forecast – making it perfect for reproducible demos, CI‑friendly scripts, or just a daily dose of fun.

## Why it’s useful

* **Deterministic** – No external APIs, no network calls. The output is fully reproducible.
* **Zero dependencies** – Pure Python 3.11 standard library.
* **CLI & library** – Use it from the command line or import the `generate_forecast` function in your own code.

## Installation

Copy the `utils/nightly-emoji-forecast/` folder into your repository and run the tests to verify everything works:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt  # (no extra requirements)
python -m unittest discover -s utils/nightly-emoji-forecast/tests
```

## Usage

### CLI

```bash
python utils/nightly-emoji-forecast/src/forecast.py            # uses today’s date
python utils/nightly-emoji-forecast/src/forecast.py --date 2023-10-31
```

Typical output:

```
☀️ 🌤️ ⛅
```

### As a library

```python
from utils.nightly_emoji_forecast.src.forecast import generate_forecast
import datetime

forecast = generate_forecast(datetime.date.today())
print(f"Today's forecast: {' '.join(forecast)}")
```

## Testing

The utility ships with a small deterministic test‑suite located in `utils/nightly-emoji-forecast/tests/`. Run it with:

```bash
python -m unittest discover -s utils/nightly-emoji-forecast/tests
```

## License

MIT – see the top‑level `LICENSE` file.
