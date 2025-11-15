# Ancient Whisper Decoder

Unearth the secrets of the past (or just poorly encoded messages) with the Ancient Whisper Decoder! This utility attempts to decipher cryptic strings using a battery of common encoding and cipher techniques.

## Features

*   **Base64 Decoding**: Unravel base64 encoded messages.
*   **ROT13 Decoding**: Decode messages shifted by ROT13.
*   **String Reversal**: Sometimes the simplest solution is the right one.

## How to Use

Run the `decoder.py` script with the mysterious message as a command-line argument.

```bash
python src/decoder.py "SGVsbG8sIFdvcmxkIQ=="
# Expected output:
# Attempting to decode: 'SGVsbG8sIFdvcmxkIQ=='
# ------------------------------
# Base64: Hello, World!

python src/decoder.py "Uryyb, Jbeyq!"
# Expected output:
# Attempting to decode: 'Uryyb, Jbeyq!'
# ------------------------------
# ROT13: Hello, World!

python src/decoder.py "!dlroW ,olleH"
# Expected output:
# Attempting to decode: '!dlroW ,olleH'
# ------------------------------
# Reverse: Hello, World!

python src/decoder.py "This is a plain message."
# Expected output:
# Attempting to decode: 'This is a plain message.'
# ------------------------------
# No common encoding/cipher found or message is already plain.
```

## Development

This utility is written in Python 3.11 and is self-contained. No external dependencies are required beyond the standard library.
