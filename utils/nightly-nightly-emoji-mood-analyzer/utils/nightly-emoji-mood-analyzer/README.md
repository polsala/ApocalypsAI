# Nightly Emoji Mood Analyzer

**Utility name:** `nightly-emoji-mood-analyzer`

## What it does

Scans an input string for Unicode emojis and returns a simple mood classification:

- **happy** – the text contains more positive emojis than negative ones.
- **sad** – the text contains more negative emojis than positive ones.
- **neutral** – the counts are equal or no emojis are found.

The sentiment mapping is tiny and self‑contained, making the tool completely offline and deterministic.

## Usage

```bash
python -m utils.nightly-emoji-mood-analyzer.src.emoji_analyzer "I love 🍕 and 🎉!"
# → happy
```

Or import it in your own Python code:

```python
from utils.nightly-emoji-mood-analyzer.src.emoji_analyzer import analyze_mood

mood = analyze_mood("Feeling 😢 today.")
print(mood)  # sad
```

## Testing

Run the bundled tests with `pytest`:

```bash
cd utils/nightly-emoji-mood-analyzer
pytest -q
```

All tests are deterministic and require no external resources.
