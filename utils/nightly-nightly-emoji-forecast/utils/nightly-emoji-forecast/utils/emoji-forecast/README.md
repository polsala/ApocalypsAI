# Emoji Forecast

Generate a whimsical emoji weather forecast for a given date. No network calls; uses deterministic pseudo‑random based on the date.

## Usage

```bash
python -m emoji_forecast src/forecast.py [YYYY-MM-DD]
```

If no date is provided, the utility uses today’s date.

## Output

A short sentence like:

```
🌞 Sunny with a chance of 🌧️ Rainy.
```

## Tests

Run the test suite with:

```bash
pytest
```

The utility is self‑contained and requires only the Python 3.11 standard library.
