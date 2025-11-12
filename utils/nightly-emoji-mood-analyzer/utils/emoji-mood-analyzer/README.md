# Emoji Mood Analyzer

A whimsical‑yet‑useful command‑line tool that turns a short piece of text into a mood‑representing emoji.

## Features
- Pure Python 3.11, no external dependencies.
- Deterministic keyword‑based mapping (happy → 😊, sad → 😢, angry → 😠, neutral → 🤔).
- Simple `--text` argument or pipe input.
- Comes with a tiny test suite that runs offline.

## Installation & Usage
```bash
# Clone the repository (or copy the folder) and run the module directly:
python -m utils.emoji-mood-analyzer.src.analyzer "I love this project!"
# → 😊
```

You can also pipe text:
```bash
echo "I'm feeling terrible today" | python -m utils.emoji-mood-analyzer.src.analyzer
# → 😢
```

## How it works
The analyzer lower‑cases the input and looks for a set of mood‑related keywords. The first matching category wins. If nothing matches, a thinking face 🤔 is returned.

## Testing
```bash
python -m pytest utils/emoji-mood-analyzer/tests
```
All tests are deterministic and require no network access.
