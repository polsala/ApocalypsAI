# Emoji Mood Generator

A tiny, self‑contained utility that turns a textual mood into a list of emojis.

## Why?
- Communicating feelings in chat, commit messages, or documentation can be faster with emojis.
- The mapping is **deterministic** and works **offline** – no network calls, no API keys.

## Features
- Simple Python 3.11 library (`get_emojis(mood: str) -> List[str]`).
- Command‑line interface:
  ```bash
  python -m utils.emoji-mood-generator.src.emoji_mood happy
  # 😄 😊 🥳
  ```
- Optional JSON output (`--json`).
- Comprehensive unit tests.

## Installation
The utility is self‑contained; just copy the folder or import the module directly.

```bash
# From the repository root
python -m utils.emoji-mood-generator.src.emoji_mood happy
```

## Usage
```python
from utils.emoji-mood-generator.src.emoji_mood import get_emojis

print(get_emojis("sad"))  # ['😢', '😞', '☔']
```

### CLI
```bash
$ python -m utils.emoji-mood-generator.src.emoji_mood love
❤️ 😍 💖

$ python -m utils.emoji-mood-generator.src.emoji_mood confused --json
["🤔", "😕", "🙃"]
```

## Mood → Emoji Mapping
| Mood | Emojis |
|------|--------|
| happy | 😄 😊 🥳 |
| sad | 😢 😞 ☔ |
| angry | 😠 🤬 🔥 |
| love | ❤️ 😍 💖 |
| surprised | 😲 🤯 😮 |
| tired | 😴 🥱 😪 |
| confused | 🤔 😕 🙃 |
| celebrate | 🎉 🥂 🍾 |

## Testing
Run the bundled tests with:
```bash
python -m unittest discover -s utils/emoji-mood-generator/tests
```
All tests are deterministic and require no external resources.
