# Nightly Emoji Mood Indicator

A tiny, self‑contained Python utility that converts a numeric mood score (1‑5) into a single emoji. Perfect for adding a splash of personality to commit messages, Slack updates, or any place you want to convey a quick emotional snapshot.

## Usage

```bash
python -m src.mood <score>
```

- `<score>` must be an integer between **1** (very sad) and **5** (very happy).
- The script prints the corresponding emoji to stdout.

### Example

```bash
$ python -m src.mood 4
🙂
```

## API

```python
from src.mood import get_mood_emoji

emoji = get_mood_emoji(3)  # returns "😐"
```

- `get_mood_emoji(score: int) -> str`
- Raises `ValueError` if `score` is not in the range 1‑5.

## Mapping Table

| Score | Emoji | Meaning |
|------|-------|---------|
| 1 | 😞 | Very sad |
| 2 | ☹️ | Sad |
| 3 | 😐 | Neutral |
| 4 | 🙂 | Happy |
| 5 | 😁 | Very happy |

## Testing

Run the bundled unit tests with:

```bash
python -m unittest discover -s tests
```

All tests are deterministic and require no external resources.
