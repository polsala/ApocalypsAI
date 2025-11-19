# Nightly Emoji Forecast

Generate a whimsical weather forecast represented by emojis for any given date.

## Usage

```bash
python -m src.emoji_forecast 2025-12-31
# Output: 🌤️
```

The forecast is deterministic: the same date always yields the same emoji.

## How it works

The utility hashes the input date and maps it to one of several weather emojis.

## Testing

Run tests with:

```bash
python -m unittest discover -s tests
```
