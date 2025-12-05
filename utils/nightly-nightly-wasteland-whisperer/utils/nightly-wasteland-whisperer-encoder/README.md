# Wasteland Whisperer Message Encoder

## 📻 Overview

In a world where the internet is but a distant, static memory, reliable communication is key. The `Wasteland Whisperer Message Encoder` is a simple, yet robust, command-line utility that allows survivors to encode and decode messages using a classic Caesar cipher. It's easy to use, requires no external dependencies, and ensures your vital messages (like "Beware of the mutated squirrels!" or "Found a stash of pre-war instant coffee!") remain somewhat private from prying eyes.

## 🛠️ Features

*   **Caesar Cipher**: Implements a standard Caesar cipher for shifting alphabetic characters.
*   **Case Preservation**: Maintains the original casing of letters.
*   **Non-Alphabetic Preservation**: Numbers, symbols, and spaces are left untouched.
*   **Encode/Decode Modes**: Easily switch between encrypting and decrypting messages.
*   **Self-Contained**: No external libraries needed, just Python 3.11+.

## 🚀 Usage

Navigate to the `utils/nightly-wasteland-whisperer-encoder/` directory and run the `encoder.py` script.

### Encoding a Message

To encode a message, use the `--message` (or `-m`) and `--shift` (or `-s`) arguments. The `--mode` defaults to `encode`.

```bash
python src/encoder.py --message "Hello, Survivor!" --shift 3
# Or shorter:
python src/encoder.py -m "Hello, Survivor!" -s 3
```

**Example Output:**

```
Original: Hello, Survivor!
Shift: 3
Mode: encode
Result: Khoor, Vxuylyru!
```

### Decoding a Message

To decode a message, add the `--mode decode` (or `-d decode`) argument.

```bash
python src/encoder.py --message "Khoor, Vxuylyru!" --shift 3 --mode decode
# Or shorter:
python src/encoder.py -m "Khoor, Vxuylyru!" -s 3 -d decode
```

**Example Output:**

```
Original: Khoor, Vxuylyru!
Shift: 3
Mode: decode
Result: Hello, Survivor!
```

### Other Examples

*   **Wrapping around the alphabet:**
    ```bash
    python src/encoder.py -m "xyz" -s 3
    # Result: abc
    ```

*   **Messages with numbers and symbols:**
    ```bash
    python src/encoder.py -m "Base 7 is secure!" -s 5
    # Result: Ifxj 7 nx xjhzwj!
    ```

## 🧪 Testing

To ensure the Wasteland Whisperer is always ready for action, run the included unit tests:

```bash
python -m unittest tests/test_encoder.py
```

This will verify the encoding/decoding logic and the command-line interface functionality.
