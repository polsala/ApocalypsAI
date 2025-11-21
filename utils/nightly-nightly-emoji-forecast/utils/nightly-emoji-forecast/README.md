# Nightly Emoji Forecast

**What it does**

`nightly-emoji-forecast` maps any calendar date to a weather‑style emoji in a completely deterministic way. No external APIs, no network calls – just pure Python.

**Why it’s useful**

- Add a splash of personality to daily CI logs or commit messages.
- Perfect for bots that need a lightweight “weather” indicator without pulling real data.
- Completely offline and deterministic, making it safe for the ApocalypsAI sandbox.

**How to use**

```bash
# Run the CLI (prints today’s forecast)
python -m utils.nightly-emoji-forecast.src.forecast

# Or import in your own code
from utils.nightly-emoji-forecast.src.forecast import get_emoji_forecast
import datetime
print(get_emoji_forecast(datetime.date.today()))
```

**Supported emojis**

| Index | Emoji |
|------|-------|
| 0 | ☀️ |
| 1 | 🌤️ |
| 2 | ⛅ |
| 3 | 🌥️ |
| 4 | ☁️ |
| 5 | 🌦️ |
| 6 | 🌧️ |
| 7 | ⛈️ |
| 8 | 🌩️ |
| 9 | ❄️ |
|10 | 🌨️ |
|11 | 🌪️ |

The mapping is `day_of_year % 12`.
