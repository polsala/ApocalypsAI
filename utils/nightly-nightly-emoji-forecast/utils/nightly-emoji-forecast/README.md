# Nightly Emoji Forecast

A tiny, self‑contained Python utility that turns a calendar date into a playful weather forecast expressed entirely in emojis.

## Features

- **Zero external dependencies** – pure Python standard library.
- **Deterministic** – the same date always yields the same emoji, making testing trivial.
- **CLI friendly** – run `python -m nightly-emoji-forecast <YYYY-MM-DD>` to get an instant forecast.

## Usage

```bash
# As a module
python -m nightly-emoji-forecast 2025-04-01
# Or import in your own code
from nightly_emoji_forecast.src.forecast import get_emoji_forecast
print(get_emoji_forecast(date(2025, 4, 1)))
```

## How it works

The utility maps the day‑of‑year (1‑366) to a short list of weather emojis using a simple modulo operation. This ensures:

1. **Predictability** – no network calls, no randomness.
2. **Fun** – a different emoji each day, cycling through a curated set.

## License

MIT – see the repository root LICENSE file.
