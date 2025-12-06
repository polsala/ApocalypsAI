# Wasteland Whisperer Encoder

A whimsical command-line utility for encoding and decoding short messages using a simple Caesar cipher. Perfect for discreet communication in a post-apocalyptic world where you don't want the rad-roaches or rival factions eavesdropping on your vital intel.

## Features

*   **Simple Caesar Cipher**: Easy to understand and implement, yet effective enough for casual obfuscation.
*   **Configurable Shift**: Choose your secret shift value for added security (or confusion).
*   **Case-Preserving**: Maintains original casing of letters.
*   **Non-Alphabetic Passthrough**: Numbers, symbols, and spaces are left untouched.
*   **Encode & Decode Modes**: Switch between encrypting your whispers and decrypting incoming intel.

## Installation

This utility is self-contained and written in Python 3.11+. No external dependencies are required.

1.  Navigate to the `wasteland-whisperer-encoder` directory.
2.  Run directly using `python src/encoder.py`.

## Usage

The `encoder.py` script accepts the following command-line arguments:

*   `--message <TEXT>`: The message string to encode or decode. (Required)
*   `--shift <INTEGER>`: The integer value by which to shift characters. (Required)
*   `--mode <MODE>`: The operation mode, either `encode` or `decode`. (Required)

### Examples

**Encoding a message:**

```bash
python src/encoder.py --mode encode --message "Hello, Survivor!" --shift 3
# Expected Output: Khoor, Vxuylyru!
```

**Decoding a message:**

```bash
python src/encoder.py --mode decode --message "Khoor, Vxuylyru!" --shift 3
# Expected Output: Hello, Survivor!
```

**Using a negative shift (decoding with a positive shift is equivalent to encoding with a negative shift):**

```bash
python src/encoder.py --mode encode --message "ApocalypsAI" --shift -1
# Expected Output: ZoobkzlorzH
```

**Handling special characters and numbers:**

```bash
python src/encoder.py --mode encode --message "Base 42 is secure." --shift 5
# Expected Output: Ifxj 42 nx xjhzwj.
```

## How it Works

The utility applies a Caesar cipher, shifting each alphabetic character by the specified `shift` value within its respective case (A-Z or a-z). Non-alphabetic characters are ignored. The `decode` mode simply applies the shift in the opposite direction.
