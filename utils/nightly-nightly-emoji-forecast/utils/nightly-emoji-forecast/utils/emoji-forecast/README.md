# Emoji Forecast

`emoji-forecast` turns a simple weather JSON payload into a whimsical emoji summary for the day.

## Features
- **Pure Python 3.11** – no external services required.
- **CLI**: `python -m emoji_forecast` prints a one‑line emoji forecast.
- **Library function**: `get_forecast(data: dict) -> str` for programmatic use.
- **Deterministic tests** using `unittest.mock` (no network).

## Example
```json
{
  "temperature_c": 22,
  "condition": "clear",
  "precipitation_mm": 0
}
```

Running the CLI with the above data prints:
```
🌞 22°C – Clear skies
```
