# Nightly Mood Ring

A whimsical utility that maps the current hour to a mood emoji, providing a quick emotional snapshot of the day. Useful for adding a touch of personality to scripts, logs, or terminal prompts.

## Usage

```bash
python -m utils/nightly-mood-ring/src/mood_ring
# or, from the utility folder
python -m mood_ring
```

Running the module prints an emoji representing the mood for the current hour.

## API

```python
get_mood(dt: datetime | None = None) -> str
```

- **dt** – Optional `datetime` object. If omitted, the current system time is used.
- Returns the emoji that corresponds to the hour of the provided (or current) time.

## Mood Mapping

| Hour Range | Emoji |
|------------|-------|
| 00‑03      | 🌑   |
| 04‑07      | 🌅   |
| 08‑11      | ☀️   |
| 12‑15      | 😎   |
| 16‑19      | 🌆   |
| 20‑23      | 🌙   |

Feel free to embed the output in your scripts, CI logs, or daily stand‑up messages!
