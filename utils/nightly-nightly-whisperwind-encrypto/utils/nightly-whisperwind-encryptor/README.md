# Nightly Whisperwind Encryptor

A simple, self-contained Python utility for obfuscating and revealing text messages using a Vigenere cipher. In the uncertain times ahead, sometimes a little obscurity is all you need to keep your whispers private.

## Purpose

This utility provides a basic command-line interface to encrypt or decrypt text using a shared passphrase. It's not designed for military-grade security, but rather for quick, offline obfuscation of messages, perfect for passing notes in a post-apocalyptic landscape or simply adding a touch of mystery to your digital communications.

## How it Works

The Whisperwind Encryptor uses the **Vigenere cipher**, a method of encrypting alphabetic text by using a series of different Caesar ciphers based on the letters of a keyword. Non-alphabetic characters (numbers, symbols, spaces) are passed through unchanged, and the original casing of alphabetic characters is preserved.

## Usage

### Prerequisites

*   Python 3.11 (or compatible)

### Running the Utility

Navigate to the `utils/nightly-whisperwind-encryptor/` directory.

#### Encrypting a Message

```bash
python src/encryptor.py --mode encrypt --text "The quick brown fox jumps over the lazy dog." --key "APOCALYPSE"
```

Example Output:
```
Whisperwind Encrypted: Tpe qeick brmwn fpx jupms ovfr the lzzy dog.
```

#### Decrypting a Message

```bash
python src/encryptor.py --mode decrypt --text "Tpe qeick brmwn fpx jupms ovfr the lzzy dog." --key "APOCALYPSE"
```

Example Output:
```
Whisperwind Decrypted: The quick brown fox jumps over the lazy dog.
```

### Key Considerations

*   The key (passphrase) should ideally be a word or phrase containing only alphabetic characters. Non-alphabetic characters in the key will be ignored.
*   A key with no alphabetic characters will result in an error.
*   The security of the Vigenere cipher is limited. It's suitable for casual obfuscation, not for protecting highly sensitive information against determined adversaries.

## Development & Testing

To run the tests, navigate to the `utils/nightly-whisperwind-encryptor/` directory and execute:

```bash
python -m unittest tests/test_encryptor.py
```
