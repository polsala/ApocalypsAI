# Nightly Emoji Forecast

A tiny utility that converts a temperature (°C) into a whimsical emoji representing the weather. Perfect for adding a splash of fun to logs, chat messages, or commit comments.

## Usage

```bash
python -m src.forecast 23
# ☀️
```

Or import the function:

```python
from src.forecast import get_emoji_forecast
print(get_emoji_forecast(5))  # 🌨️
```

## Mapping

- ≤ 0 °C → 🥶
- 1‑10 °C → 🌨️
- 11‑20 °C → 🌤️
- 21‑30 °C → ☀️
- > 30 °C → 🔥

## Tests

Run with `pytest`:

```bash
pytest -q
```
