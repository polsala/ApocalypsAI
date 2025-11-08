# Wasteland Whisperer

## Cryptic Communications for the End Times

In the desolate expanse of the post-apocalyptic world, clear communication is a luxury. The Wasteland Whisperer is a simple, self-contained utility designed to encode and decode messages using a classic Vigenere cipher. Perfect for sharing vital intel, coordinating scavenger runs, or simply sending a cryptic note to a fellow survivor without fear of prying eyes (or rogue AI scanners).

### Features

*   **Vigenere Cipher**: A time-tested polyalphabetic substitution cipher.
*   **Keyword-Based Encryption**: Your secret keyword is the key to your messages.
*   **Simple & Self-Contained**: A single Python script, no external dependencies.
*   **Offline Operation**: Works anywhere, even when the internet is just a myth.

### How to Use

#### Prerequisites

*   Python 3.6+ (tested with 3.11)

#### Encoding a Message

To encode a message, run the script with the `-e` or `--encode` flag, providing your message and a keyword:

```bash
python src/whisperer.py --encode "MEET ME AT THE OLD BRIDGE" --keyword "SURVIVAL"
```

Example Output:
```
Original Message: MEET ME AT THE OLD BRIDGE
Keyword: SURVIVAL
Encoded Message: EIIF EI AF FHI OLE ZVILGI
```

#### Decoding a Message

To decode a message, use the `-d` or `--decode` flag with the encoded message and the *same* keyword:

```bash
python src/whisperer.py --decode "EIIF EI AF FHI OLE ZVILGI" --keyword "SURVIVAL"
```

Example Output:
```
Encoded Message: EIIF EI AF FHI OLE ZVILGI
Keyword: SURVIVAL
Decoded Message: MEET ME AT THE OLD BRIDGE
```

#### Command Line Arguments

*   `-e`, `--encode <message>`: The message to encode.
*   `-d`, `--decode <message>`: The message to decode.
*   `-k`, `--keyword <keyword>`: The keyword for encryption/decryption. **Required for both modes.**

### How it Works (Briefly)

The Vigenere cipher uses a keyword to determine different Caesar shifts for each letter in the plaintext. Non-alphabetic characters (spaces, numbers, punctuation) are preserved but not encrypted. The cipher operates on uppercase English letters (A-Z), preserving the original case of alphabetic characters.

### Development & Testing

To run the tests, navigate to the `wasteland-whisperer` directory and execute:

```bash
python -m unittest tests/test_whisperer.py
```
