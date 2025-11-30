# nightly‑emoji‑lookup

A whimsical yet handy utility for the community:

- **What it does**: Provides a small emoji dictionary and two lookup functions:
  - `get_emoji(name: str) -> str | None` – returns the Unicode character for a given short name.
  - `get_name(char: str) -> str | None` – returns the short name for a given Unicode character.
- **CLI**: `python -m emoji_lookup <name|char>` prints the matching result or an error message.
- **Why it’s useful**: Quickly embed emojis in scripts, commit messages, or documentation without leaving the terminal.
- **Self‑contained**: No external data sources; the dictionary is baked into the module, making the tests deterministic and offline.

## Usage
```bash
# As a library
>>> from emoji_lookup import get_emoji, get_name
>>> get_emoji('rocket')
'🚀'
>>> get_name('🚀')
'rocket'

# As a CLI
$ python -m emoji_lookup rocket
🚀
$ python -m emoji_lookup 🚀
rocket
```

## Testing
Run the bundled tests with:
```bash
python -m unittest discover -s utils/nightly-emoji-lookup/tests
```
