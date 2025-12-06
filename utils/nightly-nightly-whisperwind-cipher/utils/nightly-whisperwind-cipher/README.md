# Nightly Whisperwind Cipher

A simple, self-contained command-line utility for encrypting and decrypting messages using a substitution cipher. Ideal for sending secret messages across the desolate wastes, ensuring your vital intel (or grocery list) remains unreadable to prying eyes.

## Features

*   **Simple Substitution**: Uses a configurable 26-letter key to map characters.
*   **Case-Insensitive**: Handles both uppercase and lowercase input, outputting uppercase.
*   **Non-Alphabetic Passthrough**: Numbers, symbols, and spaces are preserved.
*   **Command-Line Interface**: Easy to use from your terminal.

## How to Use

### Prerequisites

*   Python 3.6+

### Running the Utility

Navigate to the `src` directory within `utils/nightly-whisperwind-cipher/` and run `cipher.py` with the desired arguments.

```bash
# Encrypt a message with the default key
python src/cipher.py --encrypt --text "Hello, wasteland!"

# Encrypt a message with a custom key
python src/cipher.py --encrypt --text "Secret plans" --key "XPMGTDHLYONZWEQJRUVICSAKFB"

# Decrypt a message with the default key
python src/cipher.py --decrypt --text "TGUUX, PXCGUFXCP!"

# Decrypt a message with a custom key
python src/cipher.py --decrypt --text "QYOGQJ BXCG" --key "XPMGTDHLYONZWEQJRUVICSAKFB"

# Get help
python src/cipher.py --help
```

### Key Format

The cipher key must be a 26-character string containing all unique uppercase English letters (A-Z) in any order. The default key is `XPMGTDHLYONZWEQJRUVICSAKFB`.

## How it Works

The utility implements a monoalphabetic substitution cipher. Each letter in the plaintext is replaced by a letter from the key based on its position in the standard alphabet. For example, if the key maps 'A' to 'X', then every 'A' in the plaintext becomes an 'X' in the ciphertext.
