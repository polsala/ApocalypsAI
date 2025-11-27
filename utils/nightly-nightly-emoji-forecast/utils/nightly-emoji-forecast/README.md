# Nightly Emoji Forecast

## What it does
`emoji-forecast` turns any calendar date into a short, deterministic weather forecast made of emojis. The forecast is **purely whimsical** – it does not query any external API, making it fast, offline, and completely reproducible.

## Why it’s useful
- **Team morale** – sprinkle a daily emoji forecast into stand‑up notes or PR comments.
- **Automation friendly** – can be called from CI pipelines to generate a fun badge.
- **Zero dependencies** – pure Python standard library, no network calls.

## Installation
```bash
# From the repository root
python -m venv .venv && source .venv/bin/activate
pip install -e utils/nightly-emoji-forecast
```

## Usage
```bash
# Get today’s forecast
python -m nightly_emoji_forecast.src.forecast

# Get forecast for a specific date (YYYY‑MM‑DD)
python -m nightly_emoji_forecast.src.forecast 2025-12-31
```

## Output example
```
🌤️ 🌦️ 🌈
```

## How it works
1. The date string (`YYYY‑MM‑DD`) is hashed using Python’s built‑in `hash()` (stabilized by `hashlib.sha256`).
2. The hash is turned into a deterministic seed.
3. A small pool of weather‑related emojis is shuffled with that seed.
4. The first three emojis are joined and returned.

Because the algorithm is deterministic, the same date always yields the same forecast – ideal for testing.

## Testing
Run the bundled tests with:
```bash
pytest utils/nightly-emoji-forecast/tests
```
