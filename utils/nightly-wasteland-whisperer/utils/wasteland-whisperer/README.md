# Wasteland Whisperer

A simple, self-contained utility for encrypting and decrypting short messages using a Vigenere cipher. Perfect for broadcasting vital (or just whimsical) communications across the desolate landscapes of the post-apocalypse, ensuring your whispers remain private from prying ears (or rogue AI scanners).

## Purpose

In a world where digital communication infrastructure is a relic, and even basic radio waves might be monitored by unknown entities, the "Wasteland Whisperer" provides a low-tech, yet effective, method for securing your text messages. It's designed for quick, on-the-fly encryption/decryption, making it ideal for field agents, bunker dwellers, or anyone needing to pass a note without giving away the farm.

## Features

*   **Vigenere Cipher**: A classic polyalphabetic substitution cipher.
*   **Case Preservation**: Maintains the original casing of alphabetic characters.
*   **Non-Alphabetic Character Handling**: Punctuation, numbers, and spaces are preserved as-is.
*   **Command-Line Interface**: Easy to use from any terminal.

## Installation

This utility is self-contained and requires no special installation beyond a Python 3.11+ environment.

1.  Navigate to the `utils/wasteland-whisperer/` directory.
2.  You can run the script directly.

## Usage

The `whisperer.py` script accepts three arguments: `mode`, `message`, and `key`.

```bash
python src/whisperer.py <mode> <message> <key>
```

*   `<mode>`: `encrypt` or `decrypt`
*   `<message>`: The text you want to encrypt or decrypt.
*   `<key>`: The secret keyword. Only alphabetic characters in the key are used for the cipher.

### Examples

**1. Encrypting a message:**

```bash
python src/whisperer.py encrypt "Meet me at the old water tower at dawn." "RAIDER"
# Expected Output: Encrypted message: Dggh qg qg hpg bld xqfgr fowgr qf hq hqxn.
```

**2. Decrypting a message:**

```bash
python src/whisperer.py decrypt "Dggh qg qg hpg bld xqfgr fowgr qf hq hqxn." "RAIDER"
# Expected Output: Decrypted message: Meet me at the old water tower at dawn.
```

**3. Message with numbers and symbols:**

```bash
python src/whisperer.py encrypt "Code: Alpha-7, Rendezvous Point: Sector 42!" "SECRET"
# Expected Output: Encrypted message: Ckfg: Xlphx-7, Rjndgsvkua Pkint: Sgctkr 42!
```

## Development & Testing

To run the tests, navigate to the `utils/wasteland-whisperer/` directory and execute:

```bash
python -m unittest tests/test_whisperer.py
```

All tests are self-contained and do not require network access.
