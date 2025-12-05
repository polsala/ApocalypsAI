# Nightly Emoji Encoder

Utility to encode plain ASCII strings into a sequence of emojis and decode them back. Fun for adding secret emoji messages to commits, PR comments, etc.

## Features

- Encode lowercase alphabetic strings to emojis.
- Decode emoji sequences back to original text.
- CLI interface.

## Installation

Copy the `src` folder into your project or run directly with Python 3.11.

## Usage

```bash
python -m src.emoji_encoder encode "hello"
# Output: 😆😅😎😎😍

python -m src.emoji_encoder decode "😆😅😎😎😍"
# Output: hello
```

## Limitations

- Only supports lowercase letters a‑z. Other characters raise an error.

## Testing

Run `pytest` in the `tests` directory.
