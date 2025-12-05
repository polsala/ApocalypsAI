# Emoji Mood Analyzer

**Utility name:** `emoji-mood-analyzer`

## What it does
`emoji-mood-analyzer` scans a short piece of text and returns a single emoji that best represents the overall mood. It uses a lightweight keyword‑based approach, making it completely offline and deterministic.

## How it works
| Mood | Keywords (case‑insensitive) | Emoji |
|------|----------------------------|-------|
| Happy | `happy`, `joy`, `glad`, `awesome`, `great`, `fantastic` | 😊 |
| Sad | `sad`, `unhappy`, `down`, `depressed`, `blue` | 😢 |
| Angry | `angry`, `mad`, `furious`, `irate`, `annoyed` | 😠 |
| Surprised | `surprised`, `shocked`, `amazed`, `wow` | 😲 |
| Default | *(no match)* | 🤔 |

The first matching keyword determines the emoji. If multiple moods match, the order above defines priority.

## Installation & Usage
The utility is self‑contained; just copy the folder into your repository.

```bash
# Run as a module
python -m emoji_mood_analyzer "I am feeling fantastic today!"
# => 😊
```

Or import it in your own Python code:

```python
from emoji_mood_analyzer.src.mood_analyzer import analyze_mood

print(analyze_mood("I'm a bit down today."))  # 😢
```

## Testing
Run the bundled tests with:

```bash
python -m unittest discover -s utils/nightly-emoji-mood-analyzer/utils/emoji-mood-analyzer/tests
```

All tests are deterministic and require no network access.
