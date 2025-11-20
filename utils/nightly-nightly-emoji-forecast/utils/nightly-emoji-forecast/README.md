# Nightly Emoji Forecast

## Overview
`nightly-emoji-forecast` produces a three‑emoji “weather” forecast for any given date. The forecast is **deterministic** – it depends only on the calendar date – so the same date always yields the same emojis. This makes the utility completely offline and perfect for unit testing.

## How it works
1. The utility defines a small palette of weather‑related emojis.
2. For a supplied `YYYY‑MM‑DD` (or today if omitted) it calculates the day‑of‑year.
3. Using simple modular arithmetic it picks three emojis from the palette.
4. The three emojis are concatenated and printed.

## Usage
```bash
# Run as a module
python -m src.forecast            # uses today’s date
python -m src.forecast 2023-01-01  # explicit date
```

## Expected output
Running the example above yields:
```
🌤️☁️❄️
```

## Testing
The utility ships with a tiny test suite under `tests/` that verifies the forecast for known dates.

---
*Created by the ApocalypsAI Nightly Integrator*
