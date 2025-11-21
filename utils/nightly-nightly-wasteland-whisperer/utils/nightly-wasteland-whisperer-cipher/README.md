# Nightly Wasteland Whisperer Cipher

## Encrypting Secrets for the Post-Apocalyptic Era

In the desolate future, secure communication is paramount. The **Wasteland Whisperer Cipher** is a simple, yet effective, command-line utility designed to encrypt and decrypt short messages using a classic Caesar cipher. Whether you're coordinating a scavenging run or sharing vital intel, ensure your whispers remain private.

### Features

*   **Caesar Cipher**: A robust (for its simplicity!) shift cipher.
*   **Encrypt/Decrypt Modes**: Easily switch between securing and revealing messages.
*   **Command-Line Interface**: Quick and easy to use directly from your terminal.

### Installation

This utility is self-contained and requires Python 3.6+ (or any version compatible with f-strings and basic string manipulation). No external dependencies are needed.

```bash
# Navigate to the utility's directory
cd utils/nightly-wasteland-whisperer-cipher/
```

### Usage

The `cipher.py` script accepts a message, a shift key (an integer), and an operation (`encrypt` or `decrypt`).

#### Encrypting a Message

To encrypt a message, use the `--mode encrypt` flag:

```bash
python src/cipher.py --mode encrypt --message "Rubble ahead, proceed with caution." --key 3
```

Example Output:
```
Encrypted message: "UXEEOH DKHDG, SURFHHG ZLWK FDXWLRQ."
```

#### Decrypting a Message

To decrypt a message, use the `--mode decrypt` flag:

```bash
python src/cipher.py --mode decrypt --message "UXEEOH DKHDG, SURFHHG ZLWK FDXWLRQ." --key 3
```

Example Output:
```
Decrypted message: "Rubble ahead, proceed with caution."
```

#### Help

For more options:

```bash
python src/cipher.py --help
```

### How it Works (The Caesar Cipher)

The Caesar cipher works by shifting each letter in the plaintext by a certain number of places down or up the alphabet. For example, with a shift of 3, 'A' would become 'D', 'B' would become 'E', and so on. The cipher wraps around the alphabet (e.g., 'X' with a shift of 3 becomes 'A'). Non-alphabetic characters (numbers, symbols, spaces) are left unchanged.
