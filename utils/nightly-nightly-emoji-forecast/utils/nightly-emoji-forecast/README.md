# Nightly Emoji Forecast

**What it does**

`emoji-forecast` is a self‑contained Python utility that produces a deterministic "weather" emoji for any given date. The algorithm is deliberately simple – it adds the year, month, and day numbers together and uses the result modulo the number of available emojis. This makes the output repeatable without any external data or network calls.

**Why it’s useful**

- Add a splash of personality to daily CI logs, Slack messages, or commit messages.
- Perfect for bots that need a lightweight, offline source of daily fun.
- No dependencies beyond the Python standard library.

**Usage**

```bash
python -m emoji_forecast          # prints today’s emoji
python -m emoji_forecast 2023-07-04  # prints the emoji for the supplied date
```

**API**

```python
from datetime import date
from emoji_forecast import get_forecast

today_emoji = get_forecast(date.today())
```

**Testing**

Run the bundled tests with:

```bash
python -m unittest discover -s utils/nightly-emoji-forecast/tests
```
