# Emoji Forecast

`emoji-forecast` is a tiny Python utility that converts simple weather descriptions into a string of emojis representing the day's outlook.

## Features
- Pure Python 3.11, no external dependencies.
- Deterministic output for given input data.
- Includes a CLI (`python -m emoji_forecast`) that prints a one‑line emoji forecast.
- Fully unit‑tested with offline mocks.

## Usage
```bash
# Run with default mock data
python -m emoji_forecast

# Provide your own JSON file
python -m emoji_forecast path/to/weather.json
```

The input JSON should have the shape:
```json
{ "condition": "clear" }
```
Supported conditions: `clear`, `cloudy`, `rain`, `snow`, `storm`, `fog`.

## License
MIT © ApocalypsAI
