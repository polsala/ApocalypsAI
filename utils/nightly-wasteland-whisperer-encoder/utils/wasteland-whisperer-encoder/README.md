# Wasteland Whisperer Message Encoder

A simple, self-contained utility for encoding and decoding messages using a configurable Caesar cipher. Perfect for transmitting cryptic messages across the desolate wastes without attracting too much attention from rogue AI or mutated wildlife.

## Features

*   **Caesar Cipher**: Shift letters by a specified amount.
*   **Configurable Shift**: Easily change the encryption key (shift value).
*   **CLI Interface**: Encode or decode messages directly from your terminal.
*   **Self-contained**: No external dependencies beyond standard Python libraries.

## Usage

### Encoding a message

```bash
python src/encoder.py encode "Hello, wasteland!" --shift 3
```

Output:
```
KHOOR, ZDVWHODQG!
```

### Decoding a message

```bash
python src/encoder.py decode "KHOOR, ZDVWHODQG!" --shift 3
```

Output:
```
HELLO, WASTELAND!
```

### Help

```bash
python src/encoder.py --help
```

## How it works

The utility applies a Caesar cipher, shifting each alphabetic character in the message by the specified `shift` value. Non-alphabetic characters (numbers, symbols, spaces) are left unchanged. The cipher wraps around the alphabet (e.g., 'Z' + 1 becomes 'A').
