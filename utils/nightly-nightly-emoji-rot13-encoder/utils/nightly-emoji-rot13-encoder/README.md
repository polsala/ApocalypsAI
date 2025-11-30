# Nightly Emoji ROT13 Encoder

Utility that transforms alphabetic characters using the classic ROT13 cipher **and** maps each resulting letter to a corresponding emoji. Non‑alphabetic characters are left untouched.

## Features
- `encode(text: str) -> str` – ROT13‑encodes the input and replaces each letter with an emoji.
- `decode(emoji_text: str) -> str` – Reverses the process, yielding the original plain‑text.
- Pure Python 3.11, no external dependencies.

## Example
```python
from src.emoji_rot13 import encode, decode

plain = "Hello, World!"
encoded = encode(plain)
print(encoded)   # 👉😀😃😄😁😆, 😇😈😉😉😊!
print(decode(encoded))  # 👉Hello, World!
```

## How it works
1. **ROT13** – each letter is shifted 13 places in the alphabet (a↔n, b↔o, …). Implemented via the standard `codecs` module.
2. **Emoji mapping** – the 26 resulting letters are each assigned a unique emoji (see source). The mapping is deterministic and reversible.

## Running the tests
```bash
python -m unittest discover -s utils/nightly-emoji-rot13-encoder/tests
```
