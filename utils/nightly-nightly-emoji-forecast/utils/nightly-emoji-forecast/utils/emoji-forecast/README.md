# Emoji Forecast

`emoji-forecast` is a lightweight Python utility that provides a deterministic emoji‑based weather forecast for a given date.

## Features

- No external API calls – completely offline.
- Deterministic output: the same date always yields the same emoji.
- Simple CLI: `python -m forecast <YYYY-MM-DD>`.
- Small footprint, pure standard library.

## Usage

```bash
python -m forecast 2025-12-01
# 🌤️
```

## How it works

The utility hashes the ISO‑format date string, maps the resulting integer to one of five emojis:

- 🌞 (sunny)
- 🌤️ (partly sunny)
- 🌥️ (cloudy)
- 🌧️ (rainy)
- ❄️ (snowy)

The mapping is deterministic and requires no network access.

## License

MIT © ApocalypsAI
