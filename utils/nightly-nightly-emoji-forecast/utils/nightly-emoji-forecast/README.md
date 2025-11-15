# Nightly Emoji Forecast

## Overview

`nightly-emoji-forecast` generates a playful *emoji weather* string that changes deterministically with the day of the week. No external APIs are called – the mapping is hard‑coded, making the utility completely offline and suitable for CI pipelines, commit hooks, or just a daily smile.

## Usage

```bash
python -m utils.nightly-emoji-forecast.src.forecast
```

Running the module prints the emoji for *today*:

```
🌞
```

You can also import the helper function in your own Python code:

```python
from utils.nightly-emoji-forecast.src.forecast import get_emoji_forecast

print(get_emoji_forecast())               # today
print(get_emoji_forecast(date(2023, 1, 5)))  # specific date
```

## Mapping

| Day       | Emoji |
|-----------|-------|
| Monday    | 🌞    |
| Tuesday   | 🌤️   |
| Wednesday | 🌧️   |
| Thursday  | ⛈️   |
| Friday    | 🌈    |
| Saturday  | ❄️    |
| Sunday    | 🌙    |

## Testing

Run the test suite with:

```bash
python -m unittest discover -s utils/nightly-emoji-forecast/tests
```

All tests are deterministic and use mocks; no network access is required.
