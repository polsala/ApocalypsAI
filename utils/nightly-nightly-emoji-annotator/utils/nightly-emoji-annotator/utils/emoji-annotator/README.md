# Emoji Annotator

`emoji-annotator` is a lightweight, zero‑dependency Python 3.11 utility that enriches plain‑text files with emojis.

## Features

- **Offline & deterministic** – no network calls, pure keyword‑based mapping.
- **Simple CLI** – `python -m emoji_annotator <input> <output>`.
- **Tested** – unit tests live under `tests/` and use only the standard library.

## How it works

Each line is scanned for a handful of keywords. The first matching keyword determines the emoji that gets appended. If no keyword matches, a neutral "🤔" is used.

| Keyword(s) | Emoji |
|------------|-------|
| happy, joy, glad | 😊 |
| sad, sorrow, upset | 😢 |
| love, heart | ❤️ |
| angry, mad, furious | 😠 |
| surprise, wow | 😲 |
| (none) | 🤔 |

## Usage

```bash
# Install (no deps required, just copy the folder)
python -m emoji_annotator input.txt output.txt
```

The `output.txt` will contain the original lines with an emoji appended.

## Development

Run the test suite with:

```bash
python -m unittest discover -s utils/nightly-emoji-annotator/utils/emoji-annotator/tests
```
