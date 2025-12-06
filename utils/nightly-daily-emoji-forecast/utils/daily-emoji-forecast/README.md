# Daily Emoji Forecast

A whimsical utility that provides a deterministic emoji "forecast" for any given date. Perfect for adding a fun mood indicator to logs, commit messages, or daily stand‑ups.

## How it works

- The date (YYYY‑MM‑DD) is hashed with SHA‑256.
- The hash is converted to an integer and modulo‑ed by the number of available emojis.
- The resulting emoji is returned.

## Usage

```bash
python -m src.forecast          # forecast for today
python -m src.forecast 2023-10-31
```

## Available emojis

🌞 🌧️ 🌪️ 🌋 🌈 🌑 🔥 ❄️ 🌊 🌟

## Testing

Run the tests with:

```bash
python -m unittest discover -s tests
```
