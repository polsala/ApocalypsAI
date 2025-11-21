# Nightly Emoji Forecast

`nightly-emoji-forecast` is a playful utility that translates the current temperature of a city into an emoji representation.  It demonstrates:

* **Self‑contained Python code** – no external services are required at test time.
* **Deterministic offline tests** – the HTTP request to a (fictional) weather API is mocked.
* **A whimsical yet useful idea** – quickly get a visual cue of the weather.

## Installation

The utility is pure Python 3.11 and only depends on the standard library plus `requests` (already allowed in the repo).

```bash
pip install requests
```

## Usage

```bash
python -m utils.nightly-emoji-forecast.src.forecast "London"
```

Output example:

```
Weather in London: 🌤️
```

## How it works

1. `forecast.py` contacts a placeholder weather endpoint (`https://api.example.com/weather`).
2. The JSON response is expected to contain a `temperature_c` field.
3. The temperature is mapped to an emoji:
   * `< 0°C` → 🥶
   * `0‑9°C` → 🧣
   * `10‑19°C` → 🌤️
   * `20‑29°C` → ☀️
   * `≥ 30°C` → 🔥

## Testing

Run the bundled tests with:

```bash
python -m unittest discover utils/nightly-emoji-forecast/tests
```

The tests mock the HTTP request, guaranteeing deterministic results.
