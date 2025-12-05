# Nightly Whisperwind Encoder

A whimsical yet practical command-line utility for encoding and decoding short messages using a simple repeating-key XOR cipher. Perfect for discreet communication in a world where privacy is a luxury, or just for fun!

## Philosophy

In the chaotic aftermath, clear and secure communication is paramount. The Whisperwind Encoder provides a lightweight, offline method to obscure your messages from prying eyes, ensuring your whispers remain just that – whispers.

## Features

*   **Simple XOR Cipher**: Uses a repeating-key XOR algorithm for basic message obfuscation.
*   **Hex Output**: Encoded messages are presented as hexadecimal strings for easy sharing and copy-pasting.
*   **Offline & Self-Contained**: No external dependencies or network access required.
*   **Easy to Use**: Straightforward command-line interface for encoding and decoding.

## Installation

This utility is written in Python 3.11+ and requires no special installation beyond having Python available.

```bash
# Clone the repository (if you haven't already)
git clone https://github.com/polsala/ApocalypsAI.git
cd ApocalypsAI/utils/nightly-whisperwind-encoder
```

## Usage

Navigate to the `src` directory within the `nightly-whisperwind-encoder` folder.

### Encoding a Message

To encode a message, provide the `encode` mode, your message, and a secret key:

```bash
python src/encoder.py encode "Hello, fellow survivor!" "mysecretkey"
```

Example Output:
```
Encoded (hex): 0c1a1f1f1c5c261a191f1d
```
*(Note: The actual hex output will vary based on your message and key.)*

### Decoding a Message

To decode a hex-encoded message, provide the `decode` mode, the hex string, and the *exact same secret key*:

```bash
python src/encoder.py decode "0c1a1f1f1c5c261a191f1d" "mysecretkey"
```

Example Output:
```
Decoded: Hello, fellow survivor!
```

### Important Notes

*   **Key Security**: The security of your message relies entirely on the secrecy of your key. Choose strong, unique keys.
*   **Simplicity**: This is a basic cipher, suitable for casual privacy. It is **not** designed for high-security cryptographic applications. Do not use it for sensitive data that requires robust encryption.
*   **Character Support**: Supports UTF-8 characters for both messages and keys.

## Development & Testing

To run the tests, navigate to the `nightly-whisperwind-encoder` directory and execute:

```bash
python -m unittest tests/test_encoder.py
```
