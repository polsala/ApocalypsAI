# Nightly Emoji Mood Meter

`nightly-emoji-mood-meter` is a tiny, self‑contained Python utility that maps any calendar date to a single emoji representing the "mood" of that day. The mapping is **deterministic** – the same date always yields the same emoji – and requires no external data or network access.

## Features

- Pure Python 3.11, no third‑party dependencies.
- Simple API: `get_mood_emoji(date: datetime.date) -> str`.
- Command‑line interface that prints today’s emoji.
- Fully tested with offline, deterministic unit tests.

## Installation & Usage

```bash
# Clone the repository (or copy the folder) and run the script directly
python -m utils.nightly-emoji-mood-meter.src.emoji_mood
```

Or import it in your own code:

```python
from utils.nightly-emoji-mood-meter.src.emoji_mood import get_mood_emoji
import datetime

print(get_mood_emoji(datetime.date.today()))
```

## How It Works

The utility computes the day‑of‑year (1‑365/366) for the supplied date, then uses a modulo operation against a curated list of 12 emojis that loosely follow a sunrise‑to‑sunset emotional arc. Because the algorithm is purely arithmetic, it works offline and is completely reproducible.

## Testing

Run the tests with the standard library:

```bash
python -m unittest discover utils/nightly-emoji-mood-meter/tests
```

---

*Created by the ApocalypsAI Nightly Integrator.*
