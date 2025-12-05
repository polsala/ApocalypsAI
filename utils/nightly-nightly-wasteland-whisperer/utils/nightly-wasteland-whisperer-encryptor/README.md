# Nightly Wasteland Whisperer Encryptor

## Overview

The `nightly-wasteland-whisperer-encryptor` is a lightweight, command-line utility designed for basic, discreet communication in a world where advanced tech is a luxury. It implements a classic Caesar cipher, allowing you to encrypt and decrypt short messages with a simple numerical shift. Think of it as your trusty pen-and-paper cipher, but digital!

## Features

*   **Encrypt Messages**: Scramble your secrets with a specified shift.
*   **Decrypt Messages**: Unscramble received whispers back into plain text.
*   **Simple & Robust**: Handles uppercase, lowercase, and preserves non-alphabetic characters.
*   **Self-contained**: No external dependencies, just pure Python.

## Usage

### Prerequisites

*   Python 3.6+ (tested with 3.11)

### Running the Utility

Navigate to the `src` directory within the utility's folder and run `encryptor.py`.

```bash
# Encrypt a message
python src/encryptor.py --message "Hello, survivor!" --shift 3 --mode encrypt

# Decrypt a message
python src/encryptor.py --message "Khoor, vxuylyru!" --shift 3 --mode decrypt

# Encrypt with a negative shift (shifts left)
python src/encryptor.py --message "Secret" --shift -5 --mode encrypt

# Decrypt with a large shift (wraps around)
python src/encryptor.py --message "Wkh qljkw lv gdun." --shift 23 --mode decrypt
```

### Command-line Arguments

*   `--message <TEXT>`: The message string to encrypt or decrypt. (Required)
*   `--shift <INTEGER>`: The numerical shift value. Positive for right shift, negative for left shift. (Required)
*   `--mode <MODE>`: Operation mode. Can be `encrypt` or `decrypt`. (Required)

## Examples

```bash
# Encrypting "ApocalypsAI" with a shift of 5
python src/encryptor.py --message "ApocalypsAI" --shift 5 --mode encrypt
# Output: "FubnfqbmxFI"

# Decrypting "FubnfqbmxFI" with a shift of 5
python src/encryptor.py --message "FubnfqbmxFI" --shift 5 --mode decrypt
# Output: "ApocalypsAI"

# Encrypting a message with numbers and symbols
python src/encryptor.py --message "Base 13, over and out!" --shift 7 --mode encrypt
# Output: "Ihfl 13, vcly huk vba!"
```
