# nightly‑emoji‑weather

A tiny, self‑contained utility that maps a calendar date to a weather‑emoji.

## Why?
* Add a splash of personality to daily reports, commit messages, or chat bots.
* Fully deterministic – the same date always yields the same emoji.
* Zero external dependencies; pure Python 3.11.

## How it works
The utility parses an ISO‑8601 date string (e.g. `2023-10-31`), converts it to a `datetime.date`, and uses the date’s ordinal value (`date.toordinal()`) modulo the size of an internal emoji list. The resulting emoji is returned.

## Usage
```bash
# As a module
python -m utils.nightly-emoji-weather.src.weather 2023-10-31
# Output: 🌧️

# As a library
>>> from utils.nightly-emoji-weather.src.weather import get_weather_emoji
>>> get_weather_emoji('2023-10-31')
'🌧️'
```

## Development
Run the test suite with:
```bash
python -m unittest discover -s utils/nightly-emoji-weather/tests
```
