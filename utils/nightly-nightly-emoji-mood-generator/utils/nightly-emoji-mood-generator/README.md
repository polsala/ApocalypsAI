# Nightly Emoji Mood Generator

`nightly-emoji-mood-generator` is a whimsical yet useful command‑line utility that converts a human‑readable mood description into an emoji (or a short emoji string).  It can be used to spice up commit messages, Slack statuses, or any place where a quick visual cue is handy.

## Features

- **Deterministic mapping** – a fixed dictionary of common moods → emojis.
- **Case‑insensitive** input.
- **Fallback** to a neutral face when the mood is unknown.
- **Zero external dependencies** – pure Python 3.11.

## Installation & Usage

```bash
# Clone the repository (or copy the folder) and run the script directly
python -m utils.nightly-emoji-mood-generator.src.mood "happy"
```

The script prints the emoji to stdout, e.g. `😊`.

## Development

Run the test suite with:

```bash
python -m unittest discover -s utils/nightly-emoji-mood-generator/tests
```

## License

MIT – see the top‑level LICENSE file.
