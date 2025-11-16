# Emoji Forecast

A tiny utility that prints a whimsical weather forecast using emojis. It determines a deterministic pseudo‑random temperature based on the supplied date (or today) and maps it to an emoji representing the weather.

## Usage

```bash
python -m src.forecast 2023-10-31
# 🌤️ 15°C
```

If no date is provided, the utility uses the current date.

## How it works

1. The date is converted to its ordinal value.
2. A simple arithmetic formula produces a temperature in the range **‑10 °C … 40 °C**.
3. The temperature is mapped to an emoji:
   - ❄️  < 0 °C
   - ☁️  0‑9 °C
   - 🌤️ 10‑19 °C
   - ☀️ 20‑29 °C
   - 🔥 ≥ 30 °C

The algorithm is fully deterministic and requires no external services.
