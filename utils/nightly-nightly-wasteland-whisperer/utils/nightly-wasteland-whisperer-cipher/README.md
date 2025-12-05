# Nightly Wasteland Whisperer Cipher

## A Simple Message Obfuscator for the Discerning Survivor

In the chaotic aftermath, clear communication is a luxury. The Wasteland Whisperer Cipher provides a simple, yet effective, way to obfuscate your messages from prying eyes (or ears, if you're broadcasting). Based on the ancient Caesar cipher, it shifts letters by a specified amount, making your secrets just a little harder to decipher.

### Features

*   **Encrypt**: Turn plain text into cryptic messages.
*   **Decrypt**: Reveal the hidden meaning of whispered secrets.
*   **Configurable Shift**: Choose your level of obfuscation.
*   **Self-contained**: No external dependencies, just pure Python power.

### How to Use

1.  Navigate to the `src` directory:
    ```bash
    cd utils/nightly-wasteland-whisperer-cipher/src
    ```

2.  **Encrypt a message**:
    ```bash
    python cipher.py encrypt "Hello, survivor!" --shift 3
    # Output: Khoor, vxuylyru!
    ```

3.  **Decrypt a message**:
    ```bash
    python cipher.py decrypt "Khoor, vxuylyru!" --shift 3
    # Output: Hello, survivor!
    ```

4.  **Help**:
    ```bash
    python cipher.py --help
    ```

### Examples

*   Encrypting with a shift of 5:
    ```bash
    python cipher.py encrypt "The quick brown fox jumps over the lazy dog." --shift 5
    # Output: Ymj vznhp gwtbs ktc ozrux tajw ymj qfed itl.
    ```
*   Decrypting with a shift of 5:
    ```bash
    python cipher.py decrypt "Ymj vznhp gwtbs ktc ozrux tajw ymj qfed itl." --shift 5
    # Output: The quick brown fox jumps over the lazy dog.
    ```
*   Handling non-alphabetic characters:
    ```bash
    python cipher.py encrypt "123 ApocalypsAI!" --shift 1
    # Output: 123 BqpdqmjqpsBJ!
    ```

### Running Tests

To ensure your whispers remain secure, run the included tests:

1.  Navigate to the `tests` directory:
    ```bash
    cd utils/nightly-wasteland-whisperer-cipher/tests
    ```
2.  Run `pytest` (or `python -m unittest` if `pytest` is not installed):
    ```bash
    python -m unittest test_cipher.py
    ```
