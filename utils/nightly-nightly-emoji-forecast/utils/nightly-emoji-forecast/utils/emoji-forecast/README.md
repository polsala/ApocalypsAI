# Emoji Forecast

A tiny utility that generates a deterministic, whimsical weather‑style forecast using emojis for any given date. Perfect for adding a splash of fun to CI logs, commit messages, or daily stand‑ups.

## Usage

```bash
python -m emoji_forecast.src.forecast [--date YYYY-MM-DD]
```

If `--date` is omitted, today’s date is used.

## How it works

The forecast is generated from a fixed list of emojis. The selection is seeded by the ISO ordinal of the date, ensuring the same date always yields the same forecast without any network calls.

## Testing

Run the tests with:

```bash
python -m unittest discover -s utils/nightly-emoji-forecast/utils/emoji-forecast/tests
```
