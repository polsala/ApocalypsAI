# Nightly Emoji Forecast

A tiny, self‑contained Python utility that produces a playful, emoji‑based weather forecast for any ISO‑format date range.

## Features
- **Deterministic** – the same start date always yields the same sequence of emojis (uses a seeded PRNG).
- **Zero external dependencies** – only the Python standard library.
- **Simple API** – `generate_forecast(start_date: str, end_date: str) -> List[str]`.

## Example
```python
from forecast import generate_forecast

forecast = generate_forecast("2023-09-01", "2023-09-05")
for line in forecast:
    print(line)
```
Possible output:
```
2023-09-01: 🌤️
2023-09-02: 🌧️
2023-09-03: ☀️
2023-09-04: 🌈
2023-09-05: 🌨️
```

## Running the tests
```bash
python -m unittest discover -s utils/nightly-emoji-forecast/tests
```
