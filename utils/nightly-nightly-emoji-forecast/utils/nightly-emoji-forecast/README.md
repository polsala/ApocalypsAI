# Nightly Emoji Forecast

A tiny utility that gives you a whimsical weather forecast expressed as an emoji, based solely on the name of a location. No external APIs, fully deterministic, and perfect for adding a splash of fun to your scripts or CI logs.

## How it works

- The location string is hashed with SHA‑256.
- The hash is converted to an integer and reduced modulo the number of supported weather emojis.
- The resulting emoji is printed.

## Usage

```sh
python -m src.forecast "San Francisco"
# Weather forecast for San Francisco: 🌧️
```

## Supported emojis

| Index | Emoji | Meaning |
|------|-------|---------|
| 0 | ☀️ | Sunny |
| 1 | ⛅ | Partly cloudy |
| 2 | ☁️ | Cloudy |
| 3 | 🌧️ | Rain |
| 4 | ⛈️ | Thunderstorm |
| 5 | ❄️ | Snow |
| 6 | 🌫️ | Fog |

## Testing

Run the test suite with:

```sh
python -m unittest discover -s tests
```

The tests mock the hashing function to guarantee deterministic results.
