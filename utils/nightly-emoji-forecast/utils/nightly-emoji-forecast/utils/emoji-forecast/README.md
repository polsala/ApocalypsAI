# Emoji Forecast

A tiny utility that converts plain‑language weather descriptions into a concise emoji string. Useful for Slack/status messages, commit messages, or any place you want a quick visual weather cue.

## Installation

Just copy the folder; no external dependencies beyond the Python standard library.

## Usage

```bash
python -m emoji_forecast "light rain"
# 🌧️
```

Or import:

```python
from emoji_forecast import forecast
print(forecast("sunny"))
```

## Mapping

| Weather description | Emoji |
|---------------------|-------|
| sunny               | ☀️    |
| clear               | ☀️    |
| partly cloudy       | 🌤️   |
| cloudy              | ☁️    |
| overcast            | ☁️    |
| light rain          | 🌧️   |
| rain                | 🌧️   |
| heavy rain          | 🌧️   |
| thunderstorm        | ⛈️   |
| snow                | ❄️    |
| fog                 | 🌫️   |
| windy               | 🌬️   |
| unknown             | ❓    |

The utility normalises input to lower‑case and matches the longest known key.
