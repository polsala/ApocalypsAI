# Emoji Commit Helper

A tiny utility that suggests an emoji to prepend to your git commit messages based on simple keyword heuristics.

## Features
- No external dependencies – pure Python 3.11.
- Deterministic keyword → emoji mapping.
- Works as a module (`python -m emoji_commit_helper "<msg>"`) or can be imported.

## Installation
Just copy the `src/emoji_commit_helper.py` file into your project or add the whole folder to your `PYTHONPATH`.

## Usage
```bash
python -m emoji_commit_helper "Add new feature to API"
# Output: ✨ Add new feature to API
```

You can also use the library programmatically:
```python
from emoji_commit_helper import suggest_emoji
print(suggest_emoji("Fix bug in parser"))  # 🐛
```

## How it works
The helper scans the commit message for a set of predefined keywords (e.g., `feat`, `fix`, `docs`). The first matching keyword determines the emoji. If no keyword matches, a generic celebration emoji 🎉 is returned.

## Contributing
Feel free to extend the `KEYWORD_EMOJI_MAP` in the source file to cover more cases.
