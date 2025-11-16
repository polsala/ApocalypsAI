# Nightly Emoji Forecast

## Overview

`nightly-emoji-forecast` is a tiny, self‑contained Python utility that produces a **deterministic** emoji “weather” forecast for any given date. The forecast is based on a pseudo‑random selection seeded by the ISO‑format date string, ensuring that the same date always yields the same emoji sequence.

## Why?

* **Whimsy** – adds a playful touch to daily stand‑ups, project boards, or GitHub README badges.
* **Deterministic** – no external API calls; the output is reproducible and offline.
* **Zero dependencies** – pure Python 3.11 standard library.

## Usage

```bash
python -m nightly_emoji_forecast <YYYY-MM-DD>
```

Or programmatically:

```python
from nightly_emoji_forecast import get_emoji_forecast
forecast = get_emoji_forecast(date(2025, 11, 16))
print(forecast)  # e.g. "☀️ 🌈"
```

## Implementation Details

* A fixed list of 12 emojis representing various “weather” conditions.
* The date string is hashed with SHA‑256, the digest is turned into an integer, and the integer is used to pick 2 emojis (primary and secondary) via modulo arithmetic.
* The utility ships with a tiny CLI wrapper and a comprehensive test suite.

## License

MIT – see the repository LICENSE file.
