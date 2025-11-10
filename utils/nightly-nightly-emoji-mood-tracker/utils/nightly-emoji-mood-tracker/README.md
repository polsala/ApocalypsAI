# Emoji Mood Tracker

**Utility name:** `nightly-emoji-mood-tracker`

## What it does

Given an ISO‑format date (`YYYY‑MM‑DD`), the tool returns a single emoji that represents a *mood* for that day. The mapping is fully deterministic and requires no external services, making it safe to run offline.

## How it works

1. Strip the dashes from the date string and interpret the result as an integer (e.g., `2023-01-01` → `20230101`).
2. Determine the weekday (`Monday=0 … Sunday=6`).
3. Compute an index: `(date_int + weekday) % len(EMOJIS)`.
4. Return the emoji at that index from a fixed list.

Because the algorithm only uses the input date, the same date will always yield the same emoji.

## Installation & Usage

```bash
# Clone the repository (or copy the folder) and navigate into it
cd utils/nightly-emoji-mood-tracker

# Run the module directly
python -m src.emoji_mood_tracker 2025-12-31
# → 🤩
```

You can also import the function in your own Python code:

```python
from src.emoji_mood_tracker import get_mood
print(get_mood("2025-12-31"))
```

## Testing

```bash
python -m pytest tests
```

All tests are deterministic and run offline.

## License

MIT – see the root `LICENSE` file.
