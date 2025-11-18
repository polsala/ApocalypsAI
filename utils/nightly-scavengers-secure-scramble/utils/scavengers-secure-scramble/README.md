# Scavenger's Secure Scramble

A simple, self-contained command-line utility for encrypting and decrypting text messages using a Vigenere cipher. Perfect for sharing secret notes in the post-apocalyptic wasteland, or just keeping your grocery list safe from prying eyes.

## Features

*   **Vigenere Cipher**: A classic polyalphabetic substitution cipher.
*   **Case Preservation**: Maintains the original casing of alphabetic characters.
*   **Non-Alphabetic Preservation**: Spaces, numbers, and symbols are left untouched.
*   **Simple CLI**: Easy to use from your terminal.
*   **Self-contained**: No external dependencies beyond standard Python libraries.

## Installation

This utility is self-contained. Simply copy the `scavengers-secure-scramble` folder to your desired location.

## Usage

Run the `scramble.py` script from the `src/` directory.

```bash
python3 src/scramble.py --help
```

### Encrypting a message

To encrypt a message, use the `--encrypt` flag along with `--text` and `--key`:

```bash
python3 src/scramble.py --text "The secret stash is under the old oak tree." --key "HIDDEN" --encrypt
# Expected output: Encrypted: Aol wkjxkj wjwhr ew yvjkt aol gld ghr xkjj.
```

### Decrypting a message

To decrypt a message, use the `--decrypt` flag along with `--text` (the encrypted message) and the **same** `--key`:

```bash
python3 src/scramble.py --text "Aol wkjxkj wjwhr ew yvjkt aol gld ghr xkjj." --key "HIDDEN" --decrypt
# Expected output: Decrypted: The secret stash is under the old oak tree.
```

### Examples

*   **Simple message:**
    ```bash
    python3 src/scramble.py --text "Hello World" --key "KEY" --encrypt
    # Encrypted: Rijvs Gspqv
    python3 src/scramble.py --text "Rijvs Gspqv" --key "KEY" --decrypt
    # Decrypted: Hello World
    ```

*   **Message with numbers and symbols:**
    ```bash
    python3 src/scramble.py --text "My coordinates are 123.45, -67.89!" --key "MAP" --encrypt
    # Encrypted: Qy gssrdewbaxkw bvi 123.45, -67.89!
    python3 src/scramble.py --text "Qy gssrdewbaxkw bvi 123.45, -67.89!" --key "MAP" --decrypt
    # Decrypted: My coordinates are 123.45, -67.89!
    ```

## Limitations

The Vigenere cipher is a relatively simple cipher and is **not suitable for high-security applications**. It's primarily for fun, learning, or very low-stakes privacy. For serious security, use modern cryptographic methods.

## Development

To run tests:

```bash
python3 -m unittest tests/test_scramble.py
```
