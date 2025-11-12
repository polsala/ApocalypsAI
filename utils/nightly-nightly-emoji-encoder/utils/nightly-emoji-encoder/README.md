# Nightly Emoji Encoder

Utility that encodes plain ASCII strings into a sequence of emojis and decodes them back. Useful for adding a playful layer of obfuscation to logs, commit messages, or CI output.

## Features

- Encode any uppercase alphabetic string (A‑Z) into emojis.
- Decode previously encoded emoji strings back to the original text.
- CLI interface: `python -m src.emoji_encoder encode "HELLO"` or `decode "😀😁..."`.
- No external dependencies; pure Python 3.11.

## Usage

```bash
python -m src.emoji_encoder encode "HELLO"
# Output: 😀😁😂😂😃

python -m src.emoji_encoder decode "😀😁😂😂😃"
# Output: HELLO
```

## Limitations

- Only supports uppercase A‑Z letters; other characters raise `ValueError`.
