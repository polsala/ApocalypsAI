# Nightly Emoji Mood Meter

Utility that translates the current hour into a whimsical emoji representing the typical mood of that time. Useful for adding a touch of personality to logs, bots, or status messages.

## Usage

```python
from mood_meter import get_mood

print(get_mood())        # Uses the local system time
print(get_mood(14))      # Explicit hour (0‑23)
```

## Mood Mapping

| Hour(s) | Emoji | Description |
|---------|-------|-------------|
| 0‑5     | 🌙    | Late night / dreaming |
| 6‑9     | 🌅    | Sunrise optimism |
| 10‑12   | ☕    | Coffee break |
| 13‑17   | 💼    | Work hustle |
| 18‑20   | 🌆    | Evening unwind |
| 21‑23   | 🌙    | Nightfall chill |
