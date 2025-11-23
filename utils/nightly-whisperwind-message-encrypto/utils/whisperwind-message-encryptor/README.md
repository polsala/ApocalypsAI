# Whisperwind Message Encryptor

## 🌬️ Secure Your Whispers in the Wind 🌬️

In the desolate quiet of the post-apocalypse, reliable communication is paramount. The Whisperwind Message Encryptor provides a simple, yet effective, way to encrypt and decrypt short messages using a classic Caesar cipher. No complex machinery, no network required – just a shared shift key and a bit of ingenuity.

### Features:

*   **Simple Caesar Cipher**: Easy to understand and implement, even with limited resources.
*   **Encrypt & Decrypt Modes**: Toggle between securing your messages and revealing their secrets.
*   **CLI Interface**: Quick and easy to use from any terminal.
*   **Self-Contained**: No external dependencies beyond standard Python libraries.

## Usage

This utility is a Python 3.11 script. You can run it directly from the command line.

### Encryption

To encrypt a message, provide the `--text` and `--shift` arguments. The `--mode` defaults to `encrypt`.

```bash
python3 utils/whisperwind-message-encryptor/src/encryptor.py --text "Hello, survivor!" --shift 3
```

**Output:**

```
Khoor, vxuylyru!
```

### Decryption

To decrypt a message, provide the encrypted text, the original `--shift` value, and set `--mode` to `decrypt`.

```bash
python3 utils/whisperwind-message-encryptor/src/encryptor.py --text "Khoor, vxuylyru!" --shift 3 --mode decrypt
```

**Output:**

```
Hello, survivor!
```

### Examples:

*   **Encrypting a secret rendezvous point:**
    ```bash
    python3 utils/whisperwind-message-encryptor/src/encryptor.py --text "Meet at the old water tower tonight." --shift 7
    # Output: "Tlly ha aol vsk dhaly avdly avupnoa."
    ```

*   **Decrypting a supply cache location:**
    ```bash
    python3 utils/whisperwind-message-encryptor/src/encryptor.py --text "Tlly ha aol vsk dhaly avdly avupnoa." --shift 7 --mode decrypt
    # Output: "Meet at the old water tower tonight."
    ```

## Development

### Running Tests

To ensure the Whisperwind Encryptor is functioning correctly, navigate to the utility's root directory and run the tests using `unittest`:

```bash
cd utils/whisperwind-message-encryptor
python3 -m unittest tests/test_encryptor.py
```

All tests should pass, confirming the cipher's integrity.
