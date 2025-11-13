# Emoji Forecast

`emoji-forecast` is a tiny, self‑contained utility that prints a whimsical weather forecast using emojis for any given city.

## Features

* Deterministic output – the same city always yields the same emoji sequence.
* No external API calls – works completely offline.
* Simple CLI: `python -m emoji_forecast src/forecast.py <city>`.
* Adjustable number of forecast days.

## Usage

```sh
python -m emoji_forecast src/forecast.py "San Francisco" -d 5
```

## How it works

The utility hashes the lower‑cased city name with SHA‑256, then maps the resulting integer to a rotating list of weather emojis.

## Testing

Run the bundled tests with:

```sh
python -m unittest discover -s utils/emoji-forecast/tests
```
