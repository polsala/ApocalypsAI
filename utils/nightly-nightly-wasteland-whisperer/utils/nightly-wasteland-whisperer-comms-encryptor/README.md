# Nightly Wasteland Whisperer Comms Encryptor

A simple, self-contained command-line utility for basic message obfuscation using a Caesar cipher. In the desolate wastes, sometimes a little privacy is all you need to keep your whispers safe from prying ears.

## Features

*   **Encrypt Messages**: Scramble your plain text into a coded message.
*   **Decrypt Messages**: Unscramble coded messages back into plain text.
*   **Simple Caesar Cipher**: Uses a shift cipher derived from a string key.
*   **Handles Case and Symbols**: Preserves non-alphabetic characters and maintains case.

## Installation

This utility is self-contained and requires Python 3.11+. No external dependencies are needed.

1.  Navigate to the `utils/nightly-wasteland-whisperer-comms-encryptor/` directory.
2.  The main script is `src/encryptor.py`.

## Usage

Run the `encryptor.py` script from your terminal.

```bash
python src/encryptor.py <mode> <message> <key>
```

### Arguments

*   `<mode>`: `encrypt` or `decrypt`. Specifies whether to encrypt or decrypt the message.
*   `<message>`: The text string you want to process.
*   `<key>`: A secret string key. The shift for the Caesar cipher is derived from the sum of the ASCII values of its characters, modulo 26.

### Examples

**Encrypting a message:**

```bash
python src/encryptor.py encrypt "Hello, fellow survivor!" "whisper"
# Expected output (shift for "whisper" is 16):
# Yvccf, vvccf mkikyflh!
```

**Decrypting a message:**

```bash
python src/encryptor.py decrypt "Yvccf, vvccf mkikyflh!" "whisper"
# Expected output:
# Hello, fellow survivor!
```

**Using a different key:**

```bash
python src/encryptor.py encrypt "The stash is under the old oak tree." "maple"
# Expected output (shift for "maple" is 10):
# Dro cjcrx sc yxnob dro ewz eak bboo.
```

## Development

### Running Tests

To ensure the encryptor is functioning correctly, run the provided tests:

```bash
python -m unittest tests/test_encryptor.py
```

## License

This utility is part of the ApocalypsAI project and is licensed under the [MIT License](https://github.com/polsala/ApocalypsAI/blob/main/LICENSE).
