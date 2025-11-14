# Wasteland Whisperer: Secure Your Post-Apocalyptic Comms

In the desolate future, trust is a luxury. The Wasteland Whisperer provides a simple, robust way to encrypt and decrypt your vital messages using a classic Vigenere cipher. Keep your secrets safe from rogue AI, mutant scavengers, and nosy neighbors.

## Features

*   **Simple Vigenere Cipher**: A time-tested polyalphabetic substitution cipher.
*   **Case-Insensitive Keys**: Keys are automatically converted to uppercase for consistency.
*   **Preserves Non-Alphabetic Characters**: Spaces, numbers, and punctuation are kept intact; only alphabetic characters are encrypted/decrypted.
*   **Command-Line Interface**: Easy to use from your terminal.

## How to Use

1.  **Navigate to the utility directory**:
    ```bash
    cd utils/wasteland-whisperer
    ```

2.  **Encrypt a message**:
    ```bash
    python src/whisperer.py encode "Hello World, this is a secret message!" "SURVIVE"
    ```
    Expected Output:
    ```
    ZYCGW RSJFU, BCMK CJ V AZGJYK UZWKU XZ!
    ```

3.  **Decrypt a message**:
    ```bash
    python src/whisperer.py decode "ZYCGW RSJFU, BCMK CJ V AZGJYK UZWKU XZ!" "SURVIVE"
    ```
    Expected Output:
    ```
    HELLO WORLD, THIS IS A SECRET MESSAGE!
    ```

## How it Works

The Vigenere cipher uses a keyword to encrypt a plaintext message. Each letter of the plaintext is shifted by a different amount determined by the corresponding letter of the keyword. The keyword is repeated as many times as necessary to match the length of the plaintext. Decryption reverses this process. This utility handles the letter-to-number and number-to-letter conversions, ensuring only alphabetic characters are processed while preserving the original formatting of your message.
