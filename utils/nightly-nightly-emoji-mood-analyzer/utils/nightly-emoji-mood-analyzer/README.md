# Nightly Emoji Mood Analyzer

**Utility name:** `nightly-emoji-mood-analyzer`

## What it does

Scans a string (or a file) for a set of known emojis and returns the *dominant* mood:

- 😄, 😊, 😁 → **happy**
- 😢, 😞, 😔 → **sad**
- 😡, 🤬, 😠 → **angry**
- If none of the above appear, the mood is **neutral**.

The tool is deliberately lightweight and has **no external dependencies** beyond the Python standard library.

## Installation & usage

```bash
# Clone the repo (or copy the folder) and run the script directly
python -m utils.nightly-emoji-mood-analyzer.src.emoji_mood_analyzer "Your text here"
```

Or, if you have a file:

```bash
python -m utils.nightly-emoji-mood-analyzer.src.emoji_mood_analyzer --file path/to/file.txt
```

## API

```python
from utils.nightly-emoji-mood-analyzer.src.emoji_mood_analyzer import analyze_mood

mood = analyze_mood("I am so happy 😄😄!")  # -> "happy"
```

## Testing

```bash
pytest utils/nightly-emoji-mood-analyzer/tests
```

All tests are deterministic and run offline.
