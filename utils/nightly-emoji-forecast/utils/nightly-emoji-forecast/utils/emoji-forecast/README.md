# Emoji Forecast

A tiny, self‑contained utility that returns an emoji representation of the weather for a given date. It uses a simple deterministic algorithm (day‑of‑year modulo a short cycle) so it works completely offline.

## Usage
```bash
python -m emoji_forecast <YYYY-MM-DD>
```
Example:
```bash
$ python -m emoji_forecast 2023-04-01
☀️
```

## How it works
- The utility defines a four‑item cycle: `☀️` (sun), `⛅` (partly cloudy), `🌧️` (rain), `❄️` (snow).
- The day of the year (`1`‑`366`) is taken modulo `4` to pick an emoji from the cycle.
- Because the algorithm is pure math, the same date always yields the same emoji.

## Files
- `src/forecast.py` – core implementation and CLI entry point.
- `tests/test_forecast.py` – deterministic unit tests.
