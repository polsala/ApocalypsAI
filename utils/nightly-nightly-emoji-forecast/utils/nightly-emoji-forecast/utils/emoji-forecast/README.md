# Nightly Emoji Forecast

A whimsical yet handy utility that turns a simple weather description into emojis.
Perfect for adding a splash of fun to daily stand‑ups, Slack messages, or commit messages.

## How it works

`get_emoji_forecast(date: str, location: str) -> str`

* Parses the date (YYYY‑MM‑DD).
* Calls a deterministic mock weather provider.
* Maps the weather description to an emoji.

## CLI

```bash
python -m utils.nightly_emoji_forecast.src.emoji_forecast 2023-10-31 "New York"
```

Outputs an emoji such as `☀️` or `🌧️`.

## Testing

Run the bundled tests with:

```bash
python -m unittest discover -s utils/nightly-emoji-forecast/utils/emoji-forecast/tests
```
