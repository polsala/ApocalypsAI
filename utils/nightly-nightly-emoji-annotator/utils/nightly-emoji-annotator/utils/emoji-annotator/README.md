# Emoji Annotator

**Utility name:** `emoji-annotator`

## What it does
`emoji-annotator` scans a block of text, looks for a handful of predefined keywords, and appends a matching emoji to each sentence that contains one of those keywords. The mapping is deliberately tiny and deterministic so the utility stays self‑contained and offline.

## Installation & usage
```bash
# Clone the repository (or copy the folder) and cd into it
cd utils/nightly-emoji-annotator
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt  # (no external deps required)

# Run the CLI
python -m emoji_annotator "I love coding! It makes me happy."
# → I love coding! ❤️ It makes me happy 😊.
```

You can also import the core function in your own Python code:
```python
from src.annotator import annotate
print(annotate("Fire! What a star?"))
# → Fire! 🔥 What a star? ⭐
```

## Keyword → Emoji mapping (hard‑coded)
| Keyword | Emoji |
|---------|-------|
| love    | ❤️   |
| happy   | 😊   |
| sad     | 😢   |
| fire    | 🔥   |
| star    | ⭐   |
| question| ❓   |
| exclamation| ❗ |

The mapping can be extended by editing `src/annotator.py`.

## Testing
Run the bundled tests with:
```bash
pytest -q
```
All tests are deterministic and require no network access.
